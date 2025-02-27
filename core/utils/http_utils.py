import httpx
import asyncio

async def send_request(url, method='GET', params=None, data=None, headers=None, timeout=10):
    if headers is None:
        headers = {
            'User-Agent': 'SecureSync-Scanner/1.0'
        }
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response
    except httpx.RequestError as e:
        raise ConnectionError(f"Error connecting to {url}: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise TimeoutError(f"Request to {url} failed with status {e.response.status_code}")