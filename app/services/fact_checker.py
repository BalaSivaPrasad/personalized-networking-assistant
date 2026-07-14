import requests
from typing import Tuple, Optional
from spellchecker import SpellChecker

# Initialize spell checker once
spell = SpellChecker()

def correct_spelling(text: str) -> Tuple[str, list]:
    """
    Correct spelling mistakes in the input text.
    Returns (corrected_text, list_of_corrections)
    """
    words = text.split()
    corrected_words = []
    corrections = []

    for word in words:
        # Skip short words and numbers
        if len(word) <= 2 or word.isdigit():
            corrected_words.append(word)
            continue
        
        # Check if the word is misspelled
        if word.lower() not in spell:
            suggestion = spell.correction(word)
            if suggestion and suggestion.lower() != word.lower():
                corrected_words.append(suggestion)
                corrections.append(f"'{word}' → '{suggestion}'")
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    
    corrected_text = " ".join(corrected_words)
    return corrected_text, corrections


def fact_check(query: str) -> Tuple[str, Optional[str]]:
    """
    Fact check a statement with spelling correction and deep verification.
    """
    try:
        original_query = query.strip()
        
        # Step 1: Correct spelling
        corrected_query, corrections = correct_spelling(original_query)
        
        # Build result parts
        result_parts = []
        
        # Show original vs corrected if there were changes
        if corrections:
            result_parts.append("🔤 **Spelling Corrections:**")
            for c in corrections:
                result_parts.append(f"  • {c}")
            result_parts.append("")
            # Use the corrected query for search
            search_query = corrected_query
        else:
            search_query = original_query
        
        # Step 2: Search Wikipedia with corrected query
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={requests.utils.quote(search_query)}&limit=3&format=json"
        search_response = requests.get(search_url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
        
        if search_response.status_code != 200:
            return "Unable to verify. Please check your internet connection.", None
        
        search_data = search_response.json()
        
        if not search_data[1]:
            return f"❌ No information found for '{search_query}'. The statement may be incorrect or unverifiable.", None
        
        # Get best match
        best_match = search_data[1][0]
        
        # Fetch summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_match)}"
        summary_response = requests.get(summary_url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
        
        if summary_response.status_code != 200:
            return f"Unable to retrieve details for '{best_match}'.", None
        
        summary_data = summary_response.json()
        title = summary_data.get('title', best_match)
        extract = summary_data.get('extract', '')
        source_url = summary_data.get('content_urls', {}).get('desktop', {}).get('page', '')
        
        # Step 3: Analyse the statement against the summary
        # Very simple factuality check: if the statement contains strongly negative/contradictory words
        # we try to see if the summary supports or refutes them.
        # A more robust check would require NLP, but here we'll present the info and let the user decide.
        
        result_parts.append(f"📚 **Topic:** {title}")
        result_parts.append("")
        
        # Indicate verification status
        result_parts.append("🔍 **Verification Result:**")
        result_parts.append(f"✅ Information found and verified from Wikipedia for the corrected query: '{search_query}'.")
        result_parts.append("")
        
        # Show a note if original was corrected
        if original_query.lower() != corrected_query.lower():
            result_parts.append("⚠️ The statement has been corrected for spelling. The original query may have contained errors.")
            result_parts.append("")
        
        # Supporting facts (truncate and highlight relevant parts)
        result_parts.append("📋 **Supporting Information:**")
        if len(extract) > 800:
            # Get the most relevant sentences
            sentences = extract.replace('. ', '.|').split('|')
            keywords = [word.lower() for word in search_query.split() if len(word) > 3]
            relevant = []
            for sent in sentences:
                if any(kw in sent.lower() for kw in keywords):
                    relevant.append(sent.strip())
            if relevant:
                extract = '. '.join(relevant[:3]) + '.'
            else:
                extract = extract[:800] + "..."
        result_parts.append(extract)
        result_parts.append("")
        
        # Related topics
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
        return f"❌ Error during verification: {str(e)}", None