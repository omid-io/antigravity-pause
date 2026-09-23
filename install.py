"""
antigravity-pause: Universal Cross-Platform Installer
Installs Skills, Workflows/Actions, and Manifests into Antigravity on ANY machine.
Dynamically resolves local paths so other users can clone and run with zero configuration.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def patch_content_paths(content: str, target_root: Path) -> str:
    """Replaces any static path references with the dynamic local repo_root."""
    old_patterns = [
        "E:\\programming\\Tools\\antigravity-pause",
        "E:/programming/Tools/antigravity-pause",
        "E:\\programming\\antigravity-pause",
        "E:/programming/antigravity-pause",
        "{{ANTIGRAVITY_PAUSE_ROOT}}",
    ]
    new_path = str(target_root)
    # Ensure proper escaping for Windows
    for pattern in old_patterns:
        content = content.replace(pattern, new_path)
    return content


def install():
    print("=" * 68)
    print("🚀 نصب و فعال‌سازی خودکار antigravity-pause برای Antigravity 2 Desktop & IDE")
    print("=" * 68)

    repo_root = Path(__file__).parent.resolve()
    gemini_config_dir = Path.home() / ".gemini" / "config"

    # Patch local skill files in-place to match this machine's exact path
    skills_source = repo_root / "skills"
    for skill_file in skills_source.rglob("*.md"):
        try:
            raw = skill_file.read_text(encoding="utf-8")
            patched = patch_content_paths(raw, repo_root)
            if patched != raw:
                skill_file.write_text(patched, encoding="utf-8")
        except Exception:
            pass

    # 1. Register Skills
    gemini_skills_dir = gemini_config_dir / "skills"
    gemini_skills_dir.mkdir(parents=True, exist_ok=True)

    skills_to_link = {
        "pause": skills_source / "pause",
        "hibernate": skills_source / "hibernate",
        "killswitch": skills_source / "killswitch",
    }

    print("\n📦 [1/3] در حال ثبت مهارت‌های پردازشی (Skills)...")
    for skill_name, src_path in skills_to_link.items():
        dest_link = gemini_skills_dir / skill_name
        if dest_link.exists() or dest_link.is_symlink():
            if os.name == "nt":
                subprocess.run(f'cmd /c rmdir "{dest_link}"', shell=True, capture_output=True)
            if dest_link.exists():
                try:
                    if dest_link.is_dir() and not dest_link.is_symlink():
                        shutil.rmtree(dest_link, ignore_errors=True)
                    else:
                        dest_link.unlink(missing_ok=True)
                except Exception:
                    pass

        # Try junction on Windows, otherwise standard symlink
        linked = False
        if os.name == "nt":
            res = subprocess.run(f'cmd /c mklink /J "{dest_link}" "{src_path}"', shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  ✅ اسکیل {skill_name} از طریق Junction متصل شد.")
                linked = True

        if not linked:
            try:
                os.symlink(src_path, dest_link, target_is_directory=True)
                print(f"  ✅ اسکیل {skill_name} از طریق Symlink متصل شد.")
                linked = True
            except Exception:
                # Fallback: copy tree if permissions restrict symlinks
                shutil.copytree(src_path, dest_link, dirs_exist_ok=True)
                print(f"  ✅ اسکیل {skill_name} کپی و ثبت شد.")

    # 2. Register Workflows (Chat UI / Slash Actions)
    print("\n⚡ [2/3] در حال ثبت اکشن‌های منوی چت (Workflows & Slash Actions)...")
    wf_src = repo_root / "workflows"
    wf_targets = [
        gemini_config_dir / "workflows",
        gemini_config_dir / "global_workflows",
    ]

    for target_dir in wf_targets:
        target_dir.mkdir(parents=True, exist_ok=True)
        for md_file in wf_src.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            patched_content = patch_content_paths(content, repo_root)
            (target_dir / md_file.name).write_text(patched_content, encoding="utf-8")
        print(f"  ✅ اکشن‌ها با مسیر محلی در {target_dir.name} ثبت شدند.")

    # 3. Register workflows.json Manifest
    manifest_src = repo_root / "workflows.json"
    if manifest_src.exists():
        shutil.copy2(manifest_src, gemini_config_dir / "workflows.json")
        print(f"  ✅ مانیفست workflows.json در کانفیگ سراسری ثبت شد.")

    # 4. Run Pre-flight Network Probe Test
    print("\n🔍 [3/3] در حال اجرای تست سلامت شبکه و ضد نشت آی‌پی...")
    probe_script = repo_root / "cli.py"
    subprocess.run([sys.executable, str(probe_script), "probe"])

    print("\n" + "=" * 68)
    print("🎉 نصب با موفقیت کامل روی این سیستم انجام شد!")
    print(f"📍 مسیر شناسایی‌شده پروژه: {repo_root}")
    print("اکنون دستورات زیر در کادر چت Antigravity (با تایپ /) فعال هستند:")
    print("  /pause      -> ایست گرم، سکوت رادیویی و حفظ کانتکست")
    print("  /play       -> بررسی سلامت اتصال و ادامه فوری کار")
    print("  /hibernate  -> خواب عمیق دیسک، ثبت چک‌پوینت و بستن برنامه‌ها")
    print("  /continue   -> لود چک‌پوینت و ادامه تسک از گام بعدی")
    print("  /killswitch -> مدیریت کیل‌سوئیچ فایروال ویندوز و تست نشت آی‌پی")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(install())
