"""CircuitAgent v0.1 — AI-powered hardware design system.

Pipeline:
    Natural Language → RequirementAgent → ComponentAgent → SchematicAgent → BOM + Schematic

Usage:
    python main.py
"""

from __future__ import annotations

import json
import sys

from agents.requirement_agent import RequirementAgent
from agents.component_agent import ComponentAgent
from agents.schematic_agent import SchematicAgent
from models.schemas import BOM, BOMEntry, DesignOutput


def generate_bom(components, schematic) -> BOM:
    """Generate a BOM from selected components and schematic connections."""
    entries: list[BOMEntry] = []
    for i, comp in enumerate(components, start=1):
        # Count how many times this part appears in schematic
        qty = sum(
            1
            for conn in schematic.connections
            if comp.part_number in (conn.from_component, conn.to_component)
        )
        qty = max(qty, 1)  # At least 1

        # Determine reference prefix
        ref_prefix_map = {
            "MCU": "U",
            "Sensor": "U",
            "Display": "U",
            "Power": "U",
            "Wireless": "U",
            "Interface": "U",
            "Storage": "U",
            "Other": "U",
        }
        prefix = ref_prefix_map.get(comp.category, "U")

        entries.append(
            BOMEntry(
                index=i,
                part_number=comp.part_number,
                description=f"{comp.category} — {comp.package}",
                quantity=qty,
                package=comp.package,
                reference=f"{prefix}{i}",
            )
        )

    return BOM(entries=entries, total_unique_parts=len(entries))


def format_output(output: DesignOutput) -> str:
    """Pretty-print the design output for the terminal."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  CircuitAgent Design Output")
    lines.append(f"  Project: {output.requirement.project_name}")
    lines.append("=" * 60)

    # ── Modules ──
    lines.append(f"\n📐 Functional Modules ({len(output.requirement.modules)}):")
    for mod in output.requirement.modules:
        lines.append(f"  • {mod.name}: {mod.description}")
        if mod.interfaces:
            lines.append(f"    interfaces: {', '.join(mod.interfaces)}")
        if mod.constraints:
            lines.append(f"    constraints: {', '.join(mod.constraints)}")

    # ── Components ──
    lines.append(f"\n🔌 Selected Components ({len(output.components)}):")
    for comp in output.components:
        lines.append(f"  • [{comp.module_name}] {comp.part_number}")
        lines.append(f"    package: {comp.package}  |  voltage: {comp.supply_voltage}")
        lines.append(f"    reason: {comp.reason}")

    # ── Connections ──
    lines.append(f"\n🔗 Connections ({len(output.schematic.connections)}):")
    for conn in output.schematic.connections:
        lines.append(
            f"  {conn.from_component}:{conn.from_pin}"
            f"  ──[{conn.protocol}]──▶"
            f"  {conn.to_component}:{conn.to_pin}"
        )

    # ── Power Tree ──
    if output.schematic.power_tree:
        lines.append(f"\n⚡ Power Tree:")
        for comp, source in output.schematic.power_tree.items():
            lines.append(f"  {comp} ← {source}")

    # ── BOM ──
    lines.append(f"\n📦 Bill of Materials ({output.bom.total_unique_parts} unique parts):")
    lines.append(f"  {'#':<4} {'Part Number':<28} {'Qty':<5} {'Package':<14} {'Ref':<5}")
    lines.append(f"  {'-'*4} {'-'*28} {'-'*5} {'-'*14} {'-'*5}")
    for e in output.bom.entries:
        lines.append(f"  {e.index:<4} {e.part_number:<28} {e.quantity:<5} {e.package:<14} {e.reference:<5}")

    # ── Notes / Warnings ──
    if output.schematic.notes:
        lines.append(f"\n📝 Notes:")
        for note in output.schematic.notes:
            lines.append(f"  ⚠  {note}")
    if output.warnings:
        lines.append(f"\n⚠ Warnings:")
        for w in output.warnings:
            lines.append(f"  ⚠  {w}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def run_pipeline(requirement_text: str) -> DesignOutput:
    """Execute the full CircuitAgent pipeline."""
    print(f"\n🔍 Parsing requirement...")
    req_agent = RequirementAgent()
    requirement = req_agent.run(requirement_text)
    print(f"   → Found {len(requirement.modules)} functional modules")

    print(f"\n🧩 Selecting components...")
    comp_agent = ComponentAgent()
    components = comp_agent.run(requirement.modules)
    print(f"   → Selected {len(components)} components")

    print(f"\n🔗 Generating schematic connections...")
    sch_agent = SchematicAgent()
    schematic = sch_agent.run(components)
    print(f"   → Generated {len(schematic.connections)} connections")

    print(f"\n📦 Building BOM...")
    bom = generate_bom(components, schematic)
    print(f"   → {bom.total_unique_parts} unique parts")

    return DesignOutput(
        requirement=requirement,
        components=components,
        schematic=schematic,
        bom=bom,
    )


def main():
    """CLI entry point."""

    # Default example to demonstrate the pipeline
    default_requirement = """设计一个基于ESP32的智能自行车仪表，
包含：
- TFT 显示
- 霍尔测速
- MAX30102 心率检测
- MQTT 上传
- 锂电池供电"""

    print("╔══════════════════════════════════════════════════════╗")
    print("║         CircuitAgent v0.1 — AI Hardware Design       ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("输入你的硬件需求（自然语言），或直接回车使用示例需求：")
    print()

    user_input = input("> ").strip()
    if not user_input:
        user_input = default_requirement
        print(f"\n使用示例需求:\n{user_input}\n")

    try:
        output = run_pipeline(user_input)
        print(format_output(output))

        # Also save as JSON
        json_path = "design_output.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output.model_dump(), f, ensure_ascii=False, indent=2, default=str)
        print(f"\n💾 完整设计输出已保存到 {json_path}")
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        print("请确保已设置环境变量 CIRCUITAGENT_API_KEY", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
