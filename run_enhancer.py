import json
import os
import sys
from pathlib import Path

from agent_utilities.security.persistence_privacy import sanitize_for_persistence

# Add scripts directory to path dynamically
scripts_dir_value = os.getenv("CODE_ENHANCER_SCRIPTS_DIR")
if not scripts_dir_value:
    raise SystemExit("CODE_ENHANCER_SCRIPTS_DIR must be configured")
sys.path.append(str(Path(scripts_dir_value).expanduser().resolve()))

from generate_report import generate_report
from generate_sdd_handoff import generate_sdd_handoff
from run_multi_project import _run_single_project

project_dir = str(Path(__file__).parent.resolve())
print("Running code-enhancer against langfuse-agent...")
result = _run_single_project(project_dir)
safe_result, _privacy_report = sanitize_for_persistence(result)

print("Writing results...")
workspace_dir = Path(__file__).parent.parent.parent.parent
output_dir = workspace_dir / "reports" / "code-enhancer-langfuse"
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "results.json").write_text(
    json.dumps(safe_result, indent=2), encoding="utf-8"
)

# Generate SDD handoff
print("Generating SDD handoff...")
generate_sdd_handoff(
    safe_result["domain_results"],
    project_name="langfuse-agent",
    output_dir=project_dir,
)

# Generate human-readable report
try:
    print("Generating human-readable report...")
    report_content = generate_report(
        safe_result["domain_results"],
        project_name=safe_result["project"],
        output_path=str(output_dir / "code_enhancement_report.md"),
    )
except Exception as e:
    print(f"Operation failed: {type(e).__name__}")

print("Done! Graded GPA:", safe_result["gpa"])
