"""Command line: one document in, one document out.

    zyfenutri batch.yml               # YAML on stdout
    zyfenutri batch.yml --json
    cat batch.yml | zyfenutri
    zyfenutri batch.yml -o sheet.yml

No server, no port, no HTTP. A process, standard input, standard output — the
decoupling is the operating system's, which is both the simplest and the most
robust. The caller need not even share our Python interpreter.

Exit codes: 0 done, 2 the document could not be read.
"""
import argparse
import json
import sys
from pathlib import Path

from zyfenutri import __version__, compute


def _load(text: str) -> dict:
    """Read YAML if PyYAML is around, JSON otherwise. JSON is valid YAML, so
    a JSON document always works either way."""
    try:
        import yaml
        return yaml.safe_load(text) or {}
    except ImportError:
        return json.loads(text)


def _dump(data: dict, as_json: bool) -> str:
    if not as_json:
        try:
            import yaml
            return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)
        except ImportError:
            pass
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zyfenutri",
        description="Composition nutritionnelle d'un lot de tempeh.")
    parser.add_argument("document", nargs="?",
                        help="fichier YAML ou JSON (défaut : entrée standard)")
    parser.add_argument("-o", "--output", help="écrire le résultat dans ce fichier")
    parser.add_argument("--json", action="store_true", help="sortie JSON plutôt que YAML")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    text = Path(args.document).read_text(encoding="utf-8") if args.document else sys.stdin.read()
    try:
        document = _load(text)
    except Exception as exc:                        # noqa: BLE001 - any parser error
        print(f"document illisible : {exc}", file=sys.stderr)
        return 2
    if not isinstance(document, dict):
        print("le document doit être un objet (une liste de clés)", file=sys.stderr)
        return 2

    rendu = _dump(compute(document), args.json)
    if args.output:
        Path(args.output).write_text(rendu, encoding="utf-8")
    else:
        sys.stdout.write(rendu)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
