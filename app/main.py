import logging
import os
from dotenv import load_dotenv
load_dotenv()  # ✅ .env 파일 불러오기!

import uvicorn
from fastapi import FastAPI
from starlette.responses import Response
from app.routers import chatgpt, slack
from app.internal import admin

# ✅ 항상 FastAPI 문서 접근 가능하게 설정
app = FastAPI()

# 라우터 등록
app.include_router(chatgpt.router, prefix="/openai", tags=["openai"])
app.include_router(slack.router, prefix="/slack", tags=["slack"])
app.include_router(admin.router, prefix="/admin", tags=["admin"], responses={418: {"description": "I'm a teapot"}})

# 로그 설정
logging.basicConfig(level=logging.INFO)

# 루트 테스트
@app.get("/")
async def root():
    return Response("Hello ChatGPT Applications!")

# 서버 실행
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        access_log=False,
        reload=True,
        timeout_keep_alive=65,
    )
