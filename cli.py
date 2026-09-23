"""
antigravity-pause: Unified CLI Interface
Supports command-line probing, checkpoint management, and process sanitation.
"""

import sys
import argparse
import json
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.network_probe import NetworkProbe, ProbeResult
from core.engine import CheckpointEngine
from core.process_guard import ProcessGuard
from core.kill_switch import AntigravityKillSwitch


def cmd_probe(args):
    result = NetworkProbe.run_full_probe(timeout=args.timeout)
    data = result.to_dict()

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if result.status == ProbeResult.STATUS_OK else 1

    # Human-readable colored output
    if result.status == ProbeResult.STATUS_OK:
        print(f"\n[OK] اتصال ایمن است (Latency: {data['latency_ms']}ms | IP: {data['ip']} | Country: {data['country']})")
        print(f"-> {data['message']}")
        return 0
    elif result.status == ProbeResult.STATUS_IP_LEAK_IRAN:
        print(f"\n[ALERT - IP LEAK] نشت آی‌پی شناسایی شد!")
        print(f"-> {data['message']}")
        print(f"-> برای جلوگیری از مسدودسازی و ارور ۴۰۳، قبل از ادامه فیلترشکن را متصل و تست کنید.")
        return 2
    else:
        print(f"\n[ERROR] اینترنت متصل نیست یا مسیر مسدود است (کد: {result.status})")
        print(f"-> {data['message']}")
        return 1


def cmd_checkpoint_save(args):
    target = CheckpointEngine.save_checkpoint(
        task_intent=args.task or "General task in progress",
        current_phase=args.phase or "Execution",
        last_completed_step=args.last_step or "Step completed",
        next_immediate_step=args.next_step or "Proceed to next task",
        base_dir=args.cwd,
    )
    print(f"[OK] چک‌پوینت ذخیره شد: {target}")
    return 0


def cmd_checkpoint_load(args):
    data = CheckpointEngine.load_active_checkpoint(base_dir=args.cwd)
    if not data:
        print("[INFO] هیچ چک‌پوینت فعالی یافت نشد.")
        return 1

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_checkpoint_clear(args):
    cleared = CheckpointEngine.clear_active_checkpoint(base_dir=args.cwd, archive=not args.no_archive)
    if cleared:
        print("[OK] چک‌پوینت فعال آرشیو و پاکسازی شد.")
        return 0
    else:
        print("[INFO] چک‌پوینتی برای پاکسازی وجود نداشت.")
        return 0


def cmd_clean_locks(args):
    cleaned = ProcessGuard.clean_git_locks(repo_dir=args.cwd or ".")
    if cleaned:
        print(f"[OK] قفل‌های معلق گیت پاکسازی شدند: {cleaned}")
    else:
        print("[OK] قفل معلقی در مخزن یافت نشد.")
    return 0


def cmd_killswitch(args):
    action = args.action
    if action == "status":
        data = AntigravityKillSwitch.get_status()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        if data["kill_switch_enabled"]:
            print(f"\n[ACTIVE] کیل‌سوئیچ فایروال روشن است (تعداد رول‌ها: {data['active_rules_count']})")
            print(f"-> کارت‌های فیزیکی مسدودشده: {', '.join(data['physical_adapters'])}")
            print(f"-> برنامه‌های محافظت‌شده: {len(data['protected_binaries'])} فایل اجرایی")
        else:
            print(f"\n[INACTIVE] کیل‌سوئیچ فایروال خاموش است.")
            print(f"-> برای فعال‌سازی از دستور: python cli.py killswitch enable استفاده کنید.")
        return 0

    elif action == "enable":
        data = AntigravityKillSwitch.enable()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0 if data.get("success") else 1
        if data.get("success"):
            print(f"\n[OK] {data.get('message')}")
            return 0
        else:
            print(f"\n[ERROR] {data.get('message', 'خطا در فعال‌سازی')}")
            if data.get("error") == "ADMIN_REQUIRED":
                print("-> پیشنهاد: ترمینال را در حالت Run as Administrator اجرا کرده یا فایل enable_killswitch.bat را اجرا کنید.")
            return 1

    elif action == "disable":
        data = AntigravityKillSwitch.disable()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0 if data.get("success") else 1
        if data.get("success"):
            print(f"\n[OK] {data.get('message')}")
            return 0
        else:
            print(f"\n[ERROR] {data.get('message', 'خطا در غیرفعال‌سازی')}")
            return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="antigravity-pause: Resilience, Checkpoint & Kill Switch CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # probe
    p_probe = subparsers.add_parser("probe", help="Run out-of-band network & leak probe")
    p_probe.add_argument("--json", action="store_true", help="Output pure JSON")
    p_probe.add_argument("--timeout", type=float, default=3.0, help="Probe timeout in seconds")
    p_probe.set_defaults(func=cmd_probe)

    # killswitch
    p_ks = subparsers.add_parser("killswitch", help="Manage Windows Firewall Outbound Kill Switch for Antigravity")
    p_ks.add_argument("action", choices=["status", "enable", "disable"], help="Kill Switch operation (status, enable, disable)")
    p_ks.add_argument("--json", action="store_true", help="Output pure JSON for agents / automation")
    p_ks.set_defaults(func=cmd_killswitch)

    # checkpoint save
    p_save = subparsers.add_parser("checkpoint-save", help="Save active checkpoint atomically")
    p_save.add_argument("--task", type=str, help="Overall task intent")
    p_save.add_argument("--phase", type=str, help="Current phase name")
    p_save.add_argument("--last-step", type=str, help="Last completed step description")
    p_save.add_argument("--next-step", type=str, help="Next immediate action")
    p_save.add_argument("--cwd", type=str, default=".", help="Base project directory")
    p_save.set_defaults(func=cmd_checkpoint_save)

    # checkpoint load
    p_load = subparsers.add_parser("checkpoint-load", help="Load active checkpoint")
    p_load.add_argument("--cwd", type=str, default=".", help="Base project directory")
    p_load.set_defaults(func=cmd_checkpoint_load)

    # checkpoint clear
    p_clear = subparsers.add_parser("checkpoint-clear", help="Clear or archive active checkpoint")
    p_clear.add_argument("--cwd", type=str, default=".", help="Base project directory")
    p_clear.add_argument("--no-archive", action="store_true", help="Delete without archiving")
    p_clear.set_defaults(func=cmd_checkpoint_clear)

    # clean locks
    p_locks = subparsers.add_parser("clean-locks", help="Clean dangling .git lock files")
    p_locks.add_argument("--cwd", type=str, default=".", help="Target repository directory")
    p_locks.set_defaults(func=cmd_clean_locks)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
