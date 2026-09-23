# ⏸️ antigravity-pause

> **Graceful Pause, Deep Hibernation & Pre-Flight Leak Protection for Google Antigravity (2.0 Desktop, IDE, and CLI).**  
> Protect your active AI agent sessions from `ECONNRESET`, geoblock `403 Forbidden` errors, orphaned processes, and corrupted Git locks during VPN switches, network changes, or system sleep. Includes an optional hardware-level **Windows Firewall Kill Switch** to block IP leaks when VPN TUN drops.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)]()
[![Platform: Windows%20%7C%20Linux%20%7C%20macOS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Antigravity: 2.0+ Compatible](https://img.shields.io/badge/Antigravity-2.0+-orange.svg)]()

[English](#-antigravity-pause) | [فارسی (Persian)](#-راهنمای-فارسی)

---

## ⚡ 1-Click Agent Install Prompt

Simply copy and paste this single prompt directly into your Antigravity chat:

```text
Please clone https://github.com/omid-io/antigravity-pause.git and run python install.py to equip Antigravity with /pause, /play, /hibernate, and /killswitch skills.
```

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

**`antigravity-pause`** equips Antigravity with smart slash-command workflows:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          1. Hot Standby (Zero-Kill)                         │
│                                                                             │
│   /pause       ──► Radio silence + light sleep for subagents (preserves RAM)│
│   /play        ──► <200ms anti-leak pre-flight probe + instant resumption  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      2. Deep Hibernation (Disk Snapshot)                    │
│                                                                             │
│   /hibernate   ──► Atomic checkpoint saved + git locks freed + clean exit   │
│   /continue    ──► Network probe verified + state rehydrated from next step │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│               3. Hardware-Level Kill Switch (Anti-Leak Firewall)            │
│                                                                             │
│   /killswitch  ──► Windows Firewall Outbound Block on physical adapters     │
│                    (Wi-Fi, Ethernet). If VPN drops, 0 bytes leak to Iran ISP│
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
4. **Hardware-Level Windows Firewall Kill Switch (`/killswitch`):**
   * Optional manual toggle that creates Windows Defender Firewall Outbound Block rules for Antigravity processes on physical adapters (`Wi-Fi`, `Ethernet`). If your VPN TUN drops unexpectedly, Windows drops the packets locally at the kernel level—zero bytes leak to your local ISP.
5. **Git Lock Sanitizer:**
   * Automatically detects and removes orphaned `.git/index.lock` files caused by interrupted git commands.
6. **Universal Compatibility & Machine-Friendly CLI:**
   * Native plug-and-play support for **Antigravity 2.0 Desktop**, **Antigravity IDE**, and the **`agy` CLI**. All commands support `--json` for effortless subagent introspection.

---

## 🚀 Installation

### 🤖 Method 1: Ask Your Antigravity Agent (Recommended)
Paste this into your Antigravity chat:
> *"Please clone https://github.com/omid-io/antigravity-pause.git and run `python install.py` to enable /pause, /hibernate, and /killswitch in my environment."*

### 💻 Method 2: Manual Terminal Setup
```bash
git clone https://github.com/omid-io/antigravity-pause.git
cd antigravity-pause
python install.py
```
*(On Windows, you can simply double-click `setup.bat`).*

---

## 🛡️ Windows Firewall Kill Switch Guide

The Kill Switch is **strictly manual & optional** (disabled by default). Users outside restricted zones do not need it, while developers in Iran or geo-fenced environments can turn it on with one command.

### How to Control:

#### Option A: Inside Antigravity Chat
* `/killswitch status` — Check whether the firewall shield is active.
* `/killswitch on` — Enable Outbound Block rules on Wi-Fi and Ethernet.
* `/killswitch off` — Cleanly remove firewall rules and restore default routing.

#### Option B: Desktop 1-Click Batch Files
* Double-click `enable_killswitch.bat` (requests Administrator permission and enables rules).
* Double-click `disable_killswitch.bat` (removes rules).

#### Option C: CLI (Machine-Friendly for Agents)
```powershell
# Check status (pure JSON)
python cli.py killswitch status --json

# Enable rules
python cli.py killswitch enable

# Disable rules
python cli.py killswitch disable
```

---

## 📖 Everyday Scenarios

### Scenario 1: Switching VPN or Quick Laptop Sleep
1. In your chat, type `/pause`. The agent enters radio silence.
2. Toggle your VPN, change Wi-Fi, or put your laptop to sleep.
3. Type `/play` (or say "continue"). The pre-flight probe verifies connection integrity and resumes the task instantly.

### Scenario 2: System Shutdown or Closing Antigravity
1. In your chat, type `/hibernate`. Subagents and tasks are saved into an atomic checkpoint.
2. Shut down or reboot your PC.
3. In a new session, type `/continue`. State rehydrates and continues from the next step.

---

## 🛠️ CLI Usage

```powershell
# Run the fast network & anti-leak probe
python cli.py probe

# Check Kill Switch status (formatted or JSON)
python cli.py killswitch status
python cli.py killswitch status --json

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
│   ├── network_probe.py      # Ultra-fast (<200ms) anti-leak network probe
│   ├── engine.py             # Atomic checkpointing and state persistence
│   ├── process_guard.py      # Safe subagent freezing and git lock cleanup
│   └── kill_switch.py        # Windows Firewall Outbound Kill Switch engine
├── skills/
│   ├── pause/SKILL.md        # /pause and /play skill definitions
│   ├── hibernate/SKILL.md    # /hibernate and /continue skill definitions
│   └── killswitch/SKILL.md   # /killswitch skill definition
├── cli.py                    # Standalone CLI diagnostic & agent control tool
├── install.py                # Automated installer & skill linker
├── setup.bat                 # 1-click Windows installer
├── enable_killswitch.bat     # 1-click elevated Kill Switch activation
├── disable_killswitch.bat    # 1-click elevated Kill Switch deactivation
├── LICENSE                   # MIT License
└── README.md
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). Free and open-source for all developers.

---
---

## 🇮🇷 راهنمای فارسی

> **سیستم هوشمند مدیریت پاز، فریز وضعیت (چک‌پوینت)، تست سلامت اتصال، رفع نشت آی‌پی و کیل‌سوئیچ فایروال برای Antigravity (دسکتاپ ۲، IDE و CLI).**

---

### ⚡ نصب خودکار با یک دستور به ایجنت (پیشنهادی)

کافی است متن زیر را کپی کرده و در کادر چت Antigravity بفرستید:

```text
لطفاً ریپازیتوری https://github.com/omid-io/antigravity-pause.git را کلون کن و با اجرای دستور python install.py قابلیت‌های /pause، /play، /hibernate و /killswitch را روی سیستم من نصب و فعال کن.
```

---

### 🌍 مسأله چیست؟
دستیارهای کدنویسی هوش مصنوعی به جریان‌های زنده HTTP/2 و Server-Sent Events (SSE) متکی هستند. در شرایط ناپایدار شبکه—مانند نیاز به تعویض سرور فیلترشکن، سوییچ بین وای‌فای و هات‌اسپات، اسلیپ کردن لپ‌تاپ یا قطع ناگهانی تونل VPN در ایران—هرگونه تغییر شبکه بلافاصله سوکت فعال را قطع می‌کند.

اگر فیلترشکن قطع شود، ویندوز به طور پیش‌فرض ترافیک را به کارت شبکه فیزیکی (وای‌فای/مودم ایران) می‌فرستد. در نتیجه پکت بعدی با آی‌پی ایران به گوگل رسیده و خطای **۴۰۳ Geoblock** سشن کاری را متوقف می‌کند.

---

### 💡 راه‌حل
ابزار **`antigravity-pause`** سه راهکار هماهنگ ارائه می‌دهد:

1. **ایست گرم بدون بستن پروسه (Hot Standby):**
   * `/pause`: سکوت رادیویی و خواب سبک والد و ساب‌ایجنت‌ها بدون بستن پروسه‌ها یا خالی شدن رم.
   * `/play`: تست ۲۰۰ میلی‌ثانیه‌ای ضد نشت IP و ادامه فوری کار بدون هدررفت کانتکست.
2. **خواب عمیق دیسک (Deep Hibernation):**
   * `/hibernate`: ثبت اتمیک وضعیت، پاکسازی قفل‌های گیت و بستن تمیز برنامه‌ها برای خاموش کردن سیستم.
   * `/continue`: تست اتصال، بازسازی وضعیت و ساب‌ایجنت‌ها و ادامه پروژه از گام بعدی.
3. **کیل‌سوئیچ فایروال ویندوز (Windows Firewall Kill Switch):**
   * `/killswitch`: مسدودسازی ترافیک خروجی Antigravity روی کارت‌های فیزیکی (`Wi-Fi` و `Ethernet`) در فایروال ویندوز. در صورت قطعی ناگهانی VPN، حتی یک بایت هم از اینترنت ایران خارج نمی‌شود و گوگل متوجه آی‌پی ایران نخواهد شد.

---

### 🛡️ راهنمای فعال‌سازی دستی کیل‌سوئیچ (اختیاری)

این قابلیت **کاملاً اختیاری و دستی (Manual Toggle)** است تا کاربران بین‌المللی دچار محدودیت نشوند و برنامه‌نویسان داخل ایران بتوانند در صورت تمایل آن را روشن کنند.

#### روش‌های کنترل:
* **در چت Antigravity:**
  * تایپ `/killswitch on` یا `/killswitch enable` برای فعال‌سازی.
  * تایپ `/killswitch off` یا `/killswitch disable` برای غیرفعال‌سازی.
  * تایپ `/killswitch status` برای استعلام وضعیت.
* **فایل‌های یک‌کلیکی ویندوز:**
  * اجرای فایل `enable_killswitch.bat` برای روشن کردن.
  * اجرای فایل `disable_killswitch.bat` برای خاموش کردن.
* **خط‌فرمان (مخصوص اتوماسیون و ایجنت‌ها):**
  ```powershell
  python cli.py killswitch status --json
  python cli.py killswitch enable
  python cli.py killswitch disable
  ```

---

### 🚀 راهنمای نصب دستی
در محیط ویندوز فایل `setup.bat` را اجرا کرده یا در ترمینال بزنید:

```powershell
python install.py
```

---

### 📜 مجوز و لایسنس
این پروژه تحت پروانه [MIT License](LICENSE) منتشر شده و استفاده از آن برای تمام برنامه‌نویسان آزاد و رایگان است.
