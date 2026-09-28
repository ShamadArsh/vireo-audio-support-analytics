# Vireo Audio — Task 4 Submission Form

## 1. What did you build, and what business outcome does it move?
I built a lightweight Streamlit support-performance dashboard using deterministic Pandas analysis plus an optional local Ollama qualitative text analysis. It reports policy-compliant CSAT, handle time, SLA breaches and replacement economics, then creates a contextual Tier-1 training attention watchlist.

The business pilot is the four lowest-CSAT eligible Chat Frontline attention candidates. Their Q2 2026 replacement rate was **24.5%**, versus **15.3%** for Chat Frontline overall. Using the observed team rate as the benchmark, rather than choosing an arbitrary target, gives an estimated quarterly opportunity of approximately **₹31,191** at the observed Q2 volume and replacement-cost mix. This is an opportunity estimate, not a causal savings guarantee.

## 2. What does one run cost, and monthly cost at ~650 tickets/week?
The dashboard has **₹0 in paid model/API charges**. Core metrics and Q&A use local Pandas calculations. The optional root-cause model is local Ollama, so there is no per-ticket API charge.

Arithmetic for ~650 tickets/week:
- 650 × 52 / 12 ≈ 2,817 tickets/month
- 2,817 × ₹0 paid model/API cost per ticket = **₹0/month** in paid model/API charges

This excludes the user's existing machine/electricity cost and any future production infrastructure.

## 3. How do you know it works?
The deterministic analysis was checked on all **11,750 supplied tickets**, including **11,183 completed tickets** and **4,947 CSAT responses**. Checks include duplicate ticket IDs, unknown agents after the agent join, and negative handle times after legacy timestamp conversion. The expected headline metrics reconcile to 1,014 SLA breaches and ₹3,236,490 of policy-based replacement cost.

The AI root-cause component has no labelled ground truth, so I do **not** claim an AI accuracy percentage. It is qualitative assistance only and should be manually reviewed before decisions are made.

## 4. Did you change, narrow or push back on the client ask? What, when and why?
Yes. I initially considered a raw all-agent bottom-ten ranking. I changed this to a Tier-1, within-team screening because the supplied policy says Tier 2 work is structurally different and should not be compared with Tier 1 on volume metrics. I also added a ≥75 CSAT-response gate.

I used policy replacement cost (product unit cost + ₹340 logistics) rather than the rough ₹2,500 estimate in the email thread. Finally, I replaced an arbitrary 20% pilot target with the observed Q2 Chat Frontline baseline of 15.3%.

## 5. What is wrong with what you are handing us?
- The watchlist is a screening flag, not proof that an individual caused an outcome.
- The ≥75-response gate is an analyst-chosen stability threshold.
- The Q2 team baseline is a benchmark, not a causal training forecast.
- The optional AI root-cause output has no labelled ground truth.
- The supplied data includes known junk IVR transcripts, which can make text analysis noisy.
- The prototype is snapshot-based and is not connected directly to the live helpdesk.
- The Q&A supports common deterministic question patterns rather than arbitrary natural-language analysis.

## 6. What did you deliberately leave out and why?
I left out a live helpdesk integration, production database, authentication, deployment infrastructure, streaming, per-ticket paid LLM calls, lot-code analysis and a large frontend/backend architecture. These were not necessary to demonstrate the requested business logic within the assignment's limited time. The dashboard can be refreshed when a new CSV snapshot is supplied.

## 7. Anything built/found nobody asked for?
Yes:
- SLA credit exposure in rupees.
- Policy-based replacement-cost economics.
- Contextual Tier-1/team-relative training watchlist.
- A deterministic “Ask the dashboard” interface for common business questions.
- A refresh action for replacing the CSV snapshot.
- Optional sampled local-Ollama root-cause analysis.

## 8. What AI did you use? Where did it help, waste time, and what did you discard?
I used ChatGPT for analysis/methodology/reasoning and local Ollama `qwen2.5-coder:7b` for optional qualitative root-cause analysis. AI helped accelerate data interpretation, implementation and iteration on the dashboard. I deliberately did not use an LLM for numerical metrics because deterministic calculations are safer.

I discarded the raw all-agent bottom-ten idea, arbitrary target-setting, per-ticket LLM calls, and a larger production architecture. No paid model/API calls are required.

**3-minute recording:** [PASTE PUBLIC RECORDING LINK]

## 9. Public Google Drive Link
[PASTE PUBLIC GOOGLE DRIVE LINK]

## 10. Someone picks this up Monday: three things they need to know
1. Run `streamlit run app.py`; the dashboard works from the supplied CSV snapshot.
2. The training watchlist is Tier 1 only, within-team, ≥75 CSAT responses, and is a screening flag rather than a causal ranking.
3. The Q&A is deterministic and snapshot-based; the optional Ollama analysis is qualitative and should not be treated as ground truth.

## 11. Honest hours spent
[ENTER ACTUAL HOURS]

## 12. GitHub Repo Link
[PASTE GITHUB REPOSITORY LINK]

## 13. Public GitHub repo URL
[PASTE PUBLIC GITHUB URL]
