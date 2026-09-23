# ⏸️ antigravity-pause

> **Graceful Pause, Deep Hibernation & Pre-Flight Leak Protection for Google Antigravity (2.0 Desktop, IDE, and CLI).**  
> *سیستم مدیریت پاز، فریز وضعیت (چک‌پوینت)، تست سلامت اتصال و مهار نشت آی‌پی برای Antigravity.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)]()
[![Platform: Windows%20%7C%20Linux%20%7C%20macOS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Antigravity: 2.0+ Compatible](https://img.shields.io/badge/Antigravity-2.0+-orange.svg)]()

---

## 🌍 The Problem / مسأله چیست؟

### English
AI coding assistants rely on continuous HTTP/2 and Server-Sent Event (SSE) streams. In unstable network environments—such as using corporate VPNs (Zscaler, Cisco), switching between Wi-Fi and mobile hotspots, putting laptops to sleep, or navigating internet censorship and geoblocking (e.g. in Iran)—any network switch immediately terminates the TCP socket. The agent crashes with `ECONNRESET`, throws `403 Forbidden` / `FAILED_PRECONDITION` geoblock errors, leaves orphaned background processes, and corrupts `.git/index.lock` files.

### فارسی
دستیارهای کدنویسی هوش مصنوعی به جریان‌های زنده HTTP/2 و SSE وابسته هستند. در شرایط بی‌ثباتی اینترنت (مانند نیاز به تعویض فیلترشکن، سوییچ بین وای‌فای و هات‌اسپات، اسلیپ کردن سیستم یا دوره‌های قطعی برق)، هر تغییر شبکه بلافاصله سوکت فعال را نابود می‌کند. این مسأله باعث خطای قرمز `ECONNRESET`، خطای تحریم `403 Forbidden` (به دلیل نشت ثانیه‌ای آی‌پی ایران)، معلق ماندن ساب‌ایجنت‌ها و ایجاد قفل‌های خراب در گیت (`.git/index.lock`) می‌شود.

---

## 💡 The Solution / راه‌حل

**`antigravity-pause`** دو جفت اسلش‌کامند هوشمند به Antigravity اضافه می‌کند:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          1. Hot Standby (ایست گرم)                          │
│                                                                             │
│   /pause  ──► سکوت رادیویی + خواب سبک ساب‌ایجنت‌ها (بدون بستن پروسه‌ها)     │
│   /play   ──► پروب ۲۰۰ میلی‌ثانیه‌ای ضد نشت IP + ادامه فوری کار             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     2. Deep Hibernation (خواب عمیق دیسک)                    │
│                                                                             │
│   /hibernate ──► ثبت اتمیک چک‌پوینت + پاکسازی قفل‌ها + بستن تمیز برنامه‌ها │
│   /continue  ──► پروب شبکه + بازسازی ساب‌ایجنت‌ها + ادامه تسک از گام بعدی   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Features / ویژگی‌های کلیدی

1. **Sub-second Pre-Flight Leak Probe:**
   * اسکریپت سبک پایتون با زمان پاسخ زیر ۲۰۰ میلی‌ثانیه قبل از ارسال هرگونه ریکوئست، اتصال و کشور آی‌پی را می‌سنجد. اگر آی‌پی ایران نشت کند یا فیلترشکن قطع باشد، درخواست متوقف شده و با هشدار فارسی از ارور ۴۰۳ و مسدود شدن سشن جلوگیری می‌کند.
2. **Zero-Kill Hot Standby (`/pause`):**
   * ساب‌ایجنت‌ها و والد بدون کشته شدن پروسه در وضعیت `waiting_for_message` قرار می‌گیرند؛ رم حفظ شده و ترافیک شبکه به صفر می‌رسد تا بتوانید وی‌پی‌ان را عوض کنید.
3. **Atomic State Checkpointing (`/hibernate`):**
   * ذخیره ضد خرابی در فایل دیسک حتی اگر برق ناگهان قطع شود.
4. **Git Lock Sanitizer:**
   * پاکسازی خودکار فایل‌های مزاحم `.git/index.lock` که پس از قطع ناگهانی ارتباط در سیستم می‌مانند.
5. **Universal Compatibility:**
   * سازگار با **Antigravity 2.0 Desktop**، **Antigravity IDE** و **`agy` CLI**.

---

## 🚀 Quick Installation / نصب سریع

### روش ۱: نصب با یک کلیک در ویندوز (توصیه‌شده)
فقط کافی است فایل `setup.bat` را اجرا کنید یا دستور زیر را در ترمینال بزنید:

```powershell
python install.py
```

این اسکریپت اسکیل‌ها را مستقیماً از طریق Junction در پوشه کانفیگ سراسری Antigravity (`~/.gemini/config/skills/`) ثبت می‌کند و بلافاصله در کادر چت فعال می‌شوند.

---

## 📖 How to Use / نحوه استفاده

### سناریو ۱: تعویض فیلترشکن یا اسلیپ کوتاه
1. در چت تایپ کنید:
   ```text
   /pause
   ```
   *ایجنت فوراً به حالت سکوت می‌رود و اعلام می‌کند آماده تغییر اینترنت است.*
2. فیلترشکن را عوض کنید، سرور را تغییر دهید یا سیستم را موقتاً اسلیپ کنید.
3. پس از برقراری اینترنت در چت تایپ کنید:
   ```text
   /play
   ```
   *(یا بنویسید: «ادامه بده»).*
   *پروب شبکه در کسری از ثانیه اتصال را می‌سنجد و در صورت سلامت، بدون هیچ دوباره‌کاری ادامه می‌دهد.*

### سناریو ۲: خاموش کردن سیستم یا بستن کامل Antigravity
1. در چت تایپ کنید:
   ```text
   /hibernate
   ```
   *اسنپ‌شات کامل وضعیت ذخیره شده و تمام پروسه‌ها به صورت تمیز بسته می‌شوند.*
2. سیستم را خاموش یا برنامه را ببندید.
3. پس از روشن کردن مجدد، بنویسید:
   ```text
   /continue
   ```
   *چک‌پوینت لود شده، ساب‌ایجنت‌ها بازسازی می‌شوند و تسک ادامه می‌یابد.*

---

## 🛠️ CLI Usage / استفاده از خط فرمان

می‌توانید قابلیت‌های هسته را به صورت مجزا نیز اجرا و تست کنید:

```powershell
# تست سلامت شبکه و نشت آی‌پی
python cli.py probe

# پاکسازی قفل‌های معلق گیت
python cli.py clean-locks

# مشاهده چک‌پوینت فعال
python cli.py checkpoint-load
```

---

## 📂 Repository Structure

```
antigravity-pause/
├── core/
│   ├── network_probe.py    # پروب شبکه سریع و ضد نشت آی‌پی ایران
│   ├── engine.py           # موتور اتمیک ذخیره و بازخوانی چک‌پوینت
│   └── process_guard.py    # ماژول فریز ساب‌ایجنت‌ها و رفع قفل‌های معلق
├── skills/
│   ├── pause/SKILL.md      # اسکیل /pause و /play
│   └── hibernate/SKILL.md  # اسکیل /hibernate و /continue
├── cli.py                  # ابزار خط فرمان تست و مدیریت
├── install.py              # نصب‌کننده خودکار
├── setup.bat               # اسکریپت نصب ویندوز
├── LICENSE                 # MIT License
└── README.md
```

---

## 📜 License
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است و برای تمام توسعه‌دهندگان آزاد و رایگان می‌باشد.
