from fastapi import FastAPI
from app.routers.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HyperCLOVA X Chat API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ★ 모든 Origin(IP·포트·프로토콜)을 허용
    allow_methods=["*"],      # GET·POST·PUT … 전부 허용
    allow_headers=["*"],      # 모든 헤더 허용
    allow_credentials=False,  # 쿠키·Authorization 헤더를 쓰지 않을 경우
)

app.include_router(chat_router)
