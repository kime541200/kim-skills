#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitLab Issue Archiver
---------------------
Fetches all issues from a GitLab project via `glab` CLI and saves each one
as a Markdown file with YAML front-matter under a dated directory.

Usage:
    python3 archive_issues.py [OPTIONS]

Options:
    -R, --repo REPO     GitLab repo in GROUP/NAMESPACE/REPO format.
                        Auto-detected from the origin remote if omitted.
    -o, --output DIR    Root output directory. Default: ./issues
    -d, --date DATE     Date label for the subdirectory (YYYY-MM-DD).
                        Default: today's date.
    --per-page N        Number of issues per page (default: 100).
    --force             Replace issue files that already exist.

Output structure:
    <output>/<date>/opened/  — open issues
    <output>/<date>/closed/  — closed issues

Examples:
    # Auto-detect repo, output to ./issues/2026-02-26/
    python3 archive_issues.py

    # Specify repo explicitly
    python3 archive_issues.py -R mygroup/myproject

    # Custom output directory
    python3 archive_issues.py -o ./docs/issues
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from typing import Dict, List

# ── helpers ──────────────────────────────────────────────────────────────────

def _detect_repo() -> str:
    """Read the origin URL and return a glab-compatible repository selector."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        m = re.search(r'gitlab\.com[:/](.+?)(?:\.git)?$', url)
        if m:
            return m.group(1)
        if url:
            # glab accepts full HTTP and Git URLs, which preserve self-managed hosts.
            return url
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return ""


def _safe_filename(iid: int, title: str) -> str:
    safe = re.sub(r'[^\w\u4e00-\u9fff\u3040-\u30ff]+', '_', title)[:60].strip('_')
    return f"#{iid}_{safe}.md"


def _fetch_issues(repo: str, per_page: int) -> List[dict]:
    """Fetch every issue page and de-duplicate by issue IID."""
    issues: List[dict] = []
    seen_iids = set()
    page = 1

    while True:
        cmd = [
            "glab", "issue", "list", "--all", "-O", "json",
            "--page", str(page), "--per-page", str(per_page), "-R", repo
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            page_issues = json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] glab command failed on page {page}:\n{e.stderr}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to parse glab JSON on page {page}.", file=sys.stderr)
            sys.exit(1)

        if not isinstance(page_issues, list):
            print(f"[ERROR] Expected a JSON list on page {page}.", file=sys.stderr)
            sys.exit(1)

        added = 0
        for issue in page_issues:
            iid = issue.get("iid")
            if iid not in seen_iids:
                seen_iids.add(iid)
                issues.append(issue)
                added += 1

        if len(page_issues) < per_page:
            return issues
        if added == 0:
            print("[ERROR] Pagination repeated a page; refusing an incomplete archive.", file=sys.stderr)
            sys.exit(1)
        page += 1


def _yaml_string(value: object) -> str:
    """Return a JSON-quoted string, which is also valid YAML."""
    return json.dumps(str(value), ensure_ascii=False)


def _render_markdown(issue: dict) -> str:
    iid = issue["iid"]
    title = issue["title"]
    state = issue["state"]
    description = (issue.get("description") or "").strip()
    web_url = issue.get("web_url", "")
    created_at = issue.get("created_at", "")
    updated_at = issue.get("updated_at", "")
    closed_at = issue.get("closed_at") or ""

    author = issue.get("author") or {}
    author_name = author.get("name", "") if isinstance(author, dict) else ""
    author_username = author.get("username", "") if isinstance(author, dict) else ""

    assignees = issue.get("assignees") or []
    assignee_names = [a.get("name", "") for a in assignees if isinstance(a, dict)]
    assignee_str = ", ".join(assignee_names) if assignee_names else "（未指派）"

    labels = issue.get("labels") or []
    if labels and isinstance(labels[0], dict):
        label_names = [l.get("name", "") for l in labels]
    else:
        label_names = list(labels)
    label_str = ", ".join(label_names) if label_names else "（無）"

    milestone = issue.get("milestone")
    milestone_title = milestone.get("title", "") if isinstance(milestone, dict) else ""

    closed_line = f"**關閉時間**：{closed_at}  \n" if closed_at else ""
    return f"""---
id: {iid}
title: {_yaml_string(title)}
state: {_yaml_string(state)}
author: {_yaml_string(f'{author_name} (@{author_username})')}
assignees: {_yaml_string(assignee_str)}
labels: {json.dumps(label_names, ensure_ascii=False)}
milestone: {_yaml_string(milestone_title)}
created_at: {_yaml_string(created_at)}
updated_at: {_yaml_string(updated_at)}
closed_at: {_yaml_string(closed_at)}
url: {_yaml_string(web_url)}
---

# #{iid} {title}

**狀態**：{state}  
**建立者**：{author_name} (@{author_username})  
**指派給**：{assignee_str}  
**標籤**：{label_str}  
**里程碑**：{milestone_title or "（無）"}  
**建立時間**：{created_at}  
**更新時間**：{updated_at}  
{closed_line}**原文連結**：{web_url}

---

## 描述

{description if description else "（無描述）"}
"""


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Archive GitLab issues to Markdown files.")
    parser.add_argument("-R", "--repo", default="", help="GitLab repo (GROUP/NAMESPACE/REPO)")
    parser.add_argument("-o", "--output", default="./issues", help="Root output directory")
    parser.add_argument("-d", "--date", default=date.today().isoformat(), help="Date label (YYYY-MM-DD)")
    parser.add_argument("--per-page", type=int, default=100, dest="per_page", help="Issues per page")
    parser.add_argument("--force", action="store_true", help="Replace issue files that already exist")
    args = parser.parse_args()

    if args.per_page < 1:
        parser.error("--per-page must be at least 1")

    repo = args.repo or _detect_repo()
    if not repo:
        print("[ERROR] Could not resolve a repository. Pass -R GROUP/NAMESPACE/REPO or a full URL.", file=sys.stderr)
        return 2

    print(f"▶ Fetching issues from: {repo}")
    issues = _fetch_issues(repo, args.per_page)
    print(f"  Found {len(issues)} issues\n")

    base = os.path.join(args.output, args.date)
    planned: List[Dict[str, object]] = []
    for issue in sorted(issues, key=lambda x: x["iid"]):
        state = issue.get("state")
        if state not in ("opened", "closed"):
            print(f"[ERROR] Unsupported state for issue {issue.get('iid')}: {state}", file=sys.stderr)
            return 1
        filename = _safe_filename(issue["iid"], issue["title"])
        planned.append({
            "issue": issue,
            "path": os.path.join(base, state, filename),
            "relative": f"{state}/{filename}",
        })

    collisions = [item["path"] for item in planned if os.path.exists(str(item["path"]))]
    if collisions and not args.force:
        print(
            f"[ERROR] {len(collisions)} archive file(s) already exist under {base}. "
            "Review them and pass --force to replace them.",
            file=sys.stderr,
        )
        return 1

    for state in ("opened", "closed"):
        os.makedirs(os.path.join(base, state), exist_ok=True)

    written = 0
    counts = {"opened": 0, "closed": 0}
    for item in planned:
        issue = item["issue"]
        content = _render_markdown(issue)
        with open(str(item["path"]), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {item['relative']}")
        written += 1
        counts[issue["state"]] += 1

    print(
        f"\n✅ Archived {written}/{len(issues)} issues "
        f"(opened: {counts['opened']}, closed: {counts['closed']}) → {base}/"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
