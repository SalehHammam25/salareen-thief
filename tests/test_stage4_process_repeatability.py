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
    assert run_probe() == run_probe() == {
        "request": 0,
        "response": 0,
        "text": "I kept moving near New York.",
    }
