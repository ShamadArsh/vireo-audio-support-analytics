import os
import re
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from analysis.analysis import run

st.set_page_config(
    page_title="Vireo Audio — Support Performance",
    page_icon="🎧",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_analysis():
    return run()


def money(value):
    return f"₹{value:,.0f}"


def fmt_pct(value):
    return f"{value:.1%}"


def normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())


def agent_lookup(m, question):
    q = normalize(question)
    # Prefer explicit IDs because display names are not unique in the supplied roster.
    ids = sorted(m.agent_id.astype(str).unique(), key=len, reverse=True)
    for agent_id in ids:
        if agent_id.lower() in q:
            return m[m.agent_id.astype(str).eq(agent_id)].iloc[0]

    # Match full display names only when unambiguous.
    matches = []
    for _, row in m.iterrows():
        name = str(row["name"]).lower()
        if name and name in q:
            matches.append(row)
    unique_ids = {str(r["agent_id"]) for r in matches}
    if len(unique_ids) == 1:
        return matches[0]
    return None


def answer_question(question, completed, metrics, products):
    """Answer a small, deterministic set of business questions from the snapshot.

    The tool deliberately does not let an LLM invent numerical answers. Unsupported
    questions receive a safe response rather than a guessed result.
    """
    q = normalize(question)
    if not q:
        return "Please enter a question about the loaded support data."

    # Time window: Q2 2026 / Apr-Jun 2026.
    if "q2" in q or "apr-jun" in q or "april" in q and "june" in q:
        df = completed[
            (completed.created_at >= pd.Timestamp("2026-04-01"))
            & (completed.created_at < pd.Timestamp("2026-07-01"))
        ]
        label = "Q2 2026 (Apr–Jun)"
    else:
        df = completed
        label = "supplied period"

    # Agent-level questions.
    agent = agent_lookup(metrics, q)
    if agent is not None:
        if "csat" in q:
            return f"{agent['agent_id']} ({agent['name']}) — CSAT: {agent['csat']:.2f}/5 from {int(agent['csat_responses'])} responses."
        if "sla" in q or "breach" in q:
            return f"{agent['agent_id']} ({agent['name']}) — first-response SLA breach rate: {agent['sla_breach_rate']:.1%}."
        if "handle" in q or "time" in q:
            return f"{agent['agent_id']} ({agent['name']}) — median handle time: {agent['median_handle_h']:.2f} hours."
        if "ticket" in q or "volume" in q:
            return f"{agent['agent_id']} ({agent['name']}) — {int(agent['tickets']):,} completed tickets in the supplied period."
        if "replace" in q:
            return f"{agent['agent_id']} ({agent['name']}) — {int(agent['replacements']):,} replacement tickets in the supplied period."
        return f"I found {agent['agent_id']} ({agent['name']}). Ask for CSAT, SLA breaches, handle time, tickets, or replacements."

    # Team questions.
    teams = sorted(completed.team.dropna().unique())
    team = next((x for x in teams if x.lower() in q), None)
    if team:
        td = df[df.team.eq(team)]
        if len(td) == 0:
            return f"No completed tickets for {team} in {label}."
        if "csat" in q:
            value = td.csat_score.mean()
            responses = int(td.csat_score.count())
            return f"{team} — {label} CSAT: {value:.2f}/5 from {responses:,} responses."
        if "sla" in q or "breach" in q:
            value = td.sla_breach.mean()
            return f"{team} — {label} first-response SLA breach rate: {value:.1%} ({int(td.sla_breach.sum()):,} breaches)."
        if "replace" in q:
            value = (td.replacement_issued == "Y").mean()
            return f"{team} — {label} replacement rate: {value:.1%} ({int((td.replacement_issued == 'Y').sum()):,} replacements / {len(td):,} completed tickets)."
        if "ticket" in q or "volume" in q:
            return f"{team} — {label} completed tickets: {len(td):,}."
        return f"I found {team}. Ask for its CSAT, SLA breach rate, replacement rate, or ticket volume."

    # Watchlist.
    if "watchlist" in q or "training" in q and ("who" in q or "flag" in q):
        rows = st.session_state.get("watchlist")
        if rows is not None:
            names = ", ".join(f"{r.agent_id} ({r.name})" for _, r in rows.iterrows())
            return "Current Tier-1 training attention watchlist: " + names + "."

    # Overall / time-window metrics.
    if "csat" in q:
        return f"{label} CSAT: {df.csat_score.mean():.2f}/5 from {int(df.csat_score.count()):,} responses."
    if "sla" in q or "breach" in q:
        breaches = int(df.sla_breach.sum())
        return f"{label} first-response SLA breach rate: {df.sla_breach.mean():.1%} ({breaches:,} breaches). Estimated policy credit exposure: {money(breaches * 350)}."
    if "replacement" in q or "replace" in q:
        repl = df[df.replacement_issued.eq("Y")].merge(
            products[["sku", "unit_cost_inr"]], left_on="product_sku", right_on="sku", how="left"
        )
        cost = (repl.unit_cost_inr + 340).sum()
        return f"{label} replacement tickets: {len(repl):,}. Replacement rate: {(len(repl) / len(df)) if len(df) else 0:.1%}. Policy-based replacement cost estimate: {money(cost)}."
    if "handle" in q or "time" in q:
        return f"{label} median handle time: {df.handle_hours.median():.2f} hours; mean: {df.handle_hours.mean():.2f} hours."
    if "ticket" in q or "volume" in q:
        return f"{label} completed tickets: {len(df):,}."

    return (
        "I can answer deterministic questions about the loaded snapshot, including overall "
        "CSAT, SLA breaches, replacement rate/cost, handle time, team metrics, agent metrics, "
        "Q2 2026 metrics, and the training watchlist. I will not guess unsupported answers."
    )


