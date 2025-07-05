from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from DevLab.dev_engine import DevEngine

app = FastAPI()

# Serve the minimal UI bundled in DevLab/ui
_UI_DIR = Path(__file__).resolve().parent.parent / "DevLab" / "ui"
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
    import uvicorn

    uvicorn.run("src.app:app")


if __name__ == "__main__":
    main()
