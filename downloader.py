import asyncio
import os.path
from datetime import timedelta

import aiofiles
from aiohttp import ClientSession, ClientTimeout


async def download(db_code: str, base_dir: str) -> str:
    url = (
        f"https://www.ip2location.com/download/"
        f"?token=JpejrYyU90Ox0GWBDitDyVyxophoj6WNgnAWwfwPTtHkmqBJKdWm0Osmr1NJO3bP"
        f"&file={db_code}"
    )

    chunk_size = 1024 * 1024
    filename = os.path.join(base_dir, f"{db_code}.zip")

    fh = await aiofiles.open(file=filename, mode="wb")
    try:
        async with ClientSession(
            timeout=ClientTimeout(total=timedelta(minutes=60).seconds)
        ) as session:
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    async for chunk in resp.content.iter_chunked(chunk_size):
                        await fh.write(chunk)
    finally:
        await fh.close()

    return filename


async def main():

    ip_geo = "DB11LITECSV"
    ip_proxy = "PX11LITECSV"
    asn = "DBASNLITE"

    base_dir = "./temp"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    await asyncio.gather(
        download(db_code=ip_geo, base_dir=base_dir),
        download(db_code=ip_proxy, base_dir=base_dir),
        download(db_code=asn, base_dir=base_dir),
    )


if __name__ == "__main__":
    asyncio.run(main())
