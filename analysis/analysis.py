from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TARGETS = {"chat": 15, "email": 480, "voice": 120, "social": 240}


def run():
    """Run the deterministic support-performance analysis from the supplied snapshot."""
    t = pd.read_csv(DATA / "tickets.csv")
    a = pd.read_csv(DATA / "agents.csv")
    p = pd.read_csv(DATA / "products.csv")

    for c in ["created_at", "first_response_at", "resolved_at"]:
        t[c] = pd.to_datetime(t[c], errors="coerce")

    # Legacy resolution timestamps are reconstructed in UTC in the source notes;
    # convert them to the IST display convention used by the helpdesk export.
    legacy = t.source_system.eq("legacy_fd")
    t.loc[legacy, "resolved_at"] += pd.Timedelta(hours=5, minutes=30)

    t["first_response_min"] = (
        t.first_response_at - t.created_at
    ).dt.total_seconds() / 60
    t["sla_target_min"] = t.channel.map(TARGETS)
    t["sla_breach"] = t.first_response_min > t.sla_target_min
    t["handle_hours"] = (
        t.resolved_at - t.first_response_at
    ).dt.total_seconds() / 3600

    lookup = a[["agent_id", "name", "site", "team", "shift", "tier"]].drop_duplicates(
        "agent_id"
    )
    c = t[t.status.isin(["resolved", "closed"])].merge(
        lookup, on="agent_id", how="left", validate="many_to_one"
    )

    m = (
        c.groupby(["agent_id", "name", "team", "tier"])
        .agg(
            tickets=("ticket_id", "count"),
            csat_responses=("csat_score", "count"),
            csat=("csat_score", "mean"),
            median_handle_h=("handle_hours", "median"),
            mean_handle_h=("handle_hours", "mean"),
            sla_breach_rate=("sla_breach", "mean"),
            replacements=("replacement_issued", lambda x: (x == "Y").sum()),
        )
        .reset_index()
    )

    # Tier 2 is structurally different work and is excluded from the Tier-1
    # training comparison. Tier-1 agents are compared only within their team.
    x = m[m.tier == 1].copy()
    x["csat_bad_pct"] = x.groupby("team").csat.transform(lambda s: 1 - s.rank(pct=True))
    x["handle_bad_pct"] = x.groupby("team").median_handle_h.transform(lambda s: s.rank(pct=True))
    x["sla_bad_pct"] = x.groupby("team").sla_breach_rate.transform(lambda s: s.rank(pct=True))
    x["attention_score"] = (
        0.5 * x.csat_bad_pct + 0.3 * x.handle_bad_pct + 0.2 * x.sla_bad_pct
    )

    watch = (
        x[x.csat_responses >= 75]
        .sort_values("attention_score", ascending=False)
        .head(10)
        .copy()
    )

    # Q2 business pilot: four lowest-CSAT eligible Tier-1 Chat Frontline agents.
    q2 = c[(c.created_at >= pd.Timestamp("2026-04-01")) & (c.created_at < pd.Timestamp("2026-07-01"))]
    chat_eligible = (
        m[(m.tier == 1) & (m.team == "Chat Frontline") & (m.csat_responses >= 75)]
        .sort_values("csat")
        .head(4)
    )
    pilot = q2[q2.agent_id.isin(chat_eligible.agent_id)]
    team_q2 = q2[q2.team == "Chat Frontline"]
    pilot_rate = (pilot.replacement_issued == "Y").mean()
    team_rate = (team_q2.replacement_issued == "Y").mean()

    return t, c, m, watch, p, pilot_rate, team_rate, len(pilot)


if __name__ == "__main__":
    _, _, _, w, _, _, _, _ = run()
    print(
        w[
            [
                "agent_id",
                "name",
                "team",
                "tickets",
                "csat_responses",
                "csat",
                "median_handle_h",
                "sla_breach_rate",
                "attention_score",
            ]
        ].to_string(index=False)
    )
