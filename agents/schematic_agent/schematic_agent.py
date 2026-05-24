"""SchematicAgent — generates connection relationships between selected components.

Uses rule-based pin mapping + LLM reasoning for more complex routing decisions.

This is step 3 of the CircuitAgent pipeline.
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from models.schemas import Component, PinConnection, Schematic

# ── Common pin mappings ─────────────────────────────────────────────
# Maps (from_category, to_category, protocol) → typical pin pairs
# These are design rules that reduce LLM hallucination for common buses.

PIN_RULES: dict[tuple[str, str, str], list[tuple[str, str]]] = {
    # I2C bus rules (MCU ↔ anything I2C)
    ("MCU", "Sensor", "I2C"): [("GPIO22", "SCL"), ("GPIO21", "SDA")],
    ("MCU", "Display", "I2C"): [("GPIO22", "SCL"), ("GPIO21", "SDA")],
    ("MCU", "Interface", "I2C"): [("GPIO22", "SCL"), ("GPIO21", "SDA")],

    # SPI bus rules (MCU ↔ SPI peripherals)
    ("MCU", "Display", "SPI"): [
        ("GPIO18", "SCK"),
        ("GPIO23", "MOSI"),
        ("GPIO5", "CS"),
        ("GPIO19", "DC"),
    ],
    ("MCU", "Sensor", "SPI"): [
        ("GPIO18", "SCK"),
        ("GPIO23", "MOSI"),
        ("GPIO19", "MISO"),
        ("GPIO5", "CS"),
    ],
    ("MCU", "Storage", "SPI"): [
        ("GPIO18", "SCK"),
        ("GPIO23", "MOSI"),
        ("GPIO19", "MISO"),
        ("GPIO5", "CS"),
    ],
    ("MCU", "Wireless", "SPI"): [
        ("GPIO18", "SCK"),
        ("GPIO23", "MOSI"),
        ("GPIO19", "MISO"),
        ("GPIO5", "CS"),
    ],

    # UART
    ("MCU", "Wireless", "UART"): [("GPIO16", "RX"), ("GPIO17", "TX")],
    ("MCU", "Interface", "UART"): [("GPIO16", "RX"), ("GPIO17", "TX")],

    # 1-Wire
    ("MCU", "Sensor", "1-Wire"): [("GPIO4", "DQ")],

    # Hall / GPIO
    ("MCU", "Sensor", "GPIO (open-collector)"): [("GPIO34", "OUT")],
    ("MCU", "Sensor", "GPIO"): [("GPIO26", "OUT")],

    # Power rules
    ("Power", "MCU", "POWER"): [("VOUT", "VIN")],
    ("Power", "Sensor", "POWER"): [("VOUT", "VCC")],
    ("Power", "Display", "POWER"): [("VOUT", "VCC")],
    ("Power", "Wireless", "POWER"): [("VOUT", "VCC")],
    ("Power", "Interface", "POWER"): [("VOUT", "VCC")],
    ("Power", "Storage", "POWER"): [("VOUT", "VCC")],
}

# Default power rail assignments
DEFAULT_VOLTAGE_MAP: dict[str, str] = {
    "ESP32": "3.3V",
    "STM32": "3.3V",
    "Arduino": "5V",
    "5V": "5V",
    "3.3V": "3.3V",
    "3.7V": "VBAT",
    "4.2V": "VBAT",
}

CONNECTION_PROMPT = """You are a hardware connectivity expert. Given a list of components,
suggest additional pin-to-pin connections beyond the standard bus wiring.

Consider:
- Power connections between power modules and consumers
- Any extra GPIO connections needed (chip-selects, reset lines, interrupts)
- Shared bus considerations (I2C addresses, SPI CS lines should be unique)

Reply with ONLY a JSON array of additional connections:
[
  {
    "from_component": "part_number",
    "from_pin": "pin name",
    "to_component": "part_number",
    "to_pin": "pin name",
    "protocol": "GPIO / POWER / I2C / etc."
  }
]

