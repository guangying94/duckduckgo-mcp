import os
from typing import Any, Dict, List, Optional

from ddgs import DDGS
from fastmcp import FastMCP
import trafilatura


mcp = FastMCP("duckduckgo-search")


def _extract_body(item: Dict[str, Any]) -> str:
	for key in ("body", "snippet", "description", "content", "summary"):
		value = item.get(key)
		if isinstance(value, str) and value.strip():
			return value.strip()
	return ""


def _fetch_url_content(url: str) -> str:
	if not url:
		return ""
	try:
		downloaded = trafilatura.fetch_url(url)
		if not downloaded:
			return ""
		text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
		return text.strip() if isinstance(text, str) else ""
	except Exception:
		return ""


def _normalize_results(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
	results: List[Dict[str, Any]] = []
	for item in items:
		url = item.get("href") or item.get("url") or ""
		extracted = _fetch_url_content(url)
		results.append(
			{
				"title": item.get("title") or "",
				"url": url,
				"body": _extract_body(item),
				"extracted": extracted,
				"source": item.get("source") or "",
				"date": item.get("date") or "",
			}
		)
	return results


@mcp.tool()
def search_text(query: str, max_results: int = 5) -> Dict[str, Any]:
	"""Search DuckDuckGo text results and return JSON with body content."""
	max_results = max(1, min(max_results, 20))
	with DDGS() as ddgs:
		items = list(ddgs.text(query, max_results=max_results))
	return {"query": query, "results": _normalize_results(items)}


@mcp.tool()
def search_news(query: str, max_results: int = 5) -> Dict[str, Any]:
	"""Search DuckDuckGo news results and return JSON with body content."""
	max_results = max(1, min(max_results, 20))
	with DDGS() as ddgs:
		items = list(ddgs.news(query, max_results=max_results))
	return {"query": query, "results": _normalize_results(items)}


@mcp.tool()
def fetch_url_content(url: str) -> Dict[str, Any]:
	"""Fetch and extract main content from a URL."""
	content = _fetch_url_content(url)
	return {"url": url, "content": content}


if __name__ == "__main__":
	transport = os.getenv("MCP_TRANSPORT", "http")
	host = os.getenv("MCP_HOST", "0.0.0.0")
	port = int(os.getenv("PORT", "8000"))
	if transport == "http":
		mcp.run(transport="http", host=host, port=port)
	else:
		mcp.run()
