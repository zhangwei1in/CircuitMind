"""RequirementAgent — parses natural language into structured functional modules.

This is step 1 of the CircuitAgent pipeline.
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from models.schemas import FunctionalModule, Requirement

SYSTEM_PROMPT = """You are a hardware system architect. Your job is to decompose a natural-language
hardware requirement into a list of functional modules.

For each module provide:
- name: short module name (e.g. "MCU", "Temperature Sensor", "Display", "Power Management")
- description: what this module does in this specific design
- interfaces: required electrical interfaces (I2C, SPI, UART, GPIO, ADC, PWM, POWER, 1-Wire, etc.)
- constraints: any special requirements (voltage, power budget, form factor, environmental)

Rules:
- Always identify the MCU / main controller first
- Include a power-supply / power-management module
- Group related functions together (e.g. "Environmental Sensing" for temp + humidity + pressure)
- Think about what buses and protocols connect each module to the MCU

Reply with ONLY a JSON object in this exact shape:
{
  "project_name": "inferred project name",
  "description": "one-sentence summary",
  "modules": [
    {
      "name": "MCU",
      "description": "...",
      "interfaces": [...],
      "constraints": [...]
    }
  ]
}"""


class RequirementAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="RequirementAgent", **kwargs)

    def run(self, requirement_text: str) -> Requirement:
        result = self.chat_json(SYSTEM_PROMPT, requirement_text, temperature=0.2)
        modules = [FunctionalModule(**m) for m in result["modules"]]
        return Requirement(
            project_name=result["project_name"],
            description=result["description"],
            modules=modules,
        )
