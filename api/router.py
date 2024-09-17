import httpx
from fastapi import APIRouter
from injector import Injector

from command import Commander
from config.inject_module import ChungMuro

injector = Injector([ChungMuro()])
commander = injector.get(Commander)

home_router = APIRouter()

@home_router.get("/nfc")
async def get_nfc_uid(nfc_uid: str):
    data = commander.start_card_polling(nfc_uid)
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/user", json=data.dict())
        print(response.text)  # 서버 응답을 텍스트로 출력

@home_router.get("/session")
async def get_session_info(company: str, enter: str):
    commander.set_session_info(company, enter)

@home_router.post("/user")
async def show_user_page(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/user", json=data.dict())
        print(response.text)  # 서버 응답을 텍스트로 출력

@home_router.post("/admin")
async def show_admin_page(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/admin", json=data.dict())
        return {"status": "Data sent", "response": response.json()}
