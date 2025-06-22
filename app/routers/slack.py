import random
from fastapi import APIRouter, Header, Request
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse, Response

from app.config.constants import LLMModel
from app.services.slack import message_process

router = APIRouter()

# 👇 여기에 봇의 Slack 유저 ID를 설정 (auth.test 로 얻은 값)
BOT_USER_ID = "U092APUA1FS"

# ✅ Slack Event Verification 엔드포인트 (challenge 응답 + 메시지 핸들링)
@router.post("/chat")
async def slack_event(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    # Slack challenge 인증 응답
    if "challenge" in body:
        return JSONResponse(content={"challenge": body["challenge"]})

    event = body.get("event", {})
    event_type = event.get("type")
    text = event.get("text", "")

    # 봇이 맨션된 app_mention or 일반 message 처리
    if event_type in ["app_mention", "message"] and f"<@{BOT_USER_ID}>" in text:
        background_tasks.add_task(message_process, body, LLMModel.GPT)

    return Response("OK")


# 👇 이하 모델별 수동 테스트용 엔드포인트들 (건들 필요 없음)
@router.post("/gpt")
async def slack_gpt(request: Request, message: dict, background_tasks: BackgroundTasks, headers=Header(default=None)):
    if message.get("challenge"):
        return message.get("challenge")
    if request.headers.get("x-slack-retry-num") and request.headers.get("x-slack-retry-reason") == "http_timeout":
        return Response("ok")
    background_tasks.add_task(message_process, message, LLMModel.GPT)
    return Response("ok")

@router.post("/gemini")
async def slack_gemini(request: Request, message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")
    if request.headers.get("x-slack-retry-num") and request.headers.get("x-slack-retry-reason") == "http_timeout":
        return Response("ok")
    background_tasks.add_task(message_process, message, LLMModel.GEMINI)
    return Response("ok")

@router.post("/claude")
async def slack_claude(request: Request, message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")
    if request.headers.get("x-slack-retry-num") and request.headers.get("x-slack-retry-reason") == "http_timeout":
        return Response("ok")
    background_tasks.add_task(message_process, message, LLMModel.CLAUDE)
    return Response("ok")

@router.post("/random")
async def slack_random(request: Request, message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")
    if request.headers.get("x-slack-retry-num") and request.headers.get("x-slack-retry-reason") == "http_timeout":
        return Response("ok")
    llm_model = random.choice([LLMModel.GPT, LLMModel.GEMINI, LLMModel.CLAUDE])
    background_tasks.add_task(message_process, message, llm_model)
    return Response("ok")