# ---------- Load / refresh ----------
if "snapshot_loaded_at" not in st.session_state:
    st.session_state.snapshot_loaded_at = datetime.now().strftime("%d %b %Y %H:%M")

if st.sidebar.button("🔄 Refresh analysis", use_container_width=True):
    st.cache_data.clear()
    st.session_state.snapshot_loaded_at = datetime.now().strftime("%d %b %Y %H:%M")
    st.rerun()

try:
    t, completed, metrics, watchlist, products, pilot_rate, team_rate, pilot_n = load_analysis()
except Exception as exc:
    st.error(f"The analysis could not be loaded: {exc}")
    st.stop()

st.session_state["watchlist"] = watchlist

# ---------- Header ----------
st.title("Vireo Audio — Support Performance")
st.caption("Task 4 | Policy-compliant metrics + contextual Tier-1 training watchlist")
st.info(
    "Snapshot-based prototype: calculations run from the supplied CSV export. "
    "Refresh after replacing the CSVs; this prototype is not connected directly to the live helpdesk."
)

# ---------- KPI cards ----------
repl = completed[completed.replacement_issued.eq("Y")].merge(
    products[["sku", "unit_cost_inr"]], left_on="product_sku", right_on="sku", how="left"
)
replacement_cost = (repl.unit_cost_inr + 340).sum()
sla_breaches = int(completed.sla_breach.sum())

cols = st.columns(4)
cols[0].metric("Completed tickets", f"{len(completed):,}")
cols[1].metric("CSAT", f"{completed.csat_score.mean():.2f}/5")
cols[2].metric("SLA breach rate", f"{completed.sla_breach.mean():.1%}")
cols[3].metric("Replacement cost", money(replacement_cost))

