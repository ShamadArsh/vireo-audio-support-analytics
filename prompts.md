# AI-use log / prompt notes

## What AI was used for
- ChatGPT: helped reason about the assignment, data definitions, methodology, validation checks, and implementation choices.
- Local Ollama (`qwen2.5-coder:7b`): optional qualitative root-cause analysis on a small sample of up to 40 tickets.
- No paid model/API calls are required by the tool.

## Initial approach
The first analysis idea was a raw all-agent bottom-ten ranking using CSAT.

## What changed
- Narrowed the training screen to Tier 1 because the supplied policy explicitly says Tier 2 work should not be compared with Tier 1 on volume metrics.
- Compared Tier 1 agents within their team rather than across unlike queues.
- Added a ≥75 CSAT-response gate to avoid over-interpreting thin survey samples.
- Kept CSAT as the primary component, with median handle time and SLA breach rate as supporting components.
- Used agent IDs throughout because display names are not unique.
- Used policy replacement cost (unit cost + ₹340) rather than the rough ₹2,500 estimate in the email thread.
- Replaced the arbitrary 20% pilot target with the observed Q2 Chat Frontline baseline of 15.3%.

## Deliberately discarded
- Per-ticket paid LLM calls: too expensive and unnecessary for the dashboard metrics.
- A large production architecture with database, authentication, deployment and live streaming: outside the assignment's small working-prototype scope.
- Lot-code analysis: not necessary to establish the requested agent-performance screen.
- Raw all-agent "worst ten" ranking: can confound structurally different Tier 2 work.
- LLM-generated numerical metrics: deterministic Pandas calculations are safer.

## Root-cause prompt
The local model is asked to identify five recurring actionable themes from a small sample, provide evidence, and distinguish queue/product issues from agent-process issues. It is explicitly told not to blame individuals or infer causality.

## Important AI limitation
There is no labelled ground-truth dataset for root-cause categories. Therefore the tool does not claim an AI accuracy percentage. AI output is qualitative and should be reviewed by a human.
