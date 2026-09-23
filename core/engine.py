"""
antigravity-pause: Checkpoint Engine
Atomic serialization and deserialization of agent workflows and subagent states.
"""

import os
import json
import time
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CheckpointEngine:
    CHECKPOINT_DIR = ".agents/checkpoints"
    ACTIVE_CHECKPOINT_FILE = "active_checkpoint.json"
    HISTORY_DIR = "history"

    @classmethod
    def get_checkpoint_dir(cls, base_dir: Optional[str] = None) -> Path:
        root = Path(base_dir) if base_dir else Path.cwd()
        checkpoint_path = root / cls.CHECKPOINT_DIR
        checkpoint_path.mkdir(parents=True, exist_ok=True)
        return checkpoint_path

    @classmethod
    def get_git_snapshot(cls, base_dir: Optional[str] = None) -> Dict[str, Any]:
        """Captures lightweight git status without heavy operations."""
        root = Path(base_dir) if base_dir else Path.cwd()
        snapshot = {"is_git": False, "branch": "", "modified_files": [], "untracked_files": []}
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain", "-b"],
                cwd=str(root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=3,
            )
            if res.returncode == 0:
                lines = res.stdout.strip().splitlines()
                snapshot["is_git"] = True
                if lines and lines[0].startswith("##"):
                    snapshot["branch"] = lines[0][3:].split("...")[0].strip()
                for line in lines[1:]:
                    if line.startswith("??"):
                        snapshot["untracked_files"].append(line[3:].strip())
                    else:
                        snapshot["modified_files"].append(line[3:].strip())
        except Exception:
            pass
        return snapshot

    @classmethod
    def save_checkpoint(
        cls,
        task_intent: str,
        current_phase: str,
        last_completed_step: str,
        next_immediate_step: str,
        subagents: Optional[List[Dict[str, Any]]] = None,
        base_dir: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> Path:
        """
        Saves a structured checkpoint atomically.
        Uses a temporary file + atomic rename (os.replace) to prevent file corruption.
        """
        checkpoint_dir = cls.get_checkpoint_dir(base_dir)
        target_file = checkpoint_dir / cls.ACTIVE_CHECKPOINT_FILE
        temp_file = checkpoint_dir / f".tmp_{int(time.time())}.json"

        git_snapshot = cls.get_git_snapshot(base_dir)

        payload = {
            "schema_version": "1.0",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "task_intent": task_intent,
            "current_phase": current_phase,
            "last_completed_step": last_completed_step,
            "next_immediate_step": next_immediate_step,
            "subagents": subagents or [],
            "git_state": git_snapshot,
            "metadata": extra_metadata or {},
        }

        # Atomic write
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        os.replace(temp_file, target_file)
        return target_file

    @classmethod
    def load_active_checkpoint(cls, base_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Loads and returns the active checkpoint if it exists."""
        checkpoint_dir = cls.get_checkpoint_dir(base_dir)
        target_file = checkpoint_dir / cls.ACTIVE_CHECKPOINT_FILE
        if not target_file.exists():
            return None

        try:
            with open(target_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    @classmethod
    def has_active_checkpoint(cls, base_dir: Optional[str] = None) -> bool:
        checkpoint_dir = cls.get_checkpoint_dir(base_dir)
        return (checkpoint_dir / cls.ACTIVE_CHECKPOINT_FILE).exists()

    @classmethod
    def clear_active_checkpoint(cls, base_dir: Optional[str] = None, archive: bool = True) -> bool:
        """Clears active checkpoint, optionally archiving it to history."""
        checkpoint_dir = cls.get_checkpoint_dir(base_dir)
        target_file = checkpoint_dir / cls.ACTIVE_CHECKPOINT_FILE
        if not target_file.exists():
            return False

        if archive:
            history_dir = checkpoint_dir / cls.HISTORY_DIR
            history_dir.mkdir(parents=True, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            archive_target = history_dir / f"checkpoint_{timestamp}.json"
            os.replace(target_file, archive_target)
        else:
            target_file.unlink(missing_ok=True)
        return True


if __name__ == "__main__":
    test_path = CheckpointEngine.save_checkpoint(
        task_intent="Refactor authentication system and fix token expiration",
        current_phase="Phase 2: Database Migration",
        last_completed_step="Applied migration 003_add_session_table.py",
        next_immediate_step="Run pytest tests/test_auth.py to verify schema",
        subagents=[
            {
                "role": "Database Migrator",
                "typeName": "self",
                "workspace": "inherit",
                "last_action": "Completed migration",
            }
        ],
    )
    print(f"Checkpoint successfully written to: {test_path}")
    loaded = CheckpointEngine.load_active_checkpoint()
    print("Loaded verification:", loaded["task_intent"])
