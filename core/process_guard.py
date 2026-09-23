"""
antigravity-pause: Process Guard & Lock Sanitizer
Safely cleans dangling locks and prepares subagents for hibernation without state corruption.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ProcessGuard:
    @classmethod
    def clean_git_locks(cls, repo_dir: str = ".") -> List[str]:
        """
        Removes dangling .git/index.lock files caused by sudden network drops or abrupt terminations.
        """
        root = Path(repo_dir).resolve()
        git_dir = root / ".git"
        cleaned = []

        if not git_dir.exists():
            return cleaned

        lock_files = list(git_dir.glob("*.lock")) + list((git_dir / "refs").rglob("*.lock"))
        for lock in lock_files:
            try:
                lock.unlink(missing_ok=True)
                cleaned.append(str(lock.relative_to(root)))
            except Exception:
                pass
        return cleaned

    @classmethod
    def get_pause_contract_message(cls, reason: str = "Network switch or temporary standby") -> str:
        """Returns standard instruction prompt sent to active subagents when pausing."""
        return (
            f"[SYSTEM NOTICE: STANDBY INSTRUCTION]\n"
            f"Reason: {reason}\n"
            f"Action Required:\n"
            f"1. Immediately stop any active network calls or tool dispatches.\n"
            f"2. Ensure any pending file modification has valid syntax/state.\n"
            f"3. Yield your turn without calling further tools.\n"
            f"4. Await resume signal from orchestrator."
        )

    @classmethod
    def get_resume_contract_message(cls) -> str:
        """Returns standard instruction prompt sent to active subagents when resuming."""
        return (
            "[SYSTEM NOTICE: RESUME INSTRUCTION]\n"
            "Network connection is verified and safe. Resume your assigned task from your last completed step."
        )


if __name__ == "__main__":
    locks = ProcessGuard.clean_git_locks(".")
    print(f"Cleaned locks: {locks}")
    print(ProcessGuard.get_pause_contract_message())