# ---------- Agent performance ----------
st.subheader("Agent performance")
show = metrics.copy()
show["CSAT"] = show.csat.round(2)
show["Median handle (h)"] = show.median_handle_h.round(2)
show["SLA breach"] = (show.sla_breach_rate * 100).round(1).astype(str) + "%"
st.dataframe(
    show[
        [
            "agent_id", "name", "team", "tier", "tickets", "csat_responses",
            "CSAT", "Median handle (h)", "SLA breach"
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# ---------- Training watchlist ----------
st.subheader("Training attention watchlist")
st.caption(
    "Tier 1 only; agents are compared within team and must have at least 75 CSAT responses. "
    "This is a screening flag, not proof of causality."
)
watch = watchlist.copy()
watch["CSAT"] = watch.csat.round(2)
watch["Median handle (h)"] = watch.median_handle_h.round(2)
watch["SLA breach"] = (watch.sla_breach_rate * 100).round(1).astype(str) + "%"
st.dataframe(
    watch[
        [
            "agent_id", "name", "team", "tickets", "csat_responses",
            "CSAT", "Median handle (h)", "SLA breach", "attention_score"
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# ---------- Business goal ----------
q2 = completed[
    (completed.created_at >= pd.Timestamp("2026-04-01"))
    & (completed.created_at < pd.Timestamp("2026-07-01"))
]
chat_eligible = (
    metrics[(metrics.tier == 1) & (metrics.team == "Chat Frontline") & (metrics.csat_responses >= 75)]
    .sort_values("csat")
    .head(4)
)
pilot_ids = chat_eligible.agent_id.tolist()
pilot = q2[q2.agent_id.isin(pilot_ids)]
pilot_repl = pilot[pilot.replacement_issued.eq("Y")].merge(
    products[["sku", "unit_cost_inr"]], left_on="product_sku", right_on="sku", how="left"
)
avg_replacement_cost = (pilot_repl.unit_cost_inr + 340).mean()
opp = max(0, (pilot_rate - team_rate) * len(pilot)) * avg_replacement_cost

st.subheader("Business goal")
st.write(
    f"Pilot benchmark: reduce replacement rate for the four lowest-CSAT eligible Chat Frontline "
    f"attention candidates from {pilot_rate:.1%} in Apr–Jun 2026 toward the observed Q2 Chat Frontline "
    f"baseline of {team_rate:.1%}. At the observed Q2 volume and replacement-cost mix, the estimated "
    f"quarterly opportunity is {money(opp)}. This is an opportunity estimate, not a causal savings guarantee."
)
st.caption(
    f"Pilot volume: {len(pilot):,} completed tickets | Pilot agents: {', '.join(pilot_ids)} | "
    f"Average policy replacement cost in pilot: {money(avg_replacement_cost)}"
)

# ---------- Interactive Q&A ----------
st.subheader("Ask the dashboard")
st.caption(
    "Ask for a metric from the currently loaded snapshot. Numerical answers are calculated with "
    "deterministic Pandas logic rather than generated by an LLM."
)
question = st.text_input(
    "Question",
    placeholder="e.g. What is the Q2 2026 replacement rate for Chat Frontline?",
)
if st.button("Answer", type="primary"):
    st.success(answer_question(question, completed, metrics, products))

with st.expander("Example questions"):
    st.markdown(
        "- What is the overall CSAT?\n"
        "- What is the Q2 2026 SLA breach rate?\n"
        "- What is Chat Frontline's replacement rate in Q2?\n"
        "- What is A3004's CSAT?\n"
        "- How many tickets did Billing handle?\n"
        "- What is the replacement cost?\n"
        "- Who is on the training watchlist?"
    )

# ---------- Optional local AI ----------
st.subheader("Optional AI root-cause analysis")
st.write(
    "Only a small sample is sent to a local Ollama model; there are no per-ticket model calls. "
    "This output is qualitative assistance and has no labelled ground truth. Review before using it for decisions."
)
model = st.text_input("Ollama model", os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b"))
if st.button("Analyze sampled tickets"):
    candidate = completed[completed.agent_id.isin(watchlist.agent_id)].dropna(
        subset=["customer_message", "agent_notes"]
    )
    sample = candidate.sample(min(40, len(candidate)), random_state=42)
    prompt = (
        "Analyze these sampled Vireo support tickets. Identify 5 recurring actionable themes. "
        "Do not blame individuals or infer causality. Separate queue/product problems from "
        "agent-process problems. Return: theme | evidence | possible training/process action.\n"
        + "\n".join(
            f"{r.agent_id}|CSAT {r.csat_score}|{r.category}|customer:{str(r.customer_message)[:500]}|note:{str(r.agent_notes)[:300]}"
            for _, r in sample.iterrows()
        )
    )
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        st.write(response.json().get("response", ""))
    except Exception as exc:
        st.warning(f"Ollama unavailable: {exc}. The deterministic dashboard and Q&A still work.")

st.divider()
st.caption(
    f"Snapshot loaded: {st.session_state.snapshot_loaded_at} | "
    "See memo.md, analysis/validation.md, prompts.md and submission-form.md for methodology and handoff notes."
)