Return an empty array [] if no additional connections are needed."""


class SchematicAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="SchematicAgent", **kwargs)

    def run(self, components: list[Component]) -> Schematic:
        """Generate connection map between selected components."""
        connections: list[PinConnection] = []
        power_tree: dict[str, str] = {}
        notes: list[str] = []

        comp_map = {c.module_name: c for c in components}

        # ── 1. Rule-based pin mapping ─────────────────────────────
        mcu = _find_category(components, "MCU")
        power = _find_category(components, "Power")

        if mcu:
            for c in components:
                if c.part_number == mcu.part_number:
                    continue

                for iface in c.interfaces:
                    rule_key = (
                        mcu.category,
                        c.category,
                        iface,
                    )
                    pins = PIN_RULES.get(rule_key)
                    if pins:
                        for mcu_pin, target_pin in pins:
                            conn = PinConnection(
                                from_component=mcu.part_number,
                                from_pin=mcu_pin,
                                to_component=c.part_number,
                                to_pin=target_pin,
                                protocol=iface,
                            )
                            if not _connection_exists(connections, conn):
                                connections.append(conn)
                    else:
                        # Try partial match on protocol
                        for (from_cat, to_cat, proto), pins in PIN_RULES.items():
                            if (
                                from_cat == mcu.category
                                and to_cat == c.category
                                and proto in iface
                            ):
                                for mcu_pin, target_pin in pins:
                                    conn = PinConnection(
                                        from_component=mcu.part_number,
                                        from_pin=mcu_pin,
                                        to_component=c.part_number,
                                        to_pin=target_pin,
                                        protocol=proto,
                                    )
                                    if not _connection_exists(connections, conn):
                                        connections.append(conn)

        # ── 2. Power tree ─────────────────────────────────────────
        if power:
            for c in components:
                if c.part_number == power.part_number:
                    continue
                power_tree[c.part_number] = power.part_number

                conn = PinConnection(
                    from_component=power.part_number,
                    from_pin="VOUT",
                    to_component=c.part_number,
                    to_pin="VCC",
                    protocol="POWER",
                )
                if not _connection_exists(connections, conn):
                    connections.append(conn)

        # ── 3. LLM for additional / nuanced connections ───────────
        try:
            comp_summary = [
                {
                    "part_number": c.part_number,
                    "module": c.module_name,
                    "category": c.category,
                    "interfaces": c.interfaces,
                }
                for c in components
            ]
            extra = self.chat_json(
                CONNECTION_PROMPT,
                f"Components:\n{_json_str(comp_summary)}\n\nExisting connections:\n{_json_str([conn.model_dump() for conn in connections])}",
                temperature=0.1,
            )
            for e in extra:
                conn = PinConnection(**e)
                if not _connection_exists(connections, conn):
                    connections.append(conn)
        except Exception:
            pass

        # ── 4. Notes ──────────────────────────────────────────────
        i2c_modules = [c for c in components if "I2C" in c.interfaces]
        if len(i2c_modules) > 1:
            notes.append(
                f"Multiple I2C devices ({', '.join(c.part_number for c in i2c_modules)}). "
                "Verify no address conflicts. Consider adding TCA9548A I2C multiplexer if needed."
            )

        spi_modules = [c for c in components if "SPI" in c.interfaces]
        if len(spi_modules) > 2:
            notes.append(
                f"{len(spi_modules)} SPI devices connected. "
                "Ensure each device has a unique CS pin."
            )

        if not power:
            notes.append("No dedicated power management IC selected. Verify power requirements manually.")

        return Schematic(
            components=components,
            connections=connections,
            power_tree=power_tree,
            notes=notes,
        )


def _find_category(components: list[Component], category: str) -> Component | None:
    for c in components:
        if c.category.lower() == category.lower():
            return c
    return None


def _connection_exists(existing: list[PinConnection], new: PinConnection) -> bool:
    for e in existing:
        if (
            e.from_component == new.from_component
            and e.from_pin == new.from_pin
            and e.to_component == new.to_component
            and e.to_pin == new.to_pin
        ):
            return True
    return False


def _json_str(obj) -> str:
    import json

    return json.dumps(obj, ensure_ascii=False, indent=2)
