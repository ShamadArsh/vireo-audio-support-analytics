# Vireo Audio — Task 4

A small, policy-aware support analytics prototype for the Vireo Audio take-home.

## Run from a clean machine

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# or Windows cmd
.venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens locally, normally at `http://localhost:8501`.

## Optional local AI

The deterministic dashboard does **not** require an LLM.

For the optional qualitative root-cause analysis:

```bash
ollama serve
ollama pull qwen2.5-coder:7b
```

The app sends only a small sample (up to 40 tickets) to the local Ollama endpoint. There are no per-ticket model calls and no paid model/API calls.

## What the tool does

- Policy-compliant completed-ticket metrics
- CSAT per agent, excluding blank survey responses
- First-response SLA breach rate using channel targets
- Handle time from first response to resolution
- Policy-based replacement economics: product unit cost + ₹340 logistics
- Agent performance table with `agent_id` so duplicate display names are not conflated
- Contextual Tier-1 training attention watchlist, compared within team and gated at ≥75 CSAT responses
- Business pilot benchmark using the observed Q2 Chat Frontline baseline rather than an arbitrary target
- **Ask the dashboard:** deterministic natural-language questions about common metrics, teams, agents and Q2 2026
- **Refresh analysis:** reload the CSV snapshot after replacing the supplied data files
- Optional local Ollama qualitative root-cause analysis

## Important scope boundary

This is a **snapshot-based prototype**, not a live helpdesk integration. Replacing the CSV exports and clicking **Refresh analysis** recalculates the metrics. A production implementation could connect the same analysis layer to a live helpdesk/API, but that was deliberately left out of the five-hour scope.

The Q&A feature also does not let an LLM invent numerical answers. Supported numerical answers are calculated directly from the loaded data with Pandas. Unsupported questions receive a safe explanation instead of a guessed number.

## Key policy/method decisions

- `resolved` + `closed` count as completed attendance.
- Blank CSAT is excluded from averages.
- Legacy resolution timestamps are converted UTC → IST as required by the supplied reporting notes.
- SLA breach is based on first response later than the channel target.
- Tier 2 is excluded from the Tier-1 training comparison because the policy says Tier 2 work is structurally different.
- Tier-1 watchlist comparison is within team and requires ≥75 CSAT responses.
- Replacement cost uses product unit cost + ₹340 logistics, not the rough ₹2,500 estimate in the email thread.
- No per-ticket paid LLM calls.
- The watchlist is a screening flag, not proof of causality.
- AI root-cause output is qualitative and has no labelled ground truth.

## Files

- `app.py` — Streamlit dashboard and deterministic Q&A
- `analysis/analysis.py` — core metrics and watchlist logic
- `analysis/validation.md` — data checks and limitations
- `analysis/training_watchlist.csv` — generated watchlist snapshot
- `analysis/summary.json` — generated headline metrics
- `memo.md` — one-page business memo
- `prompts.md` — AI-use log and discarded approaches
- `submission-form.md` — completed submission draft with placeholders for the candidate's links/hours
- `data/` — supplied CSV snapshot
- `docs/` — supplied policy/email reference files
