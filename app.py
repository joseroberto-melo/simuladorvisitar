import httpx
import asyncio
import random

proxies = [
    "http://usuario:senha@proxy1:porta",
    "http://usuario:senha@proxy2:porta",
    # ... lista de proxies rotativos
]

url = "https://seusite.onrender.com/"

async def acessar(proxy):
    try:
        async with httpx.AsyncClient(proxies={"http://": proxy, "https://": proxy}, timeout=10) as client:
            r = await client.get(url)
            print(f"{proxy} -> {r.status_code}")
    except Exception as e:
        print(f"{proxy} -> ERRO: {e}")

async def main():
    tasks = [acessar(random.choice(proxies)) for _ in range(100)]
    await asyncio.gather(*tasks)

asyncio.run(main())
