"""
antigravity-pause: Complete One-Click Installer
Installs Skills, Workflows/Actions, and Manifests into Antigravity so that
/pause, /play, /hibernate, and /continue appear natively in the chat popup menu.
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


def install():
    print("=" * 65)
    print("🚀 نصب و فعال‌سازی antigravity-pause برای Antigravity 2 Desktop & IDE")
    print("=" * 65)

    repo_root = Path(__file__).parent.resolve()
    gemini_config_dir = Path.home() / ".gemini" / "config"

    # 1. Register Skills via Junctions
    skills_source = repo_root / "skills"
    gemini_skills_dir = gemini_config_dir / "skills"
    gemini_skills_dir.mkdir(parents=True, exist_ok=True)

    skills_to_link = {
        "pause": skills_source / "pause",
        "hibernate": skills_source / "hibernate",
    }

    print("\n📦 [1/3] در حال ثبت مهارت‌های پردازشی (Skills)...")
    for skill_name, src_path in skills_to_link.items():
        dest_link = gemini_skills_dir / skill_name
        if dest_link.exists() or dest_link.is_symlink():
            subprocess.run(f'cmd /c rmdir "{dest_link}"', shell=True, capture_output=True)
            if dest_link.exists():
                shutil.rmtree(dest_link, ignore_errors=True)

        res = subprocess.run(f'cmd /c mklink /J "{dest_link}" "{src_path}"', shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  ✅ اسکیل {skill_name} متصل شد.")
        else:
            try:
                os.symlink(src_path, dest_link, target_is_directory=True)
                print(f"  ✅ اسکیل {skill_name} با Symlink متصل شد.")
            except Exception as e:
                print(f"  ⚠️ خطا در اتصال {skill_name}: {e}")

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
            shutil.copy2(md_file, target_dir / md_file.name)
        print(f"  ✅ اکشن‌ها در {target_dir.name} کپی و ثبت شدند.")

    # 3. Register workflows.json Manifest
    manifest_src = repo_root / "workflows.json"
    if manifest_src.exists():
        shutil.copy2(manifest_src, gemini_config_dir / "workflows.json")
        print(f"  ✅ مانیفست workflows.json در کانفیگ ثبت گردید.")

    # 4. Run Pre-flight Network Probe Test
    print("\n🔍 [3/3] در حال اجرای تست سلامت شبکه و ضد نشت آی‌پی...")
    probe_script = repo_root / "cli.py"
    subprocess.run([sys.executable, str(probe_script), "probe"])

    print("\n" + "=" * 65)
    print("🎉 نصب با موفقیت کامل انجام شد!")
    print("اکنون دستورات زیر در منوی اسلش (با تایپ /) فعال هستند:")
    print("  /pause     -> ایست گرم، سکوت رادیویی و حفظ کانتکست")
    print("  /play      -> بررسی سلامت اتصال و ادامه فوری کار")
    print("  /hibernate -> خواب عمیق دیسک، ثبت چک‌پوینت و بستن برنامه‌ها")
    print("  /continue  -> لود چک‌پوینت و ادامه تسک از گام بعدی")
    print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(install())
