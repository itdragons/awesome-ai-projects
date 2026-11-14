#!/usr/bin/env python3
"""
Awesome AI Projects - 仓库健康度与状态巡检脚本
无需第三方依赖，仅使用 Python 标准库。
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}"

# 忽略非项目仓库链接
IGNORED_REPOS = {
    "sindresorhus/awesome",
}

def extract_github_repos(file_path):
    """从 markdown 中提取所有 GitHub 仓库 (owner, repo)"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配形如 https://github.com/owner/repo 的链接
    pattern = r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"
    matches = re.findall(pattern, content)

    repos = []
    seen = set()
    for owner, repo in matches:
        # 去除末尾的 .git 或斜杠等
        repo = repo.rstrip("/").removesuffix(".git")
        slug = f"{owner}/{repo}".lower()

        # 过滤 badges, issues, pull 等非项目链接
        if repo in ("issues", "pulls", "releases", "actions") or slug in IGNORED_REPOS:
            continue
        if slug not in seen:
            seen.add(slug)
            repos.append((owner, repo))

    return repos

def fetch_repo_info(owner, repo, token=None):
    """通过 GitHub REST API 查询仓库信息"""
    url = GITHUB_API.format(owner=owner, repo=repo)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Awesome-AI-Projects-Inspector")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"status": 200, "data": data}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "data": None, "reason": e.reason}
    except Exception as e:
        return {"status": 0, "data": None, "reason": str(e)}

def format_date_diff(pushed_at_str):
    """计算最后活跃距今的天数"""
    if not pushed_at_str:
        return "未知", 0
    pushed_at = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    days = (now - pushed_at).days
    if days < 30:
        return f"{days} 天前", days
    elif days < 365:
        return f"{days // 30} 个月前", days
    else:
        return f"{days // 365} 年前", days

def main():
    token = os.environ.get("GITHUB_TOKEN")
    repos = extract_github_repos(README_PATH)
    print(f"🔍 找到 {len(repos)} 个被收录的 GitHub 仓库，开始巡检...\n")

    issues = []
    rows = []

    for owner, repo in repos:
        slug = f"{owner}/{repo}"
        result = fetch_repo_info(owner, repo, token)
        status_code = result["status"]

        if status_code == 200:
            data = result["data"]
            stars = data.get("stargazers_count", 0)
            archived = data.get("archived", False)
            pushed_at = data.get("pushed_at")
            last_push_str, days = format_date_diff(pushed_at)

            tags = []
            if archived:
                tags.append("⚠️ 已归档(Archived)")
                issues.append(f"- **{slug}** 已被原作者归档。")
            elif days > 365:
                tags.append("💤 超过1年无提交")
            else:
                tags.append("✅ 活跃")

            state_label = " / ".join(tags)
            rows.append((slug, f"{stars:,}", last_push_str, state_label))
            print(f"[{status_code}] {slug:35} | ⭐ {stars:<6} | 最近提交: {last_push_str:8} | {state_label}")
        else:
            reason = result.get("reason", "Unknown")
            state_label = f"❌ 访问异常 ({status_code}: {reason})"
            issues.append(f"- **{slug}** 无法正常访问: `{state_label}`")
            rows.append((slug, "-", "-", state_label))
            print(f"[{status_code}] {slug:35} | {state_label}")

    # 生成 Markdown 巡检报告
    report_lines = [
        "## 📊 仓库健康度巡检报告",
        f"\n> 巡检时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}，共检查 {len(repos)} 个项目。\n",
        "| 项目 | Star 数 | 最后更新 | 状态 |",
        "| :--- | :---: | :---: | :--- |",
    ]
    for slug, stars, last_push, state in rows:
        report_lines.append(f"| [{slug}](https://github.com/{slug}) | {stars} | {last_push} | {state} |")

    if issues:
        report_lines.append("\n### ⚠️ 需要注意的问题")
        report_lines.extend(issues)
    else:
        report_lines.append("\n🎉 所有收录项目均处于健康、正常访问状态！")

    report_content = "\n".join(report_lines)

    # 如果在 GitHub Actions 环境中，写入 Step Summary
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(report_content + "\n")

    # 同时写入本地 reports/latest.md 方便记录
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(report_dir, exist_ok=True)
    with open(os.path.join(report_dir, "latest.md"), "w", encoding="utf-8") as f:
        f.write(report_content + "\n")

    print("\n✅ 巡检完成，报告已保存至 reports/latest.md")

if __name__ == "__main__":
    main()
