"""ComponentAgent — selects specific part numbers for each functional module.

Uses a hybrid approach:
1. Search the local knowledge base for matching components
2. Use LLM reasoning to pick the best candidate per module

This is step 2 of the CircuitAgent pipeline.
"""

from __future__ import annotations

import json

from agents.base_agent import BaseAgent
from knowledge_base.components_db import COMPONENT_DB, search_components
from models.schemas import Component, FunctionalModule

SELECTION_PROMPT = """You are a hardware component selection expert. Given a functional module
description and a list of candidate components, select the BEST component for the module.

Consider:
- Interface compatibility (does the component have the required interfaces?)
- Voltage compatibility
- Application fit (is this component commonly used for this purpose?)
- Availability and popularity

Reply with ONLY a JSON object:
{
  "part_number": "EXACT-PART-NUMBER from candidates",
  "reason": "one sentence explaining why this is the best choice"
}"""


class ComponentAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="ComponentAgent", **kwargs)

    def run(self, modules: list[FunctionalModule]) -> list[Component]:
        """Select one component per functional module."""
        selected: list[Component] = []

        for module in modules:
            # ── 1. Search knowledge base ──────────────────────────
            keywords = [module.name, module.description] + module.interfaces
            kb_results = search_components(keywords=keywords)

            # Also try by category matching
            category_map = {
                "MCU": "MCU",
                "Sensor": "Sensor",
                "Display": "Display",
                "Power": "Power",
                "Storage": "Storage",
                "Wireless": "Wireless",
                "Interface": "Interface",
            }
            matched_category = None
            for key, cat in category_map.items():
                if key.lower() in module.name.lower() or key.lower() in module.description.lower():
                    matched_category = cat
                    break

            if matched_category and not kb_results:
                kb_results = search_components(category=matched_category)

            # Also try interface-based search
            if not kb_results and module.interfaces:
                kb_results = search_components(interfaces=module.interfaces)

            # Fallback: search across entire DB with module name
            if not kb_results:
                kb_results = search_components(keywords=[module.name])

            # ── 2. LLM selection ──────────────────────────────────
            if kb_results:
                candidates_text = json.dumps(
                    [
                        {
                            "part_number": c["part_number"],
                            "description": c["description"],
                            "package": c["package"],
                            "supply_voltage": c["supply_voltage"],
                            "interfaces": c["interfaces"],
                        }
                        for c in kb_results[:8]
                    ],
                    ensure_ascii=False,
                    indent=2,
                )

                user_msg = f"""Module:
  name: {module.name}
  description: {module.description}
  required interfaces: {module.interfaces or 'none specified'}
  constraints: {module.constraints or 'none specified'}

Candidates:
{candidates_text}"""

                result = self.chat_json(SELECTION_PROMPT, user_msg, temperature=0.1)
                part_number = result["part_number"]
                reason = result.get("reason", "")

                # Look up full component record
                comp = _lookup(part_number)
                if comp:
                    selected.append(
                        Component(
                            module_name=module.name,
                            part_number=comp["part_number"],
                            category=comp["category"],
                            package=comp["package"],
                            supply_voltage=comp["supply_voltage"],
                            interfaces=comp["interfaces"],
                            reason=reason,
                            datasheet_url=comp.get("datasheet_url"),
                        )
                    )
                    continue

            # ── 3. No match — LLM suggests a generic part ─────────
            fallback = Component(
                module_name=module.name,
                part_number="TBD",
                category="Other",
                package="TBD",
                supply_voltage="TBD",
                interfaces=module.interfaces,
                reason="No match in knowledge base — needs manual selection",
            )
            selected.append(fallback)

        return selected


def _lookup(part_number: str) -> dict | None:
    """Find a component in the knowledge base by exact or partial match."""
    for c in COMPONENT_DB:
        if c["part_number"].lower() == part_number.lower():
            return c
    # Partial match
    for c in COMPONENT_DB:
        if part_number.lower() in c["part_number"].lower():
            return c
    return None
