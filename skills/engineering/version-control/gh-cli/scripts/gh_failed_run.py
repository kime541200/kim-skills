#!/usr/bin/env python3
"""
GitHub Actions Failed Run Analyzer

This script triages a specified GitHub Actions run, or the most recent failed
run when no run ID is supplied, and extracts error evidence from failed jobs.
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional


def run_gh_command(cmd: List[str]) -> Any:
    """
    Execute a gh CLI command and return parsed JSON output.

    Args:
        cmd: List of command arguments to pass to gh

    Returns:
        Parsed JSON output from the command

    Raises:
        SystemExit: If gh command fails
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout) if result.stdout else {}
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print("Error parsing JSON output from gh command", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_most_recent_failed_run(repo: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get the most recent failed workflow run.

    Args:
        repo: Optional repository in format 'owner/name'

    Returns:
        Run information dictionary or None if no failed runs found
    """
    cmd = [
        "gh", "run", "list",
        "--status", "failure",
        "--limit", "1",
        "--json", "databaseId,number,conclusion,status,createdAt,displayTitle,url,headBranch,headSha,event"
    ]

    if repo:
        cmd.extend(["--repo", repo])

    runs = run_gh_command(cmd)

    if not runs:
        return None

    return runs[0]


def get_run(run_id: int, repo: Optional[str] = None) -> Dict[str, Any]:
    """Get one workflow run by database ID."""
    cmd = [
        "gh", "run", "view", str(run_id),
        "--json",
        "databaseId,number,conclusion,status,createdAt,displayTitle,url,headBranch,headSha,event,workflowName"
    ]
    if repo:
        cmd.extend(["--repo", repo])
    return run_gh_command(cmd)


def get_failed_jobs(run_id: int, repo: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all jobs from a run and filter for failed ones.

    Args:
        run_id: The workflow run database ID
        repo: Optional repository in format 'owner/name'

    Returns:
        List of failed job dictionaries
    """
    cmd = [
        "gh", "run", "view", str(run_id),
        "--json", "jobs"
    ]

    if repo:
        cmd.extend(["--repo", repo])

    result = run_gh_command(cmd)
    jobs = result.get("jobs", [])

    # Filter for failed jobs (conclusion is failure, timed_out, cancelled, etc.)
    failed_jobs = [
        job for job in jobs
        if job.get("conclusion") not in ["success", "skipped", None]
    ]

    return failed_jobs


def extract_error_excerpts(log_text: str, max_lines: int = 50) -> List[str]:
    """
    Extract relevant error lines from log text.

    Args:
        log_text: Raw log text from failed job
        max_lines: Maximum number of error lines to return

    Returns:
        List of error excerpt strings
    """
    error_patterns = [
        r".*\berror\b.*",
        r".*\bfailed\b.*",
        r".*\bfailure\b.*",
        r".*\bexception\b.*",
        r".*\bERROR\b.*",
        r".*\bFAILED\b.*",
        r".*\bFAILURE\b.*",
        r".*\bEXCEPTION\b.*",
        r".*\bcannot\b.*",
        r".*\bpanic\b.*",
        r".*Process completed with exit code [1-9].*",
        r".*\btimeout\b.*",
    ]

    excerpts = []
    lines = log_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line matches any error pattern
        for pattern in error_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Remove ANSI color codes and timestamps if present
                clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                clean_line = re.sub(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s*', '', clean_line)

                if clean_line and clean_line not in excerpts:
                    excerpts.append(clean_line)
                    if len(excerpts) >= max_lines:
                        return excerpts
                break

    return excerpts


def get_job_logs(run_id: int, job_id: int, repo: Optional[str] = None) -> str:
    """
    Get logs for a specific failed job.

    Args:
        run_id: The workflow run database ID
        job_id: The job database ID
        repo: Optional repository in format 'owner/name'

    Returns:
        Log text for the job
    """
    cmd = [
        "gh", "run", "view", str(run_id),
        "--log-failed",
        "--job", str(job_id)
    ]

    if repo:
        cmd.extend(["--repo", repo])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        # Do not attach all failed logs to one job; that misattributes evidence.
        return ""


def analyze_failed_run(
    repo: Optional[str] = None,
    run_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Triage a specified run, or the most recent failed run.

    Args:
        repo: Optional repository in format 'owner/name'
        run_id: Optional workflow run database ID

    Returns:
        Dictionary containing run analysis
    """
    run = get_run(run_id, repo) if run_id is not None else get_most_recent_failed_run(repo)

    if not run:
        return {
            "error": "No failed runs found",
            "repository": repo or "current"
        }

    # Get failed jobs using databaseId
    failed_jobs = get_failed_jobs(run["databaseId"], repo)

    # Build result structure
    result = {
        "run": {
            "number": run["number"],
            "database_id": run["databaseId"],
            "url": run["url"],
            "workflow": run.get("workflowName") or run.get("displayTitle"),
            "title": run.get("displayTitle"),
            "conclusion": run["conclusion"],
            "status": run["status"],
            "created_at": run["createdAt"],
            "branch": run.get("headBranch"),
            "commit": run.get("headSha"),
            "event": run.get("event")
        },
        "failed_jobs": [],
        "repository": repo or "current"
    }

    # Analyze each failed job
    for job in failed_jobs:
        job_info = {
            "name": job["name"],
            "database_id": job.get("databaseId"),
            "conclusion": job["conclusion"],
            "status": job.get("status"),
            "started_at": job.get("startedAt"),
            "completed_at": job.get("completedAt"),
            "error_excerpts": []
        }

        # Get logs and extract errors using databaseId
        job_id = job.get("databaseId")
        logs = get_job_logs(run["databaseId"], job_id, repo) if job_id else ""
        if logs:
            job_info["error_excerpts"] = extract_error_excerpts(logs)

        result["failed_jobs"].append(job_info)

    return result


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Triage a GitHub Actions run and extract failed-job evidence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                        # Analyze current repository
  %(prog)s --repo owner/name      # Analyze specific repository
  %(prog)s --run-id 123456        # Analyze a specified run
  %(prog)s --repo owner/name --run-id 123456
        """
    )

    parser.add_argument(
        "--repo",
        type=str,
        help="Repository to analyze in format 'owner/name'"
    )

    parser.add_argument(
        "--run-id",
        type=int,
        help="Workflow run database ID; defaults to the latest failed run"
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output with indentation"
    )

    args = parser.parse_args()

    # Check if gh CLI is installed
    try:
        subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: gh CLI is not installed or not in PATH", file=sys.stderr)
        print("Install it from: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)

    result = analyze_failed_run(args.repo, args.run_id)

    # Output JSON
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
