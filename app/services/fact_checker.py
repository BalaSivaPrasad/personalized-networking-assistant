import requests
from typing import Tuple, Optional
from spellchecker import SpellChecker
from duckduckgo_search import DDGS

spell = SpellChecker()

def correct_spelling(text: str) -> Tuple[str, list]:
    """Correct spelling and return (corrected_text, list of corrections)."""
    words = text.split()
    corrected_words = []
    corrections = []
    for word in words:
        if len(word) <= 2 or word.isdigit():
            corrected_words.append(word)
            continue
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


def search_web(query: str) -> list:
    """Search the web using DuckDuckGo and return list of results."""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception:
        return []


def fact_check(query: str) -> Tuple[str, Optional[str]]:
    """
    Fact check a statement with spelling correction,
    Wikipedia verification, and web search.
    Returns (HTML_result, best_source_url).
    """
    try:
        original_query = query.strip()
        html_parts = []

        # ---------- Spelling Correction ----------
        corrected_query, corrections = correct_spelling(original_query)
        if corrections:
            html_parts.append('<p><b>🔤 Spelling Corrections:</b><br>')
            for c in corrections:
                html_parts.append(f'&nbsp;&nbsp;• {c}<br>')
            html_parts.append('</p>')
            search_query = corrected_query
        else:
            search_query = original_query

        # ---------- Wikipedia ----------
        wiki_title = None
        wiki_extract = None
        wiki_link = None
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={requests.utils.quote(search_query)}&limit=3&format=json"
            resp = requests.get(search_url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data[1]:
                    best = data[1][0]
                    sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best)}"
                    sum_resp = requests.get(sum_url, headers={'User-Agent': 'NetworkingAssistant/1.0'}, timeout=10)
                    if sum_resp.status_code == 200:
                        sdata = sum_resp.json()
                        wiki_title = sdata.get("title", best)
                        wiki_extract = sdata.get("extract", "")
                        wiki_link = sdata.get("content_urls", {}).get("desktop", {}).get("page", "")
        except Exception:
            pass

        # ---------- Web Search ----------
        web_results = search_web(search_query)

        # ---------- Build HTML Report ----------
        html_parts.append('<h3>🔍 Verification Report</h3>')

        # Wikipedia section
        if wiki_extract:
            html_parts.append(f'<p><b>📚 Wikipedia – {wiki_title}</b><br>')
            extract = wiki_extract[:800]
            if len(wiki_extract) > 800:
                extract += "..."
            html_parts.append(f'{extract}<br>')
            if wiki_link:
                html_parts.append(f'<a href="{wiki_link}" target="_blank">Read full Wikipedia article</a>')
            html_parts.append('</p>')
        else:
            html_parts.append('<p><b>📚 Wikipedia:</b> No direct article found.</p>')

        # Web search section
        if web_results:
            html_parts.append('<p><b>🌐 Top Web Results:</b><br>')
            for i, res in enumerate(web_results, 1):
                title = res.get('title', 'No title')
                snippet = res.get('body', res.get('snippet', ''))[:200]
                url = res.get('href', res.get('url', ''))
                html_parts.append(f'<b>{i}. {title}</b><br>')
                html_parts.append(f'{snippet}...<br>')
                if url:
                    html_parts.append(f'<a href="{url}" target="_blank">{url}</a><br>')
                html_parts.append('<br>')
            html_parts.append('</p>')
        else:
            html_parts.append('<p><b>🌐 Web Search:</b> No relevant results found.</p>')

        # Conclusion
        html_parts.append('<p><b>💡 Conclusion:</b> ')
        if wiki_extract or web_results:
            html_parts.append('Multiple sources were consulted. The statement appears to be <b>supported</b> based on the information above.')
        else:
            html_parts.append('No reliable information was found to verify this statement. It may be unverified or incorrect.')
        html_parts.append('</p>')

        result_html = "\n".join(html_parts)
        # Use the first available URL as the main source
        main_url = wiki_link if wiki_link else (web_results[0].get('href') if web_results else None)
        return result_html, main_url

    except Exception as e:
        return f"<p style='color:red;'>❌ Error during verification: {str(e)}</p>", None