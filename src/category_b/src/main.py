import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.router import pages_router

app = FastAPI(
    docs_url='/docs',
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=['*'],
        )
    ]
)

app.include_router(pages_router, tags=['pages'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8083)
