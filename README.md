<p align="center">
  <img src="assets/banner.webp" alt="antigravity-pause banner" width="100%" />
</p>

<p align="center">
  <strong>Graceful Standby, Deep Hibernation & Pre-Flight Leak Protection for Google Antigravity</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/badge/Antigravity-2.0+-orange.svg?style=flat-square" alt="Antigravity 2.0+" />
  <a href="#-راهنمای-فارسی"><img src="https://img.shields.io/badge/%D9%81%D8%A7%D8%B1%D8%B3%D9%8A-Persian-4B0082.svg?style=flat-square" alt="Persian Guide" /></a>
</p>

<p align="center">
  <a href="#-quick-agent-install">Quick Install</a> •
  <a href="#-the-problem">The Problem</a> •
  <a href="#-core-workflows">Workflows</a> •
  <a href="#-hardware-kill-switch">Kill Switch</a> •
  <a href="#-cli-reference">CLI</a> •
  <a href="#-راهنمای-فارسی">راهنمای فارسی</a>
</p>

---

## ⚡ Quick Agent Install

Install in 1 step by pasting this prompt directly into your Antigravity chat:

> **Copy & Paste to Antigravity:**  
> `Please clone https://github.com/omid-io/antigravity-pause.git and run python install.py to equip Antigravity with /pause, /play, /hibernate, and /killswitch skills.`

Or run manually in your terminal:
```bash
git clone https://github.com/omid-io/antigravity-pause.git
cd antigravity-pause
python install.py
```
*(On Windows, you can also simply double-click `setup.bat`).*

---

## 🌍 The Problem

Autonomous AI coding agents rely on continuous HTTP/2 connections and Server-Sent Event (SSE) streams. In volatile network environments—such as toggling VPNs, switching between Wi-Fi and mobile hotspots, putting laptops to sleep, or operating in heavily geoblocked regions (e.g. Iran)—any network transition abruptly breaks active TCP sockets.

| Failure Mode | Impact on Agent Session |
| :--- | :--- |
| **`ECONNRESET` / Broken pipe** | Live model streams drop immediately without saving intermediate progress. |
| **`403 Forbidden` Geoblock** | Brief IP leaks during VPN handshakes cause API gateways to blacklist the active session. |
| **Orphaned Subagents** | Background tasks get stuck in infinite retry loops, wasting memory and CPU cycles. |
| **Dangling `.git/index.lock`** | Sudden session termination leaves unremovable Git lock files, blocking future commits. |

---

## 💡 Core Workflows

`antigravity-pause` equips Antigravity with four coordinated resilience commands:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               1. Hot Standby (Zero-Kill)                               │
│                                                                                        │
│   /pause       ──► Radio silence + light standby for subagents (RAM state preserved)   │
│   /play        ──► <200ms anti-leak pre-flight probe + instant execution resumption    │
└────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────────┐
│                            2. Deep Hibernation (Disk Snapshot)                         │
│                                                                                        │
│   /hibernate   ──► Atomic checkpoint saved + git locks freed + clean process shutdown  │
│   /continue    ──► Network verified + state rehydrated from the next sequential step   │
└────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        3. Hardware-Level Kill Switch (Firewall Shield)                 │
│                                                                                        │
│   /killswitch  ──► Windows Firewall Outbound Block on physical adapters (Wi-Fi, LAN)  │
│                    If VPN TUN drops, Windows drops packets locally. 0 bytes leak.      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Feature Matrix

| Feature | Description | Command |
| :--- | :--- | :---: |
| **Pre-Flight Leak Probe** | Validates connectivity and verifies non-sanctioned geo-location in `<200ms` before any LLM API request. | `/play` |
| **Zero-Kill Standby** | Suspends active subagents into an idle state without killing process trees. Zeroes network traffic while switching VPNs. | `/pause` |
| **Atomic Checkpoint** | Saves multi-agent progress, conversation metadata, and execution steps into a crash-resilient JSON snapshot. | `/hibernate` |
| **Firewall Kill Switch** | Blocks outbound traffic on physical adapters (`Wi-Fi`, `Ethernet`) to prevent Iran IP leaks when VPN drops. | `/killswitch` |
| **Git Lock Sanitizer** | Automatically sweeps and removes dangling `.git/index.lock` files left behind by killed processes. | Automatic / CLI |

---

## 🛡️ Hardware Kill Switch (Optional & Manual)

The Kill Switch is **strictly manual & optional** (disabled by default). International users outside restricted zones do not need it, while developers in Iran or geo-fenced environments can toggle it on with a single command.

### How to Toggle:

```text
/killswitch status   ──► Check whether the firewall shield is active
/killswitch on       ──► Enable Outbound Block rules on Wi-Fi and Ethernet
/killswitch off      ──► Cleanly remove firewall rules and restore default routing
```

Or using desktop 1-click batch files:
* Double-click **`enable_killswitch.bat`** (requests Administrator permission and enables rules).
* Double-click **`disable_killswitch.bat`** (removes rules).

