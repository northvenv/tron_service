import uvicorn
from fastapi import FastAPI

from app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="Tron Service")
    app.include_router(router=router)

    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", host="0.0.0.0", port=8080, reload=True)