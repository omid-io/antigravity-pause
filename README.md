# ⏸️ antigravity-pause

> **Graceful Pause, Deep Hibernation & Pre-Flight Leak Protection for Google Antigravity (2.0 Desktop, IDE, and CLI).**  
> Protect your active AI agent sessions from `ECONNRESET`, geoblock `403 Forbidden` errors, orphaned processes, and corrupted Git locks during VPN switches, network changes, or system sleep.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)]()
[![Platform: Windows%20%7C%20Linux%20%7C%20macOS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Antigravity: 2.0+ Compatible](https://img.shields.io/badge/Antigravity-2.0+-orange.svg)]()

[English](#-antigravity-pause) | [فارسی (Persian)](#-راهنمای-فارسی)

---

## 🌍 The Problem

Autonomous AI coding agents rely on continuous HTTP/2 connections and Server-Sent Event (SSE) streams. In volatile network environments—such as toggling corporate VPNs, switching between Wi-Fi and mobile hotspots, putting laptops to sleep, or operating in heavily geoblocked and censored regions (e.g. Iran)—any network transition abruptly breaks active TCP sockets.

This leads to:
* **Terminal Crashes (`ECONNRESET` / `Broken pipe`):** Live model streams drop immediately without saving intermediate progress.
* **Geoblock Sanction Penalties (`403 Forbidden` / `FAILED_PRECONDITION`):** Brief IP leaks during VPN handshakes cause API gateways to blacklist the active session.
* **Orphaned Background Subagents:** Background processes remain stuck consuming CPU and memory.
* **Corrupted Git Locks:** Abrupt termination during write operations leaves behind unremovable `.git/index.lock` files, preventing future commits.

---

## 💡 The Solution

**`antigravity-pause`** equips Antigravity with two smart slash-command workflows:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          1. Hot Standby (Zero-Kill)                         │
│                                                                             │
│   /pause  ──► Radio silence + light sleep for subagents (preserves state)   │
│   /play   ──► <200ms anti-leak pre-flight probe + instant task resumption   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      2. Deep Hibernation (Disk Snapshot)                    │
│                                                                             │
│   /hibernate ──► Atomic checkpoint saved + git locks freed + clean shutdown │
│   /continue  ──► Network probe verified + state rehydrated from next step   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Key Features

1. **Sub-second Pre-Flight Leak Probe (`<200ms`):**
   * High-speed, lightweight Python probe validates connectivity and verifies non-sanctioned geo-location before initiating any model requests. If an IP leak or network outage is detected, the agent safely holds back, avoiding `403 Forbidden` session drops.
2. **Zero-Kill Hot Standby (`/pause`):**
   * Sets parent agent and subagents into an idle `waiting_for_message` state without killing process trees. Preserves in-memory conversation context and zeroes network traffic while you switch VPN servers.
3. **Atomic State Checkpointing (`/hibernate`):**
   * Saves multi-agent progress, conversation metadata, and execution steps into an atomic JSON snapshot resistant to sudden power loss or reboots.
4. **Git Lock Sanitizer:**
   * Automatically detects and removes orphaned `.git/index.lock` files caused by interrupted git commands.
5. **Universal Compatibility:**
   * Native plug-and-play support for **Antigravity 2.0 Desktop**, **Antigravity IDE**, and the **`agy` CLI**.

---

## 🚀 Installation / نحوه نصب

### 🤖 Method 1: Ask Your Antigravity Agent (Recommended)
You can directly tell your Antigravity agent in any chat:
> *"Please clone https://github.com/omid-io/antigravity-pause.git and run `python install.py` to enable /pause and /hibernate commands in my desktop."*

### 💻 Method 2: Manual Terminal Setup
```bash
git clone https://github.com/omid-io/antigravity-pause.git
cd antigravity-pause
python install.py
```
*(On Windows, you can simply double-click `setup.bat`).*

The installer dynamically resolves paths for your operating system (Windows, Linux, macOS), registers the chat slash actions in `~/.gemini/config/workflows/`, and links the background resilience skills into `~/.gemini/config/skills/`.

---

## 📖 How to Use

### Scenario 1: Switching VPN or Quick Laptop Sleep
1. In your Antigravity chat, type:
   ```text
   /pause
   ```
   *The agent enters radio silence and confirms it is safe to disconnect/change network.*
2. Toggle your VPN, change network adapters, or close your laptop lid.
3. Once your connection is established, type:
   ```text
   /play
   ```
   *(Or simply say: "continue").*  
   *The pre-flight probe verifies connection integrity and resumes the task right where it left off.*

### Scenario 2: System Shutdown or Closing Antigravity
1. In your chat, type:
   ```text
   /hibernate
   ```
   *All subagents and task states are atomized into a checkpoint file and processes exit cleanly.*
2. Safely shut down or reboot your PC.
3. In a new session, type:
   ```text
   /continue
   ```
   *The previous checkpoint is loaded, subagents are rehydrated, and execution resumes seamlessly.*

---

## 🛠️ CLI Usage

You can also run the core modules standalone for quick diagnostics:

```powershell
# Run the fast network & anti-leak probe
python cli.py probe

# Clean lingering .git/index.lock files
python cli.py clean-locks

# Inspect the active checkpoint
python cli.py checkpoint-load
```

---

## 📂 Repository Structure

```
antigravity-pause/
├── core/
│   ├── network_probe.py    # Ultra-fast (<200ms) anti-leak network probe
│   ├── engine.py           # Atomic checkpointing and state persistence
│   └── process_guard.py    # Safe subagent freezing and git lock cleanup
├── skills/
│   ├── pause/SKILL.md      # /pause and /play skill definitions
│   └── hibernate/SKILL.md  # /hibernate and /continue skill definitions
├── cli.py                  # Standalone CLI diagnostic tool
├── install.py              # Automated installer & skill linker
├── setup.bat               # 1-click Windows runner
├── LICENSE                 # MIT License
└── README.md
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). Free and open-source for all developers.

---
---

## 🇮🇷 راهنمای فارسی

> **سیستم هوشمند مدیریت پاز، فریز وضعیت (چک‌پوینت)، تست سلامت اتصال و مهار نشت آی‌پی برای Antigravity (دسکتاپ ۲، IDE و CLI).**

### 🌍 مسأله چیست؟
دستیارهای کدنویسی هوش مصنوعی به جریان‌های زنده HTTP/2 و Server-Sent Events (SSE) متکی هستند. در شرایط ناپایدار شبکه—مانند نیاز به تعویض سرور فیلترشکن، سوییچ بین وای‌فای و هات‌اسپات، اسلیپ کردن لپ‌تاپ یا قطع و وصل ناگهانی اینترنت در ایران—هرگونه تغییر شبکه بلافاصله سوکت فعال را قطع می‌کند.

پیامدهای این مسأله:
* **خطای قرمز `ECONNRESET`:** قطع شدن ناگهانی استریم و از دست رفتن پاسخ‌های در حال تولید.
* **خطای تحریم `403 Forbidden` / `FAILED_PRECONDITION`:** نشت میلی‌ثانیه‌ای آی‌پی ایران حین هندشیک فیلترشکن که به مسدود شدن موقت سشن منجر می‌شود.
* **ساب‌ایجنت‌های معلق (Orphan Processes):** مصرف مداوم رم و پردازنده توسط تسک‌های بلاتکلیف پس‌زمینه.
* **قفل‌های خراب گیت:** ماندن فایل مزاحم `.git/index.lock` در دیسک به دلیل خروج اضطراری در حین عملیات‌های نوشتن.

---

### 💡 راه‌حل
ابزار **`antigravity-pause`** دو جفت اسلش‌کامند هوشمند به Antigravity اضافه می‌کند:

1. **ایست گرم بدون کشتن پروسه (Hot Standby):**
   * `/pause`: سکوت رادیویی و خواب سبک والد و ساب‌ایجنت‌ها بدون بستن پروسه‌ها یا خالی شدن رم.
   * `/play`: تست ۲۰۰ میلی‌ثانیه‌ای ضد نشت IP و ادامه فوری کار بدون هدررفت کانتکست.
2. **خواب عمیق دیسک (Deep Hibernation):**
   * `/hibernate`: ثبت اتمیک وضعیت، پاکسازی قفل‌های گیت و بستن تمیز تمام برنامه‌ها برای خاموش کردن سیستم.
   * `/continue`: تست اتصال شبکه، بازسازی وضعیت و ساب‌ایجنت‌ها و ادامه پروژه از گام بعدی.

---

### ⚡ ویژگی‌های برجسته
* **پروب فوق‌سریع ضد نشت IP (زیر ۲۰۰ میلی‌ثانیه):** بررسی زنده کشور آی‌پی و پایداری اتصال پیش از ارسال هر پیام به هوش مصنوعی تا از خطای ۴۰۳ جلوگیری شود.
* **ذخیره اتمیک (Atomic Snapshot):** بدون نگرانی از خرابی فایل حتی در صورت خاموش شدن ناگهانی سیستم یا قطعی برق.
* **پاکسازی خودکار قفل گیت (Git Lock Sanitizer):** برطرف کردن خودکار ارورهای `.git/index.lock` پس از قطع غیرمنتظره اینترنت.
* **سازگاری کامل:** قابل استفاده در **Antigravity 2.0 Desktop**، محیط **Antigravity IDE** و خط‌فرمان **`agy` CLI**.

---

### 🚀 راهنمای نصب
در محیط ویندوز تنها کافی است فایل `setup.bat` را اجرا کنید یا دستور زیر را در ترمینال بزنید:

```powershell
python install.py
```

این اسکریپت مهارت‌ها را مستقیماً از طریق Junction در پوشه کانفیگ سراسری Antigravity (`~/.gemini/config/skills/`) ثبت می‌کند و دستورات در تمام چت‌ها بلافاصله آماده استفاده خواهند بود.

---

### 📖 نحوه استفاده در سناریوهای روزمره

#### سناریو ۱: تعویض فیلترشکن، تغییر سرور یا اسلیپ کوتاه سیستم
1. در چت تایپ کنید:
   ```text
   /pause
   ```
   *ایجنت فوراً به حالت سکوت می‌رود و منتظر تغییر شبکه می‌ماند.*
2. فیلترشکن را تغییر دهید یا شبکه را عوض کنید.
3. در چت تایپ کنید:
   ```text
   /play
   ```
   *(یا بنویسید: «ادامه بده»). ایجنت پروب شبکه را تست کرده و فوراً کار را ادامه می‌دهد.*

#### سناریو ۲: خاموش کردن سیستم یا بستن کامل نرم‌افزار
1. در چت بنویسید:
   ```text
   /hibernate
   ```
   *اسنپ‌شات کامل ذخیره شده، قفل‌ها تمیز شده و کار متوقف می‌شود.*
2. سیستم را خاموش کنید.
3. بعد از روشن کردن، در چت جدید بنویسید:
   ```text
   /continue
   ```
   *چک‌پوینت لود شده و تسک از ادامه گام قبلی به صورت خودکار پیش می‌رود.*

---

### 🛠️ ابزارهای خط فرمان (CLI)
برای اجرای سریع و تست مستقل ماژول‌ها:

```powershell
# تست پایداری و سلامت نشت آی‌پی
python cli.py probe

# پاکسازی قفل‌های معلق گیت
python cli.py clean-locks

# بررسی و بارگذاری آخرین چک‌پوینت فعال
python cli.py checkpoint-load
```

---

### 📜 مجوز و لایسنس
این پروژه تحت پروانه [MIT License](LICENSE) منتشر شده و استفاده از آن برای تمام برنامه‌نویسان آزاد و رایگان است.
