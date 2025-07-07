from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from devlab.dev_engine import DevEngine
from devlab.utils import detect_externally_managed_python

app = FastAPI()

# Serve the minimal UI bundled in devlab/ui
_UI_DIR = Path(__file__).resolve().parent / "ui"
app.mount("/", StaticFiles(directory=_UI_DIR), name="static")


@app.post("/ask")
async def ask(prompt: str) -> dict[str, str]:
    """Run the DevEngine with *prompt* and return the result."""
    engine = DevEngine()
    result = engine.run(prompt)
    return {"response": result}


@app.get("/export_memory")
async def export_memory() -> FileResponse:
    """Create a ZIP archive of the memory directory and return it."""
    engine = DevEngine()
    path = engine.export_memory()
    return FileResponse(path, filename=path.name)


@app.get("/export_knowledge")
async def export_knowledge() -> FileResponse:
    """Export the knowledge database as a JSON file and return it."""
    engine = DevEngine()
    path = engine.export_knowledge()
    return FileResponse(path, filename=path.name)


def main() -> None:
    """Entry point for the ``devlab-server`` console script."""
    if detect_externally_managed_python():
        print(
            "Error: detected externally managed Python installation. "
            "Create and activate a virtual environment or run ./devlab_venv.sh.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    import uvicorn

    uvicorn.run("devlab.app:app")


if __name__ == "__main__":
    main()
