import json
import time
from pathlib import Path

import streamlit as st
import yaml
import requests
from crewai import Agent, Crew, LLM, Process, Task

from tools.router_tools import classify_request, estimate_tokens
from tools.analyst_tools import profile_sample_data, suggest_kpis, check_sql_query
from tools.scientist_tools import detect_problem_type, suggest_features, flag_data_risks, recommend_metrics

st.set_page_config(page_title="Retail Analytics Crew", page_icon="🛒", layout="wide")

BASE_DIR = Path(__file__).parent
AGENTS_YAML = BASE_DIR / "config" / "agents.yaml"
TASKS_YAML = BASE_DIR / "config" / "tasks.yaml"
SAMPLE_CSV = BASE_DIR / "mcp_server" / "sample_data" / "events_sample.csv"

DEFAULT_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:3b"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_models(url):
    try:
        r = requests.get(f"{url}/api/tags", timeout=5)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", []) if m.get("name")]
    except Exception:
        return []


def history_to_text(messages, limit):
    lines = []
    for m in messages[-limit:]:
        who = m.get("agent", m["role"])
        lines.append(f"{who}: {m['content']}")
    return "\n".join(lines)


def make_llm(model, url, temp):
    return LLM(model=f"ollama/{model}", base_url=url, temperature=temp)


def build_agent(key, cfg, llm, tool_list):
    c = cfg[key]
    return Agent(
        role=c["role"],
        goal=c["goal"],
        backstory=c["backstory"],
        llm=llm,
        allow_delegation=c.get("allow_delegation", False),
        max_iter=c.get("max_iter", 5),
        max_retry_limit=c.get("max_retry_limit", 2),
        tools=tool_list,
        verbose=True,
    )


def get_route(user_prompt, chat_history, agents_cfg, tasks_cfg, llm, log):
    router = build_agent("router_agent", agents_cfg, llm, [classify_request])
    t = Task(
        description=tasks_cfg["routing_task"]["description"].format(
            chat_history=chat_history, user_prompt=user_prompt
        ),
        expected_output=tasks_cfg["routing_task"]["expected_output"],
        agent=router,
    )
    crew = Crew(agents=[router], tasks=[t], process=Process.sequential, verbose=False)
    log.append("router: deciding who should handle this")
    result = str(crew.kickoff())

    text = result.upper()
    if "BOTH" in text:
        return "both"
    if "SCIENTIST" in text:
        return "scientist"
    return "analyst"


def run_analyst(user_prompt, chat_history, agents_cfg, tasks_cfg, llm, log):
    agent = build_agent(
        "analyst_agent", agents_cfg, llm,
        [profile_sample_data, suggest_kpis, check_sql_query],
    )
    t = Task(
        description=tasks_cfg["analyst_task"]["description"].format(
            user_prompt=user_prompt, chat_history=chat_history
        ),
        expected_output=tasks_cfg["analyst_task"]["expected_output"],
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[t], process=Process.sequential, verbose=False)
    log.append("analyst: working on the request")
    return str(crew.kickoff())


def run_scientist(user_prompt, chat_history, agents_cfg, tasks_cfg, llm, log):
    agent = build_agent(
        "scientist_agent", agents_cfg, llm,
        [detect_problem_type, suggest_features, flag_data_risks, recommend_metrics],
    )
    t = Task(
        description=tasks_cfg["scientist_task"]["description"].format(
            user_prompt=user_prompt, chat_history=chat_history
        ),
        expected_output=tasks_cfg["scientist_task"]["expected_output"],
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[t], process=Process.sequential, verbose=False)
    log.append("scientist: working on the request")
    return str(crew.kickoff())


