# fetcher.py
import aiohttp

#API_KEY = os.getenv("API_KEY", "sk_1CGTBce5Y1pxv5mF5YvCuvWhE0qxOb_qWw8wIcowWQY")
URL = "https://transcriptapi.com/api/v2/youtube/transcript"


async def get_transcript(video_url: str,api):
    params = {
        "video_url": video_url,
        "format": "json",
    }

    headers = {
        "Authorization": f"Bearer {api}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params, headers=headers, timeout=30) as resp: # type: ignore
            resp.raise_for_status()
            data = await resp.json()
            return data["transcript"]



