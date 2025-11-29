import aiohttp

#! API endpoint for YouTube transcript service
URL = "https://transcriptapi.com/api/v2/youtube/transcript"

async def get_transcript(video_url: str, api):
    """
    #! Fetch YouTube video transcript asynchronously
    #? Makes authorized API request and returns transcript data
    """
    #? Prepare request parameters
    params = {
        "video_url": video_url,
        "format": "json",
    }
    
    #! Set authorization header with API key
    headers = {
        "Authorization": f"Bearer {api}",
    }
    
    #? Create async HTTP session
    async with aiohttp.ClientSession() as session:
        #! Send GET request to transcript API
        async with session.get(URL, params=params, headers=headers, timeout=30) as resp: # type: ignore
            #? Raise exception if request fails
            resp.raise_for_status()
            #! Parse JSON response
            data = await resp.json()
            #? Extract and return transcript data
            return data["transcript"]