def run_editor(user_prompt, analyst_notes, scientist_notes, agents_cfg, tasks_cfg, llm, log):
    agent = build_agent("editor_agent", agents_cfg, llm, [])
    t = Task(
        description=tasks_cfg["editor_task"]["description"].format(
            analyst_notes=analyst_notes or "none",
            scientist_notes=scientist_notes or "none",
            user_prompt=user_prompt,
        ),
        expected_output=tasks_cfg["editor_task"]["expected_output"],
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[t], process=Process.sequential, verbose=False)
    log.append("editor: merging notes into final answer")
    return str(crew.kickoff())


if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_log" not in st.session_state:
    st.session_state.last_log = []
if "last_metrics" not in st.session_state:
    st.session_state.last_metrics = {}

try:
    agents_cfg = load_yaml(AGENTS_YAML)
    tasks_cfg = load_yaml(TASKS_YAML)
except Exception as e:
    st.error(f"could not load config: {e}")
    st.stop()

with st.sidebar:
    st.title("Settings")
    url = st.text_input("Ollama URL", value=DEFAULT_URL)
    models = get_models(url)
    if models:
        model = st.selectbox("Model", models, index=models.index(DEFAULT_MODEL) if DEFAULT_MODEL in models else 0)
        st.success("connected to ollama")
    else:
        model = st.text_input("Model name", value=DEFAULT_MODEL)
        st.warning("ollama not detected, using manual model name")

    temp = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    hist_len = st.slider("Chat history messages used", 2, 20, 8, 2)
    ctx_window = st.number_input("Context window tokens", 1024, 131072, 8192, 1024)

    st.divider()
    st.subheader("Agents")
    for k, c in agents_cfg.items():
        with st.expander(c.get("name", k)):
            st.write(c.get("role"))
            st.caption(c.get("goal"))

    st.divider()
    st.subheader("Last run log")
    if st.session_state.last_log:
        for line in st.session_state.last_log:
            st.caption(line)
    else:
        st.caption("nothing run yet")

    st.divider()
    st.subheader("Token estimate")
    if st.session_state.last_metrics:
        st.json(st.session_state.last_metrics)
    else:
        st.caption("appears after first message")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.last_log = []
        st.session_state.last_metrics = {}
        st.rerun()

st.title("Retail Analytics Crew")
st.caption("Router picks analyst, scientist, or both. Sequential process, not CrewAI auto delegation.")
st.info(f"Model: `{model}` at `{url}`. Sample data: `{SAMPLE_CSV.name}`")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("agent"):
            st.markdown(f"**{m['agent']}**")
        st.markdown(m["content"])

prompt = st.chat_input("Ask about sales, KPIs, churn, forecasts...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    chat_history = history_to_text(st.session_state.messages, hist_len)
    tok_est = estimate_tokens(chat_history + prompt)
    st.session_state.last_metrics = json.loads(tok_est)

    log = []
    llm = make_llm(model, url, temp)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_thinking..._")

        try:
            start = time.time()
            route = get_route(prompt, chat_history, agents_cfg, tasks_cfg, llm, log)

            analyst_notes = None
            scientist_notes = None

            if route in ("analyst", "both"):
                analyst_notes = run_analyst(prompt, chat_history, agents_cfg, tasks_cfg, llm, log)
            if route in ("scientist", "both"):
                scientist_notes = run_scientist(prompt, chat_history, agents_cfg, tasks_cfg, llm, log)

            final = run_editor(prompt, analyst_notes, scientist_notes, agents_cfg, tasks_cfg, llm, log)
            elapsed = round(time.time() - start, 2)
            log.append(f"done in {elapsed}s, route was {route}")

            placeholder.markdown(final)
            st.session_state.messages.append({"role": "assistant", "agent": "Retail Crew", "content": final})
            st.session_state.last_log = log

        except Exception as e:
            err = f"something went wrong: {e}\n\ncheck that `ollama serve` is running and the model is pulled."
            placeholder.error(err)
            log.append(f"failed: {e}")
            st.session_state.last_log = log
            st.session_state.messages.append({"role": "assistant", "agent": "System", "content": err})