---

## 🖥️ Terminal Showcase

Running the built-in diagnostic CLI:

```text
> python cli.py probe
[OK] اتصال ایمن است (Latency: 142.1ms | IP: 185.112.82.148 | Country: FI)
-> اتصال پایدار است و شرایط برای ارسال درخواست به هوش مصنوعی ۱۰۰٪ امن می‌باشد.

> python cli.py killswitch status --json
{
  "kill_switch_enabled": true,
  "active_rules_count": 4,
  "physical_adapters": ["Ethernet", "Wi-Fi"],
  "protected_binaries": [
    "C:\\Users\\...\\Antigravity.exe",
    "C:\\Users\\...\\language_server.exe"
  ],
  "message": "کیل‌سوئیچ فایروال فعال است: ترافیک اینترنت در صورت قطع VPN از کارت شبکه فیزیکی نشت نخواهد کرد."
}
```

---

## 📂 Repository Structure

```
antigravity-pause/
├── assets/
│   └── banner.png            # Official repository banner
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
├── install.py                # Automated installer & dynamic skill linker
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

> **متن آماده برای کپی به چت:**  
> `لطفاً ریپازیتوری https://github.com/omid-io/antigravity-pause.git را کلون کن و با اجرای دستور python install.py قابلیت‌های /pause، /play، /hibernate و /killswitch را روی سیستم من نصب و فعال کن.`

---

### 🌍 مسأله چیست؟
دستیارهای کدنویسی هوش مصنوعی به سوکت‌های زنده HTTP/2 و استریم‌های متوالی متکی هستند. در شرایط ناپایدار شبکه ایران (قطع و وصل، تعویض سرور، اسلیپ کردن سیستم یا قطع ناگهانی تونل VPN)، سوکت بلافاصله قطع می‌شود و خطاهای زیر رخ می‌دهد:

1. **خطای قرمز `ECONNRESET`:** قطع شدن ناگهانی استریم و سوختن پاسخ در حال تولید.
2. **خطای تحریم `403 Forbidden`:** سوئیچ خودکار ویندوز به کارت شبکه فیزیکی (مودم یا وای‌فای) هنگام قطع VPN و نشت آی‌پی ایران به سرورهای گوگل.
3. **ساب‌ایجنت‌های معلق (Orphan Processes):** به دام افتادن پروسه‌ها در حلقه‌های تکرار بی‌پایان.
4. **فایل‌های قفل خراب گیت:** باقی ماندن `.git/index.lock` به دلیل خروج ناگهانی حین عملیات نوشتن.

---

### 💡 راه‌حل‌های ۴گانه `antigravity-pause`

| قابلیت | عملکرد | دستور |
| :--- | :--- | :---: |
| **ایست گرم (Hot Standby)** | سکوت رادیویی و خواب سبک والد و ساب‌ایجنت‌ها بدون بستن پروسه‌ها یا خالی شدن رم. | `/pause` |
| **ادامه امن (Safe Resume)** | پروب ۲۰۰ میلی‌ثانیه‌ای سلامت اتصال و ضد نشت آی‌پی + ادامه فوری کار. | `/play` |
| **خواب عمیق (Hibernation)** | ثبت اتمیک وضعیت روی دیسک، پاکسازی قفل‌های گیت و بستن تمیز برنامه‌ها. | `/hibernate` |
| **بازیابی خودکار (Restore)** | لود آخرین چک‌پوینت و ادامه پروژه دقیقاً از گام بعدی در سشن جدید. | `/continue` |
| **کیل‌سوئیچ فایروال (Kill Switch)** | مسدودسازی ترافیک Antigravity روی وای‌فای و لن فیزیکی جهت عدم نشت به ایران در قطع VPN. | `/killswitch` |

---

### 🛡️ نحوه فعال‌سازی دستی کیل‌سوئیچ (کاملاً اختیاری)

این ویژگی به صورت پیش‌فرض خاموش است تا برای کاربران خارجی محدودیتی ایجاد نکند. برای فعال‌سازی در ایران:

* **در چت Antigravity:**
  * `/killswitch on` — فعال‌سازی سپر
  * `/killswitch off` — غیرفعال‌سازی و بازگشت به حالت عادی
  * `/killswitch status` — مشاهده وضعیت فعلی
* **فایل‌های یک‌کلیکی دسکتاپ:**
  * اجرای فایل `enable_killswitch.bat`
  * اجرای فایل `disable_killswitch.bat`
* **خط‌فرمان (مخصوص اتوماسیون):**
  ```powershell
  python cli.py killswitch status --json
  python cli.py killswitch enable
  python cli.py killswitch disable
  ```

---

### 📜 مجوز و لایسنس
این پروژه تحت پروانه [MIT License](LICENSE) منتشر شده و استفاده از آن برای تمام برنامه‌نویسان آزاد و رایگان است.
