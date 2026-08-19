"""Fresh-process verbal fallback repeatability."""

import json
import subprocess
import sys


def run_probe() -> dict[str, object]:
    script = (
        "import asyncio,json;"
        "from salareen_thief.language.models import VerbalRequest;"
        "from salareen_thief.language.providers import TemplateProvider;"
        "r=asyncio.run(TemplateProvider().generate("
        "VerbalRequest('g',2,'New York','ignored')));"
        "print(json.dumps({'text':r.text,'request':r.request_tokens,"
        "'response':r.response_tokens},sort_keys=True))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_template_output_is_identical_in_fresh_processes() -> None:
    assert (
        run_probe()
        == run_probe()
        == {
            "request": 0,
            "response": 0,
            "text": "I kept moving near New York.",
        }
    )


def run_scent_probe() -> str:
    script = (
        "from salareen_thief.base_logic.state_types import Board,Coordinate;"
        "from salareen_thief.scent.field import emit,decay;"
        "f=decay(emit(Board(7,0,'top-left'),Coordinate(3,3)));"
        "print('|'.join(str(v) for row in f.values for v in row))"
    )
    return subprocess.run(
        [sys.executable, "-c", script], check=True, capture_output=True, text=True
    ).stdout


def test_exact_scent_is_identical_in_fresh_processes() -> None:
    assert run_scent_probe() == run_scent_probe()
