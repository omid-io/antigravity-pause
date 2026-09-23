"""
antigravity-pause: Windows Firewall Kill Switch
Prevents outbound traffic leaks of Antigravity processes through physical network adapters (Wi-Fi, Ethernet)
when the VPN/TUN tunnel disconnects.
"""

import os
import sys
import json
import ctypes
import subprocess
from typing import Dict, Any, List, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def is_admin() -> bool:
    """Checks whether the current process has Windows Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


class AntigravityKillSwitch:
    RULE_PREFIX = "Antigravity-KillSwitch"

    @classmethod
    def get_antigravity_binaries(cls) -> List[str]:
        """Detects standard and active executable paths for Antigravity."""
        binaries = []
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            base_dir = os.path.join(local_app_data, "Programs", "antigravity")
            exe_main = os.path.join(base_dir, "Antigravity.exe")
            exe_lang = os.path.join(base_dir, "resources", "bin", "language_server.exe")

            if os.path.exists(exe_main):
                binaries.append(exe_main)
            if os.path.exists(exe_lang):
                binaries.append(exe_lang)

        # Fallback / additional detection from running processes if not found
        if not binaries:
            try:
                ps_cmd = (
                    "Get-Process | Where-Object { $_.ProcessName -match 'antigravity|language_server' } "
                    "| Select-Object -ExpandProperty Path -Unique"
                )
                res = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", ps_cmd],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                if res.returncode == 0:
                    for line in res.stdout.strip().splitlines():
                        p = line.strip()
                        if p and os.path.exists(p) and p not in binaries:
                            binaries.append(p)
            except Exception:
                pass

        return binaries

    @classmethod
    def get_physical_adapters(cls) -> List[str]:
        """
        Discovers physical network adapters (e.g., Wi-Fi, Ethernet)
        while ignoring virtual VPN adapters (TAP, wintun, sing-tun, etc.).
        """
        ps_cmd = (
            "Get-NetAdapter | Where-Object { "
            "  ($_.HardwareInterface -eq $true -or $_.InterfaceDescription -match 'Intel|Realtek|Broadcom|Qualcomm|Wi-Fi|Ethernet') "
            "  -and ($_.InterfaceDescription -notmatch 'TAP|TunnelBear|VPN|wintun|sing-tun|WireGuard|Virtual') "
            "} | Select-Object -ExpandProperty Name"
        )
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if res.returncode == 0:
                adapters = [a.strip() for a in res.stdout.strip().splitlines() if a.strip()]
                if adapters:
                    return adapters
        except Exception:
            pass

        # Default standard Windows names if query fails
        return ["Wi-Fi", "Ethernet"]

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """
        Retrieves the current state of Kill Switch firewall rules.
        Machine-readable format for agents and CLI.
        """
        ps_cmd = (
            f"Get-NetFirewallRule -DisplayName '{cls.RULE_PREFIX}*' -ErrorAction SilentlyContinue "
            "| Select-Object Name, DisplayName, Enabled, Direction, Action "
            "| ConvertTo-Json -Compress"
        )
        rules = []
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout.strip())
                if isinstance(data, list):
                    rules = data
                elif isinstance(data, dict):
                    rules = [data]
        except Exception:
            pass

        binaries = cls.get_antigravity_binaries()
        physical_adapters = cls.get_physical_adapters()
        is_enabled = len(rules) > 0 and all(r.get("Enabled") == 1 or r.get("Enabled") is True for r in rules)

        return {
            "is_admin": is_admin(),
            "kill_switch_enabled": is_enabled,
            "active_rules_count": len(rules),
            "physical_adapters": physical_adapters,
            "protected_binaries": binaries,
            "rules": rules,
            "message": (
                "کیل‌سوئیچ فایروال فعال است: ترافیک اینترنت در صورت قطع VPN از کارت شبکه فیزیکی نشت نخواهد کرد."
                if is_enabled
                else "کیل‌سوئیچ فایروال خاموش است: ترافیک به صورت عادی عبور می‌کند."
            ),
        }

    @classmethod
    def enable(cls, elevate_if_needed: bool = True) -> Dict[str, Any]:
        """
        Creates Outbound Block firewall rules for Antigravity binaries on physical network adapters.
        Requires Administrator privileges.
        """
        if not is_admin():
            if elevate_if_needed:
                return cls._run_elevated("enable")
            return {
                "success": False,
                "error": "ADMIN_REQUIRED",
                "message": "برای تنظیم رول‌های فایروال ویندوز دسترسی Administrator لازم است.",
            }

        binaries = cls.get_antigravity_binaries()
        if not binaries:
            return {
                "success": False,
                "error": "NO_BINARIES_FOUND",
                "message": "فایل‌های اجرایی Antigravity در مسیرهای استاندارد یافت نشدند.",
            }

        adapters = cls.get_physical_adapters()
        created_rules = []

        # First clean up any old rules to ensure idempotency
        cls.disable(elevate_if_needed=False)

        for binary in binaries:
            bin_name = os.path.basename(binary).replace(".exe", "")
            for adapter in adapters:
                rule_name = f"{cls.RULE_PREFIX}-{adapter}-{bin_name}"
                ps_cmd = (
                    f"New-NetFirewallRule -DisplayName '{rule_name}' "
                    f"-Direction Outbound -Action Block "
                    f"-Program '{binary}' -InterfaceAlias '{adapter}' "
                    f"-Profile Any -Description 'Antigravity Pause KillSwitch: Block leaks on physical {adapter}'"
                )
                try:
                    res = subprocess.run(
                        ["powershell", "-NoProfile", "-Command", ps_cmd],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                    )
                    if res.returncode == 0:
                        created_rules.append(rule_name)
                except Exception as e:
                    return {
                        "success": False,
                        "error": str(e),
                        "message": f"خطا در ایجاد رول برای {rule_name}",
                    }

        return {
            "success": True,
            "created_rules": created_rules,
            "message": f"کیل‌سوئیچ با موفقیت فعال شد. {len(created_rules)} رول ضد نشت در فایروال ویندوز ثبت گردید.",
        }

    @classmethod
    def disable(cls, elevate_if_needed: bool = True) -> Dict[str, Any]:
        """
        Removes all Antigravity Kill Switch firewall rules cleanly.
        """
        if not is_admin():
            if elevate_if_needed:
                return cls._run_elevated("disable")
            return {
                "success": False,
                "error": "ADMIN_REQUIRED",
                "message": "برای حذف رول‌های فایروال ویندوز دسترسی Administrator لازم است.",
            }

        ps_cmd = (
            f"Remove-NetFirewallRule -DisplayName '{cls.RULE_PREFIX}*' "
            "-ErrorAction SilentlyContinue"
        )
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return {
                "success": res.returncode == 0,
                "message": "کیل‌سوئیچ غیرفعال شد و تمامی رول‌های مربوطه از فایروال حذف شدند.",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def _run_elevated(cls, action: str) -> Dict[str, Any]:
        """Triggers UAC prompt to execute the action with Administrator rights."""
        script_path = os.path.abspath(__file__)
        python_exe = sys.executable
        # Wrap execution in elevated PowerShell
        elevate_cmd = (
            f"Start-Process '{python_exe}' -ArgumentList '\"{script_path}\" {action}' "
            "-Verb RunAs -Wait"
        )
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", elevate_cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if res.returncode == 0:
                # Check status afterwards
                status = cls.get_status()
                return {
                    "success": True,
                    "elevated": True,
                    "message": f"فرمان {action} با دسترسی Administrator اجرا گردید.",
                    "status": status,
                }
            return {
                "success": False,
                "error": "ELEVATION_FAILED",
                "message": "مجوز دسترسی ادمین (UAC) توسط کاربر رد شد یا با خطا متوقف گردید.",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "enable":
        out = AntigravityKillSwitch.enable()
    elif action == "disable":
        out = AntigravityKillSwitch.disable()
    elif action == "status":
        out = AntigravityKillSwitch.get_status()
    else:
        out = {"error": f"دستور ناشناخته: {action}. دستورات معتبر: status, enable, disable"}

    print(json.dumps(out, ensure_ascii=False, indent=2))
