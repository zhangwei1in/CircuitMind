"""CircuitAgent FastAPI backend — REST API for the hardware design pipeline."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from main import run_pipeline

app = FastAPI(
    title="CircuitAgent API",
    description="AI-powered hardware design system — v0.1",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DesignRequest(BaseModel):
    requirement: str = Field(
        description="Natural language hardware requirement",
        examples=["设计一个基于ESP32的环境监测系统，包含温湿度传感器、OLED显示、WiFi上传"],
    )


class DesignResponse(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.post("/api/v1/design", response_model=DesignResponse)
async def create_design(request: DesignRequest):
    """Submit a natural-language hardware requirement and get a complete design back."""
    try:
        output = run_pipeline(request.requirement)
        return DesignResponse(success=True, data=output.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
