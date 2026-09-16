"""The command line: a document in, a document out."""
import json
import subprocess
import sys
from pathlib import Path

DOCUMENT = {
    "recipe": "Tempeh de soja nature",
    "harvested_g": 1750,
    "ingredients": [{
        "name": "Soja", "role": "substrate", "weight_g": 1000,
        "per_100g": {"fat": 20, "saturates": 2.9, "carbs": 15, "sugars": 5.7,
                     "fibre": 15, "protein": 40, "salt": 0.01},
    }],
}


def run(args, stdin=""):
    return subprocess.run([sys.executable, "-m", "zyfenutri", *args],
                          input=stdin, capture_output=True, text=True,
                          cwd=Path(__file__).resolve().parents[1])


def test_json_goes_in_and_a_document_comes_out():
    """JSON is valid YAML, so a JSON document works with or without PyYAML."""
    proc = run(["--json"], json.dumps(DOCUMENT))
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["label"]["energy"] == "876 kJ / 210 kcal"
    assert result["complete"] is True


def test_a_file_works_as_well_as_a_pipe(tmp_path):
    path = tmp_path / "lot.json"
    path.write_text(json.dumps(DOCUMENT), encoding="utf-8")
    piped = json.loads(run(["--json"], json.dumps(DOCUMENT)).stdout)
    from_file = json.loads(run([str(path), "--json"]).stdout)
    assert piped == from_file


def test_it_can_write_to_a_file(tmp_path):
    out = tmp_path / "sheet.json"
    assert run(["--json", "-o", str(out)], json.dumps(DOCUMENT)).returncode == 0
    assert json.loads(out.read_text(encoding="utf-8"))["complete"] is True


def test_an_unreadable_document_exits_two_and_says_so():
    """Exit code 2 and a message on stderr: the caller must be able to tell a
    broken document from a computed one."""
    proc = run(["--json"], "{ not a document")
    assert proc.returncode == 2
    assert "illisible" in proc.stderr
