# Retail Analytics Crew

Multi-agent analytics assistant for a small retail dataset, built with CrewAI,
a local Ollama model, Streamlit, and a local MCP server for the data tools.

Instead of CrewAI's hierarchical auto-delegation, this version routes
explicitly: a router agent tags the request as analyst / scientist / both,
the app runs whichever agent(s) are needed as separate sequential crews, and
an editor agent merges the notes into one final answer.

## Folder structure

```text
retail_analytics_crew/
├── app.py
├── requirements.txt
├── README.md
├── architecture.md
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── tools/
│   ├── router_tools.py
│   ├── analyst_tools.py
│   └── scientist_tools.py
├── mcp_server/
│   ├── server.py
│   └── sample_data/
│       └── events_sample.csv
└── tests/
    └── test_tools.py
```

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.2:3b
ollama serve
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
pytest tests/
```

## Notes

- `mcp_server/server.py` exposes `run_query`, `profile_csv`,
  `check_query_safety`, and `data_quality_report` over MCP. It runs
  standalone (`python mcp_server/server.py`) and is meant to be hit from
  a separate client for the DuckDB-backed tools; the in-app agent tools in
  `tools/` cover the same ground locally so the app works even if the MCP
  server isn't running.
- Router decision is a plain text line (`ROUTE: analyst|scientist|both`)
  parsed with a simple string check, no JSON schema enforcement yet.
- Editor agent has no tools, it only rewrites text.
