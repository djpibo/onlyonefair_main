import httpx

async def pass_to_front(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/user", json=data.dict())
        print(response.text)
