import requests
from typing import Tuple, Optional

def fact_check(query: str) -> Tuple[str, Optional[str]]:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query.strip())}"
        response = requests.get(url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            extract = data.get('extract', '')[:500]
            source = data.get('content_urls', {}).get('desktop', {}).get('page', '')
            return f"📚 {data.get('title', '')}: {extract}", source
        elif response.status_code == 404:
            return f"No Wikipedia article found for '{query}'.", None
        else:
            return f"Error accessing Wikipedia (Status: {response.status_code})", None
    except Exception as e:
        return f"Error: {str(e)}", None