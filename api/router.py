import httpx
from fastapi import APIRouter, Depends
from injector import Injector

from command import Commander
from config.inject_module import ChungMuro
from service.common_service import CommonMgr

injector = Injector([ChungMuro()])
commander = injector.get(Commander)

home_router = APIRouter()

@home_router.get("/peer_id")
async def get_nfc_uid(_id: str):
    if _id is not None:
        await commander.wnt_to(_id)

@home_router.get("/session")
async def get_session_info(company: str, enter: str):
    commander.set_session_info(company, enter)

@home_router.post("/user")
async def show_user_page(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/user", json=data.dict())
        print(response.text)

@home_router.post("/admin")
async def show_admin_page(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/admin", json=data.dict())
        return {"status": "Data sent", "response": response.json()}
