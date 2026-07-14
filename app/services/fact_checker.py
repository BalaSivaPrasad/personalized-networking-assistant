import requests
from typing import Tuple, Optional

def fact_check(query: str) -> Tuple[str, Optional[str]]:
    """
    Fact check a query and return corrected information with supporting facts.
    """
    try:
        clean_query = query.strip()
        
        # Search Wikipedia for the topic
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={requests.utils.quote(clean_query)}&limit=3&format=json"
        search_response = requests.get(search_url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
        
        if search_response.status_code != 200:
            return "Unable to verify this statement. Please check your internet connection.", None
        
        search_data = search_response.json()
        
        if not search_data[1]:
            return f"❌ No information found for '{query}'. This statement may be incorrect or unverified.", None
        
        # Get the best matching article
        best_match = search_data[1][0]
        
        # Get detailed summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_match)}"
        summary_response = requests.get(summary_url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
        
        if summary_response.status_code != 200:
            return f"Unable to retrieve details for '{best_match}'.", None
        
        summary_data = summary_response.json()
        title = summary_data.get('title', best_match)
        extract = summary_data.get('extract', '')
        source_url = summary_data.get('content_urls', {}).get('desktop', {}).get('page', '')
        
        # Build response
        result_parts = []
        result_parts.append(f"📚 **{title}**")
        result_parts.append("")
        result_parts.append("🔍 **Verification Result:**")
        result_parts.append(f"✅ Information found and verified from Wikipedia.")
        result_parts.append("")
        result_parts.append("📋 **Supporting Information:**")
        
        if len(extract) > 800:
            sentences = extract.replace('. ', '.|').split('|')
            query_keywords = [word.lower() for word in clean_query.split() if len(word) > 3]
            relevant_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in query_keywords):
                    relevant_sentences.append(sentence.strip())
            
            if relevant_sentences:
                extract = '. '.join(relevant_sentences[:3]) + '.'
            else:
                extract = extract[:800] + "..."
        
        result_parts.append(extract)
        result_parts.append("")
        
        if len(search_data[1]) > 1:
            result_parts.append("📌 **Related Topics:**")
            for related in search_data[1][1:3]:
                if related != best_match:
                    result_parts.append(f"• {related}")
        
        result = "\n".join(result_parts)
        return result, source_url
        
    except requests.exceptions.Timeout:
        return "⚠️ Wikipedia API request timed out. Please try again.", None
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to Wikipedia. Please check your internet connection.", None
    except Exception as e:
        return f"❌ Error verifying statement: {str(e)}", None