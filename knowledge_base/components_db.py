"""Hardware component knowledge base.

Each entry stores key parameters used by ComponentAgent for matching.
In production this would be a vector database with RAG; here we use a
structured list as the v0.1 foundation.
"""

from __future__ import annotations

from typing import Any

# ── Component record format ──────────────────────────────────────────
# part_number: str
# category: MCU | Sensor | Display | Power | Wireless | Storage | Interface | Other
# description: str
# supply_voltage: str
# interfaces: list[str]
# package: str
# typical_applications: list[str]  (keywords for matching)
# datasheet_url: str | None

COMPONENT_DB: list[dict[str, Any]] = [
    # ═══════════════════════════════════════════════════════════════
    # MCUs / Development Boards
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "ESP32-WROOM-32E",
        "category": "MCU",
        "description": "Dual-core Xtensa LX6, WiFi b/g/n, Bluetooth 4.2 + BLE, 4MB Flash",
        "supply_voltage": "3.3V",
        "interfaces": ["GPIO", "I2C", "SPI", "UART", "ADC", "DAC", "I2S", "SDIO", "PWM"],
        "package": "QFN-48",
        "typical_applications": ["IoT", "WiFi", "Bluetooth", "MQTT", "low-power", "wearable", "smart-home"],
        "datasheet_url": "https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_datasheet_en.pdf",
    },
    {
        "part_number": "ESP32-S3-WROOM-1",
        "category": "MCU",
        "description": "Dual-core Xtensa LX7, WiFi b/g/n, BLE 5.0, AI acceleration, USB OTG",
        "supply_voltage": "3.3V",
        "interfaces": ["GPIO", "I2C", "SPI", "UART", "ADC", "USB", "I2S", "SDIO", "PWM"],
        "package": "QFN-56",
        "typical_applications": ["AI", "display", "TFT", "camera", "voice", "USB"],
        "datasheet_url": None,
    },
    {
        "part_number": "STM32F407VET6",
        "category": "MCU",
        "description": "ARM Cortex-M4F 168MHz, 512KB Flash, 192KB SRAM, FPU, DSP",
        "supply_voltage": "3.3V",
        "interfaces": ["GPIO", "I2C", "SPI", "UART", "ADC", "DAC", "USB", "CAN", "SDIO", "I2S"],
        "package": "LQFP-100",
        "typical_applications": ["industrial", "motor-control", "DSP", "real-time", "CAN"],
        "datasheet_url": None,
    },
    {
        "part_number": "STM32F103C8T6",
        "category": "MCU",
        "description": "ARM Cortex-M3 72MHz, 64KB Flash, 20KB SRAM (Blue Pill)",
        "supply_voltage": "3.3V",
        "interfaces": ["GPIO", "I2C", "SPI", "UART", "ADC", "USB", "CAN", "PWM"],
        "package": "LQFP-48",
        "typical_applications": ["general-purpose", "education", "low-cost", "DIY"],
        "datasheet_url": None,
    },
    {
        "part_number": "Arduino Nano (ATmega328P)",
        "category": "MCU",
        "description": "ATmega328P 16MHz, 32KB Flash, 2KB SRAM, 5V logic",
        "supply_voltage": "5V",
        "interfaces": ["GPIO", "I2C", "SPI", "UART", "ADC", "PWM"],
        "package": "DIP-30",
        "typical_applications": ["prototyping", "education", "simple-control", "DIY"],
        "datasheet_url": None,
    },
    {
        "part_number": "Raspberry Pi 4 Model B",
        "category": "MCU",
        "description": "Quad-core Cortex-A72 1.5GHz, 4GB RAM, Linux, HDMI, USB3, GPIO",
        "supply_voltage": "5V",
        "interfaces": ["GPIO", "I2C", "SPI", "UART", "USB", "HDMI", "Ethernet", "CSI", "DSI"],
        "package": "Module",
        "typical_applications": ["Linux", "computer-vision", "edge-computing", "multimedia"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Temperature / Humidity Sensors
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "DHT22 (AM2302)",
        "category": "Sensor",
        "description": "Digital temperature & humidity sensor, ±0.5°C, ±2% RH",
        "supply_voltage": "3.3V-5V",
        "interfaces": ["GPIO (one-wire)"],
        "package": "Through-hole",
        "typical_applications": ["temperature", "humidity", "weather", "environmental-monitoring"],
        "datasheet_url": None,
    },
    {
        "part_number": "SHT30-DIS",
        "category": "Sensor",
        "description": "High-accuracy I2C temperature & humidity sensor, ±0.3°C, ±2% RH",
        "supply_voltage": "2.4V-5.5V",
        "interfaces": ["I2C"],
        "package": "DFN-8",
        "typical_applications": ["temperature", "humidity", "precision", "industrial", "environmental-monitoring"],
        "datasheet_url": None,
    },
    {
        "part_number": "BME280",
        "category": "Sensor",
        "description": "I2C/SPI temperature, humidity & barometric pressure sensor",
        "supply_voltage": "1.7V-3.6V",
        "interfaces": ["I2C", "SPI"],
        "package": "LGA-8",
        "typical_applications": ["temperature", "humidity", "pressure", "altitude", "weather", "environmental-monitoring"],
        "datasheet_url": None,
    },
    {
        "part_number": "DS18B20",
        "category": "Sensor",
        "description": "1-Wire digital thermometer, ±0.5°C, -55°C to +125°C",
        "supply_voltage": "3.0V-5.5V",
        "interfaces": ["1-Wire"],
        "package": "TO-92",
        "typical_applications": ["temperature", "waterproof", "outdoor", "industrial"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Heart Rate / Biomedical Sensors
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "MAX30102",
        "category": "Sensor",
        "description": "I2C pulse oximeter & heart-rate sensor (IR + red LED + photodetector)",
        "supply_voltage": "1.8V/3.3V",
        "interfaces": ["I2C"],
        "package": "OLGA-14",
        "typical_applications": ["heart-rate", "pulse-oximeter", "SpO2", "wearable", "health"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Motion / IMU Sensors
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "MPU6050",
        "category": "Sensor",
        "description": "6-axis IMU: 3-axis gyroscope + 3-axis accelerometer, I2C",
        "supply_voltage": "3.3V-5V",
        "interfaces": ["I2C"],
        "package": "QFN-24",
        "typical_applications": ["motion", "gesture", "balance", "drone", "robot", "bicycle", "tilt"],
        "datasheet_url": None,
    },
    {
        "part_number": "ICM-20948",
        "category": "Sensor",
        "description": "9-axis IMU: gyro + accel + magnetometer, I2C/SPI",
        "supply_voltage": "1.7V-3.6V",
        "interfaces": ["I2C", "SPI"],
        "package": "QFN-24",
        "typical_applications": ["motion", "navigation", "drone", "robot", "AR"],
        "datasheet_url": None,
    },
    {
        "part_number": "A3144E",
        "category": "Sensor",
        "description": "Hall-effect switch, open-collector output, for speed/magnetic detection",
        "supply_voltage": "4.5V-24V",
        "interfaces": ["GPIO (open-collector)"],
        "package": "SIP-3",
        "typical_applications": ["hall", "speed", "magnetic", "rpm", "bicycle", "tachometer"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Displays
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "SSD1306 128x64 OLED",
        "category": "Display",
        "description": "128x64 monochrome OLED display, I2C/SPI, 0.96 inch",
        "supply_voltage": "3.3V",
        "interfaces": ["I2C", "SPI"],
        "package": "Module",
        "typical_applications": ["OLED", "small-display", "status", "text", "UI"],
        "datasheet_url": None,
    },
    {
        "part_number": "ILI9341 TFT 2.8inch",
        "category": "Display",
        "description": "240x320 color TFT LCD, SPI, 2.8 inch, with touch option",
        "supply_voltage": "3.3V",
        "interfaces": ["SPI"],
        "package": "Module",
        "typical_applications": ["TFT", "color-display", "GUI", "dashboard", "bicycle", "instrument"],
        "datasheet_url": None,
    },
    {
        "part_number": "ST7789 TFT 1.3inch",
        "category": "Display",
        "description": "240x240 color TFT LCD, SPI, 1.3 inch round",
        "supply_voltage": "3.3V",
        "interfaces": ["SPI"],
        "package": "Module",
        "typical_applications": ["TFT", "small-display", "wearable", "watch", "instrument"],
        "datasheet_url": None,
    },
    {
        "part_number": "LCD1602 I2C",
        "category": "Display",
        "description": "16x2 character LCD with I2C backpack",
        "supply_voltage": "5V",
        "interfaces": ["I2C"],
        "package": "Module",
        "typical_applications": ["character-display", "status", "debug", "text"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Power Management
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "AMS1117-3.3",
        "category": "Power",
        "description": "1A LDO voltage regulator, fixed 3.3V output",
        "supply_voltage": "4.75V-12V → 3.3V",
        "interfaces": ["POWER"],
        "package": "SOT-223",
        "typical_applications": ["power", "voltage-regulator", "3.3V", "LDO", "battery"],
        "datasheet_url": None,
    },
    {
        "part_number": "TP4056",
        "category": "Power",
        "description": "1A Li-Ion battery charger module with protection",
        "supply_voltage": "5V (USB) → 4.2V charge",
        "interfaces": ["POWER"],
        "package": "Module",
        "typical_applications": ["battery", "lithium", "charger", "Li-Ion", "power-management"],
        "datasheet_url": None,
    },
    {
        "part_number": "MT3608",
        "category": "Power",
        "description": "Boost converter, 2V-24V input, up to 28V output, 2A",
        "supply_voltage": "2V-24V input",
        "interfaces": ["POWER"],
        "package": "SOT-23-6",
        "typical_applications": ["boost", "battery", "power-conversion", "Li-Ion-to-5V"],
        "datasheet_url": None,
    },
    {
        "part_number": "IP5306",
        "category": "Power",
        "description": "Integrated power-bank SoC: charger + boost + fuel-gauge + button control",
        "supply_voltage": "5V (USB) → 3.7V charge / 5V boost",
        "interfaces": ["POWER", "I2C"],
        "package": "QFN-24",
        "typical_applications": ["power-bank", "battery", "lithium", "portable", "wearable"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Wireless Modules
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "SIM800L",
        "category": "Wireless",
        "description": "GSM/GPRS module, quad-band, UART AT commands",
        "supply_voltage": "3.7V-4.2V",
        "interfaces": ["UART"],
        "package": "Module",
        "typical_applications": ["GSM", "GPRS", "SMS", "cellular", "remote-monitoring"],
        "datasheet_url": None,
    },
    {
        "part_number": "SIM7600CE",
        "category": "Wireless",
        "description": "4G LTE Cat-1 module, GNSS, UART/USB",
        "supply_voltage": "3.3V-4.2V",
        "interfaces": ["UART", "USB"],
        "package": "Module",
        "typical_applications": ["4G", "LTE", "GNSS", "GPS", "remote-monitoring"],
        "datasheet_url": None,
    },
    {
        "part_number": "nRF24L01+",
        "category": "Wireless",
        "description": "2.4GHz transceiver, SPI, ultra-low-power, up to 100m range",
        "supply_voltage": "1.9V-3.6V",
        "interfaces": ["SPI"],
        "package": "Module",
        "typical_applications": ["wireless", "remote-control", "sensor-network", "low-power-radio"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Storage
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "W25Q32JV",
        "category": "Storage",
        "description": "32Mbit (4MB) SPI NOR Flash",
        "supply_voltage": "2.7V-3.6V",
        "interfaces": ["SPI"],
        "package": "SOIC-8",
        "typical_applications": ["flash", "storage", "data-logging", "firmware"],
        "datasheet_url": None,
    },
    {
        "part_number": "MicroSD SPI Module",
        "category": "Storage",
        "description": "MicroSD card slot with SPI interface, level-shifted for 3.3V/5V",
        "supply_voltage": "3.3V-5V",
        "interfaces": ["SPI"],
        "package": "Module",
        "typical_applications": ["SD-card", "storage", "data-logging", "logging"],
        "datasheet_url": None,
    },

    # ═══════════════════════════════════════════════════════════════
    # Interface / Other
    # ═══════════════════════════════════════════════════════════════
    {
        "part_number": "TCA9548A",
        "category": "Interface",
        "description": "8-channel I2C multiplexer, 1.65V-5.5V",
        "supply_voltage": "1.65V-5.5V",
        "interfaces": ["I2C"],
        "package": "TSSOP-24",
        "typical_applications": ["I2C", "multiplexer", "multi-sensor", "address-conflict"],
        "datasheet_url": None,
    },
    {
        "part_number": "TXB0108",
        "category": "Interface",
        "description": "8-bit bidirectional voltage-level translator, 1.2V-5.5V",
        "supply_voltage": "1.2V-5.5V",
        "interfaces": ["GPIO"],
        "package": "TSSOP-20",
        "typical_applications": ["level-shifter", "voltage-translation", "5V-to-3.3V"],
        "datasheet_url": None,
    },
    {
        "part_number": "CH340C",
        "category": "Interface",
        "description": "USB-to-UART bridge, built-in crystal, 3.3V/5V",
        "supply_voltage": "3.3V-5V",
        "interfaces": ["USB", "UART"],
        "package": "SOP-16",
        "typical_applications": ["USB-to-serial", "programming", "debug", "console"],
        "datasheet_url": None,
    },
    {
        "part_number": "NE555P",
        "category": "Other",
        "description": "Classic 555 timer IC, astable/monostable operation",
        "supply_voltage": "4.5V-16V",
        "interfaces": ["GPIO"],
        "package": "DIP-8",
        "typical_applications": ["timer", "oscillator", "PWM", "pulse-generation"],
        "datasheet_url": None,
    },
]


# ── Search helpers ──────────────────────────────────────────────────

def search_components(
    keywords: list[str] | None = None,
    category: str | None = None,
    interfaces: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Simple keyword + category + interface search over the component DB.

    In production this would be a vector similarity search (RAG).
    """
    results: list[dict[str, Any]] = []

    for comp in COMPONENT_DB:
        # Category filter
        if category and comp["category"].lower() != category.lower():
            continue

        # Interface filter (any match)
        if interfaces:
            comp_interfaces = [i.lower() for i in comp["interfaces"]]
            if not any(i.lower() in comp_interfaces for i in interfaces):
                continue

        # Keyword filter (match against description + typical_applications)
        if keywords:
            search_text = (
                comp["description"].lower()
                + " "
                + " ".join(comp["typical_applications"]).lower()
                + " "
                + comp["part_number"].lower()
            )
            if not any(kw.lower() in search_text for kw in keywords):
                continue

        results.append(comp)

    return results


def get_component_by_part_number(part_number: str) -> dict[str, Any] | None:
    for comp in COMPONENT_DB:
        if comp["part_number"].lower() == part_number.lower():
            return comp
    return None
