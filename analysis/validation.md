# Validation

## Deterministic data checks
- Tickets: 11,750
- Completed attendance (`resolved` + `closed`): 11,183
- CSAT responses: 4,947
- Overall CSAT: 3.3259/5
- SLA breaches: 1,014
- SLA breach rate: 9.0673%
- SLA credit exposure: ₹354,900
- Replacement count: 1,797
- Policy-based replacement cost: ₹3,236,490
- Q2 2026 completed tickets: 1,995
- Q2 2026 SLA breaches: 195
- Q2 2026 SLA breach rate: 9.7744%
- Q2 2026 SLA credit exposure: ₹68,250
- Q2 Chat Frontline pilot tickets: 188
- Pilot replacement rate: 24.4681%
- Q2 Chat Frontline replacement rate: 15.3226%
- Estimated pilot opportunity toward team baseline: ≈ ₹31,191
- Duplicate ticket IDs: 0
- Unknown agents after join: 0
- Negative handle times after legacy UTC→IST conversion: 0

## What was checked
The core analysis engine was run directly against the supplied CSVs. The app source was syntax-compiled. The submission ZIP was tested for archive integrity.

The Streamlit browser UI should still be launched on the submission machine because this environment does not have Streamlit installed and has no network access for installing it. The dashboard shown in the candidate's local browser is therefore the final UI smoke test.

## AI validation limitation
The pack provides no labelled ground truth for AI root-cause categories, so no numerical AI accuracy claim is made. The LLM output is qualitative assistance only. Before final submission, manually review a small sample of outputs and mention the qualitative review in the recording if performed.

## Known wrong/weak cases
- The supplied email thread identifies roughly 40 junk IVR transcripts; text analysis can misinterpret these.
- The watchlist is a screening flag, not proof that an agent caused the observed outcomes.
- The ≥75-response threshold is an analyst-chosen stability gate, not a policy requirement.
- The Q2 team baseline is a benchmark, not proof that training will causally achieve it.
- The interactive Q&A intentionally answers only supported deterministic question patterns; it does not pretend to be a general-purpose analyst.
