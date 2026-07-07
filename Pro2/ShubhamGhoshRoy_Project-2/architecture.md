# Architecture

```mermaid
graph TD
    User([User]) --> UI[Streamlit Chat]
    UI --> Router[Router Agent]

    Router -->|route = analyst| Analyst[Retail Data Analyst]
    Router -->|route = scientist| Scientist[Retail Data Scientist]
    Router -->|route = both| Analyst
    Router -->|route = both| Scientist

    Analyst -.->|tools| ATools[Profile Data, Suggest KPIs, Check SQL]
    Scientist -.->|tools| STools[Problem Type, Features, Risks, Metrics]

    ATools --> Data[(events_sample.csv)]

    Analyst --> Editor[Editor Agent]
    Scientist --> Editor

    Editor --> UI

    subgraph Standalone
    MCP[MCP Server] --> MTools[run_query, profile_csv, check_query_safety, data_quality_report]
    MTools --> Data
    end
```

Router, analyst, scientist, and editor each run as their own single-task
`Process.sequential` crew, called one after another by `app.py`. This is
different from CrewAI's `Process.hierarchical`, where a manager agent
delegates automatically at runtime. Here the app decides the path up front
based on the router's one-line output, which makes the flow easier to trace
and log in the sidebar.

The MCP server is a separate process (`python mcp_server/server.py`) with
its own read-only DuckDB tools. It is not wired into the Streamlit process
in this version, it can be started and queried independently, which is a
gap worth closing in a later revision.
