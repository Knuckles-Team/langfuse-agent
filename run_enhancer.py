import json
import sys
from pathlib import Path

# Add scripts directory to path dynamically
sys.path.append(
    str(
        Path.home() / ".gemini" / "antigravity" / "skills" / "code-enhancer" / "scripts"
    )
)

from generate_report import generate_report
from generate_sdd_handoff import generate_sdd_handoff
from run_multi_project import _run_single_project

project_dir = str(Path(__file__).parent.resolve())
print("Running code-enhancer against langfuse-agent...")
result = _run_single_project(project_dir)

print("Writing results...")
workspace_dir = Path(__file__).parent.parent.parent.parent
output_dir = workspace_dir / "reports" / "code-enhancer-langfuse"
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

# Generate SDD handoff
print("Generating SDD handoff...")
generate_sdd_handoff(
    result["domain_results"],
    project_name="langfuse-agent",
    output_dir=project_dir,
)

# Generate human-readable report
try:
    print("Generating human-readable report...")
    report_content = generate_report(
        result["domain_results"],
        project_name=result["project"],
        output_path=str(output_dir / "code_enhancement_report.md"),
    )
except Exception as e:
    print(f"Failed to generate human report: {e}")

print("Done! Graded GPA:", result["gpa"])
