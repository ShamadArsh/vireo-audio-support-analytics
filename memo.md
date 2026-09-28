# Memo to Priya Raman — Vireo Audio Support

## Executive summary
The data supports a targeted training approach rather than a raw all-agent ranking. Tier 2/warranty work is structurally different, so the training watchlist compares Tier 1 agents within their own teams and requires at least 75 CSAT responses.

## Key findings
- 11,183 completed tickets in the supplied period.
- Overall responding-customer CSAT: 3.33/5.
- 1,014 first-response SLA breaches; policy credit exposure ≈ ₹354,900.
- 1,797 replacements; policy-based estimated cost ≈ ₹3,236,490.
- Apr–Jun 2026: 195 SLA breaches among 1,995 completed tickets (9.8%), with ≈ ₹68,250 in SLA credits.

## Training pilot
The dashboard flags ten Tier 1 agents for attention using team-relative CSAT (50%), median handle time (30%) and SLA breach rate (20%), after a ≥75-CSAT-response gate. This is a screening tool, not a causal ranking.

The four lowest-CSAT eligible Chat Frontline attention candidates had a Q2 replacement rate of 24.5%. The observed Q2 Chat Frontline replacement rate was 15.3%, so I use that team baseline as the benchmark rather than choosing an arbitrary target. At the observed Q2 pilot volume and replacement-cost mix, moving toward the baseline represents an estimated quarterly opportunity of approximately **₹31,191**. This is an opportunity estimate, not a causal savings guarantee.

## Recommended use
Use the watchlist as a review queue for coaching and process investigation, not as an automatic performance verdict. In particular, queue design and product/warranty work can affect observed outcomes. The optional AI analysis is useful for surfacing themes from sampled text, but its outputs should be reviewed by a human before action.

## Caveats
CSAT is survey-based; blank scores are excluded. The supplied email thread identifies roughly 40 junk IVR transcripts, so text analysis can be noisy. The data does not provide labelled ground truth for AI root-cause categories. The prototype is snapshot-based rather than connected to the live helpdesk. Historical roster/source-system details also require care when interpreting individual outcomes.
