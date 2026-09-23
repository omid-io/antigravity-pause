"""
antigravity-pause: One-Click Installer for Antigravity 2 Desktop & IDE
Installs and registers /pause and /hibernate slash commands into Antigravity global configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def install():
    print("=" * 60)
    print("🚀 نصب و فعال‌سازی antigravity-pause برای Antigravity 2 Desktop")
    print("=" * 60)

    repo_root = Path(__file__).parent.resolve()
    skills_source = repo_root / "skills"
    pause_src = skills_source / "pause"
    hibernate_src = skills_source / "hibernate"

    if not pause_src.exists() or not hibernate_src.exists():
        print(f"❌ خطا: پوشه‌های اسکیل در {skills_source} یافت نشدند.")
        return 1

    # Target: ~/.gemini/config/skills
    gemini_config_dir = Path.home() / ".gemini" / "config" / "skills"
    gemini_config_dir.mkdir(parents=True, exist_ok=True)

    skills_to_link = {
        "pause": pause_src,
        "hibernate": hibernate_src,
    }

    for skill_name, src_path in skills_to_link.items():
        dest_link = gemini_config_dir / skill_name
        if dest_link.exists() or dest_link.is_symlink():
            print(f"🔄 اتصال قبلی برای {skill_name} یافت شد؛ در حال به‌روزرسانی...")
            try:
                if dest_link.is_dir() and not dest_link.is_symlink():
                    import shutil
                    shutil.rmtree(dest_link)
                else:
                    dest_link.unlink(missing_ok=True)
            except Exception as e:
                # If junction in Windows
                subprocess.run(f'cmd /c rmdir "{dest_link}"', shell=True, capture_output=True)

        print(f"🔗 ایجاد Junction برای {skill_name} -> {src_path}")
        cmd = f'cmd /c mklink /J "{dest_link}" "{src_path}"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"✅ اسکیل {skill_name} با موفقیت در Antigravity ثبت شد.")
        else:
            print(f"⚠️ ایجاد Junction با روش cmd ناموفق بود ({res.stderr.strip()}). استفاده از روش پایتون...")
            try:
                os.symlink(src_path, dest_link, target_is_directory=True)
                print(f"✅ اسکیل {skill_name} با Symlink ثبت شد.")
            except Exception as e:
                print(f"❌ خطا در ثبت {skill_name}: {e}")

    print("\n🔍 در حال اجرای تست سلامت شبکه و ضد نشت آی‌پی...")
    probe_script = repo_root / "cli.py"
    subprocess.run([sys.executable, str(probe_script), "probe"])

    print("\n" + "=" * 60)
    print("🎉 نصب با موفقیت تکمیل شد!")
    print("اکنون در Antigravity 2 Desktop می‌توانید از دستورات زیر استفاده کنید:")
    print("  /pause     -> ایست گرم و سکوت رادیویی هنگام تعویض وی‌پی‌ان یا اسلیپ")
    print("  /play      -> بررسی سلامت و ادامه کار بدون باختن کانتکست")
    print("  /hibernate -> خواب عمیق، ذخیره چک‌پوینت و بستن تمیز برنامه‌ها")
    print("  /continue  -> بازسازی چک‌پوینت و ادامه تسک از همان نقطه")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(install())
