# DuckDuckGo MCP Server (FastMCP)

This MCP server exposes two tools using the DuckDuckGo Python library:

- `search_text(query, max_results=5)`
- `search_news(query, max_results=5)`

Both return JSON with `body` content for each result.

## Local run

```bash
python main.py
```

Set transport/port as needed:

```bash
export MCP_TRANSPORT=http
export PORT=8000
python main.py
```

## Docker

```bash
docker build -t duckduckgo-mcp .
docker run -p 8000:8000 duckduckgo-mcp
```

## Testing (venv)

If you want to run tests locally, create a Python 3.13 virtual environment first:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
