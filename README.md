# Langgraph Blog Agent

A LangGraph workflow that routes a topic, optionally researches it with Tavily, creates a blog plan with Gemini, writes sections in parallel, and saves the final Markdown article.

## Requirements

- Python 3.11 or newer
- A Google Gemini API key
- A Tavily API key for topics that require web research

## Setup on Windows

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run the project with the virtual-environment interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m Backend.graph
```

## Environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`.env` is ignored by Git. Never commit API keys. If a key has been reported as leaked or exposed, revoke it and create a replacement key before running the application.

## Run

From the project root, run the graph as a module:

```powershell
python -m Backend.graph
```

The generated article is saved as a Markdown file in the project root. Images, when requested and successfully generated, are saved under `images/`.

You can also call the graph from Python:

```python
from Backend.graph import run

result = run("Self Attention in Transformer Architecture")
print(result["final"])
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'Backend'`

Run the command from the repository root and use module mode:

```powershell
python -m Backend.graph
```

Do not run `python Backend/graph.py` directly.

### Gemini `403 PERMISSION_DENIED`

The configured Google API key is invalid, revoked, or reported as leaked. Replace `GOOGLE_API_KEY` in `.env` with a new key.

### Tavily is unavailable

The workflow can still run for closed-book topics without search results. Add a valid `TAVILY_API_KEY` when research is required.
