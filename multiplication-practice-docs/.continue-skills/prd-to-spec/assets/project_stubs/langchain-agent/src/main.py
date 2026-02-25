"""Main Entrypoint for the agent"""

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from llm import ResponseModel, RequestBody

app = FastAPI()


@app.post("/agent")
async def run_agent(body: RequestBody) -> ResponseModel:
    pass


# ---- Static frontend ----
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
