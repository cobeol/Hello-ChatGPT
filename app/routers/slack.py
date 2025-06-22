import random

from fastapi import APIRouter, Header, Request
from starlette.background import BackgroundTasks
from starlette.responses import Response

from app.config.constants import LLMModel, allowed_users
from app.services.slack import message_process

router = APIRouter()


def is_user_allowed(message: dict) -> bool:
    user_id = message.get("event", {}).get("user")
    return user_id and user_id in allowed_users


@router.post("/gpt")
async def slack(request: Request, message: dict, background_tasks: BackgroundTasks, headers=Header(default=None)):
    if message.get("challenge"):
        return message.get("challenge")

    if request.headers.get("x-slack-retry-num"):
        return Response("ok")
    
    if not is_user_allowed(message):
        return Response("ok")

    background_tasks.add_task(message_process, message, LLMModel.GPT)
    return Response("ok")


@router.post("/gemini")
async def slack(request: Request, message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")

    if request.headers.get("x-slack-retry-num"):
        return Response("ok")

    if not is_user_allowed(message):
        return Response("ok")

    background_tasks.add_task(message_process, message, LLMModel.GEMINI)
    return Response("ok")


@router.post("/claude")
async def slack(request: Request, message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")

    if request.headers.get("x-slack-retry-num"):
        return Response("ok")

    if not is_user_allowed(message):
        return Response("ok")

    background_tasks.add_task(message_process, message, LLMModel.CLAUDE)
    return Response("ok")


@router.post("/random")
async def slack(request: Request, message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")

    if request.headers.get("x-slack-retry-num"):
        return Response("ok")

    if not is_user_allowed(message):
        return Response("ok")

    llm_model = random.choice([LLMModel.GPT, LLMModel.GEMINI, LLMModel.CLAUDE])
    background_tasks.add_task(message_process, message, llm_model)
    return Response("ok")
