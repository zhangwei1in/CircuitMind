from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class FunctionalModule(BaseModel):
    """A functional block parsed from the user requirement."""

    name: str = Field(description="Module name, e.g. 'MCU', 'Display', 'Power'")
    description: str = Field(description="What this module does")
    interfaces: list[str] = Field(
        default_factory=list,
        description="Required interfaces, e.g. ['I2C', 'SPI', 'GPIO']",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Constraints, e.g. '3.3V', 'low-power', 'small-form-factor'",
    )


class Requirement(BaseModel):
    """Structured requirement output from RequirementAgent."""

    project_name: str = Field(description="Inferred project name")
    description: str = Field(description="Original requirement summary")
    modules: list[FunctionalModule] = Field(description="Decomposed functional modules")


class Component(BaseModel):
    """A specific component selected by ComponentAgent."""

    module_name: str = Field(description="Which functional module this belongs to")
    part_number: str = Field(description="Specific part number, e.g. 'ESP32-WROOM-32E'")
    category: str = Field(description="Category: MCU / Sensor / Display / Power / etc.")
    package: str = Field(description="Package type, e.g. 'QFN-48', 'SOP-8'")
    supply_voltage: str = Field(description="Operating voltage, e.g. '3.3V'")
    interfaces: list[str] = Field(description="Available interfaces on this component")
    reason: str = Field(description="Why this component was selected")
    datasheet_url: Optional[str] = Field(default=None)


class PinConnection(BaseModel):
    """A connection between two component pins."""

    from_component: str
    from_pin: str
    to_component: str
    to_pin: str
    protocol: str = Field(description="e.g. 'I2C', 'SPI', 'UART', 'GPIO', 'POWER'")


class Schematic(BaseModel):
    """Schematic structure output from SchematicAgent."""

    components: list[Component]
    connections: list[PinConnection]
    power_tree: dict[str, str] = Field(
        default_factory=dict,
        description="Power supply mapping: component → voltage rail",
    )
    notes: list[str] = Field(default_factory=list)


class BOMEntry(BaseModel):
    """A single line in the Bill of Materials."""

    index: int
    part_number: str
    description: str
    quantity: int
    package: str
    reference: str = Field(description="Designator prefix, e.g. 'U1', 'R1', 'C1'")


class BOM(BaseModel):
    """Bill of Materials."""

    entries: list[BOMEntry]
    total_unique_parts: int
    estimated_cost_note: str = Field(default="")


class DesignOutput(BaseModel):
    """Final output from the CircuitAgent pipeline."""

    requirement: Requirement
    components: list[Component]
    schematic: Schematic
    bom: BOM
    warnings: list[str] = Field(default_factory=list)
