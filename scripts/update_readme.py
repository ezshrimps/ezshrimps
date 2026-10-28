"""Refresh the auto-generated sections of README.md.

- FUNDING: the 5 largest USD rounds of the last 7 days, from SVTR's public MCP server
- ACTIVITY: my 5 most recently pushed public repos
"""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone

USER = "ezshrimps"
README = os.path.join(os.path.dirname(__file__), "..", "README.md")
MCP_URL = "https://svtr.ai/api/mcp"

SECTORS = {
    "算力": "Compute", "数据": "Data", "训练与推理栈": "Training & Inference", "互连": "Interconnect",
    "大模型": "Foundation Models", "垂类模型": "Vertical Models", "开发平台": "Dev Platforms",
    "智能体": "AI Agents", "优化测评": "Optimization & Evals", "生命科学": "Life Sciences",
    "企业服务": "Enterprise", "金融服务": "Fintech", "安全合规": "Security", "机器人": "Robotics",
    "零售营销": "Retail & Marketing", "开发者": "Developer Tools", "效率工具": "Productivity",
    "社交文娱": "Social & Media", "双碳环保": "Climate", "垂类行业": "Vertical Industry",
    "法律服务": "Legal", "教育培训": "Education", "交通物流": "Mobility & Logistics",
    "国防安防": "Defense", "地产科技": "PropTech", "工业制造": "Manufacturing", "智能硬件": "Hardware",
}
STAGES = {
    "天使轮": "Angel", "种子轮": "Seed", "A轮": "Series A", "B轮": "Series B", "C轮": "Series C",
    "D轮及以后": "Series D+", "Pre-IPO轮": "Pre-IPO", "战略投资": "Strategic", "未披露": "Undisclosed",
}


def http(url, body=None, headers=None):
    headers = {"User-Agent": f"{USER}-profile-readme", **(headers or {})}
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def usd(amount):
    m = re.fullmatch(r"\$([\d.]+)([MB])", amount)
    if not m:
        return 0
    return float(m.group(1)) * (1000 if m.group(2) == "B" else 1)


def funding_table():
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "get_recent_funding_events", "arguments": {"lang": "en"}},
    }).encode()
    text = json.loads(http(MCP_URL, body, {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }))["result"]["content"][0]["text"]

    # line format: - 2026-10-27 · **Name** · sector · stage · $45M · lead: A、B
    deals = []
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        parts = line[2:].split(" · ")
        amount = next((p for p in parts if p.startswith("$")), None)
        if not amount or usd(amount) == 0:
            continue
        lead = next((p.split(": ", 1)[1] for p in parts if p.startswith("lead: ")), "—")
        deals.append({
            "date": parts[0][5:],
            "name": parts[1].strip("*"),
            "sector": SECTORS.get(parts[2], parts[2]),
            "stage": STAGES.get(parts[3], parts[3]) if parts[3] != amount else "—",
            "amount": amount,
            "lead": lead.split("、")[0] + (" +" if "、" in lead else ""),
        })
    deals.sort(key=lambda d: usd(d["amount"]), reverse=True)

    rows = ["| Date | Company | Sector | Round | Amount | Lead |", "|---|---|---|---|---:|---|"]
    rows += [f"| {d['date']} | **{d['name']}** | {d['sector']} | {d['stage']} | {d['amount']} | {d['lead']} |"
             for d in deals[:5]]
    return "\n".join(rows)


def activity_list():
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    repos = json.loads(http(f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=30", headers=headers))
    repos = [r for r in repos if not r["fork"] and r["name"] != USER][:5]
    return "\n".join(f"- `{r['pushed_at'][:10]}` [{r['name']}]({r['html_url']})" for r in repos)


def replace(readme, tag, content):
    return re.sub(rf"(<!-- {tag}:START -->).*?(<!-- {tag}:END -->)",
                  lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", readme, flags=re.S)


if __name__ == "__main__":
    with open(README, encoding="utf-8") as f:
        readme = f.read()
    readme = replace(readme, "FUNDING", funding_table())
    readme = replace(readme, "ACTIVITY", activity_list())
    readme = replace(readme, "UPDATED", f"<sub>last sync: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC</sub>")
    with open(README, "w", encoding="utf-8") as f:
        f.write(readme)
