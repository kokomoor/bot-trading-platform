"""Minimal API service entrypoint placeholder."""

from fastapi import FastAPI

app = FastAPI(title="bot-trading-platform", version="0.1.0")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


def run() -> None:
    """CLI entrypoint placeholder for API service."""
    import uvicorn

    uvicorn.run("app.services.api.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
