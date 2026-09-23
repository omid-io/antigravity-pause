---
name: pause
description: "Graceful Agent Standby & Fast Resume Protocol. Use when the user types /pause, /play, /resume or asks to temporarily pause execution to switch VPNs, change networks, or sleep PC without killing active subagents or losing RAM state."
---

# ⏸️ Antigravity Hot Standby & Safe Resume Protocol (`/pause` & `/play`)

This skill provides seamless, zero-crash pausing and resuming for **Google Antigravity 2 Desktop** (as well as IDE and CLI). It enables the user to switch VPNs, disconnect/reconnect internet, or put the machine to sleep without causing HTTP/2 stream errors, `ECONNRESET`, or geoblock `403` penalties.

---

## 🏛️ Architecture & Philosophy

```
[User invokes /pause]
        │
        ▼
1. Graceful Tool Wrap-up  ──► Ensure pending file writes are syntactically closed/valid
        │
        ▼
2. Subagent Standby       ──► Broadcast standby notice via send_message (Zero Tool Dispatch)
        │
        ▼
3. Radio Silence          ──► Stop issuing external network requests. Yield turn immediately.
        │
    [User switches VPN / Disconnects / Sleeps PC]
        │
        ▼
[User invokes /play or /resume]
        │
        ▼
4. Pre-Flight Out-of-Band Probe ──► Run python E:\programming\Tools\antigravity-pause\cli.py probe
        │
   ┌────┴──────────────────────────┐
   ▼                               ▼
[Probe: IP_LEAK_IRAN / ERROR]   [Probe: OK]
Do NOT call LLM API tools.       Notify subagents to resume.
Warn user in Persian with IP.     Continue parent task from next step.
```

---

## 🛑 Execution Rules for `/pause`

When the user types `/pause` (or "پاز کن", "صبر کن میخوام نت رو عوض کنم", "وایسا"):

1. **Check Active Subagents:**
   - Call `manage_subagents(Action: "list")`.
   - If subagents are running, send each of them a standby notice:
     ```
     send_message(
       Recipient: "<conversationId>",
       Message: "[STANDBY] Network switch in progress. Yield your turn without calling new tools. Wait for resume."
     )
     ```
   - **DO NOT kill the subagents!** Let them transition into `idle` / `waiting_for_message`.

2. **Save Quick In-Memory State:**
   - Briefly record in your mind/scratch:
     - The current sub-task you were performing.
     - The immediate next action to execute upon waking up.

3. **Cease Network Tool Calls (Radio Silence):**
   - Do NOT run web searches, URLs, git fetch, or network commands.
   - Do NOT start long-running background tasks.

4. **Confirm to User in Clean Persian:**
   Output this exact reassuring message to the user:
   > ⏸️ **سیستم در حالت ایست گرم (Hot Standby) قرار گرفت.**
   > - تمام ساب‌ایجنت‌ها و ابزارها به حالت سکوت رفتند (هیچ درخواستی به اینترنت ارسال نمی‌شود).
   > - وضعیت جاری در حافظه حفظ شده است.
   > 
   > 🟢 **اکنون با خیال راحت می‌توانید وی‌پی‌ان را عوض کنید، شبکه را تغییر دهید یا سیستم را Sleep کنید.**
   > پس از برقراری اتصال، کافی است بنویسید: **`/play`** یا **`ادامه بده`**.

5. **Yield the Turn Immediately:**
   - Stop calling any tools and end the turn.

---

## ▶️ Execution Rules for `/play` or `/resume`

When the user types `/play`, `/resume` (or "ادامه بده", "وصل شدم", "پلی"):

1. **Run Pre-Flight Out-of-Band Leak Probe:**
   Execute the zero-risk CLI probe:
   ```powershell
   python "E:\programming\Tools\antigravity-pause\cli.py" probe --json
   ```

2. **Evaluate Probe Result:**
   - **Case A: `status == "IP_LEAK_IRAN"` (نشت آی‌پی ایران):**
     - 🛑 **STOP IMMEDIATELY.** Do NOT dispatch any Gemini API requests or tools!
     - Alert the user in Persian:
       > ⚠️ **هشدار نشت IP ایران!**
       > پروب شبکه متوجه شد که اینترنت مستقیم یا آی‌پی ایران شناسایی شده است (کد ۴۰۳ یا نشت لوکیشن). برای جلوگیری از مسدودسازی سشن، هیچ درخواستی به هوش مصنوعی ارسال نشد.
       > لطفاً فیلترشکن خود را بررسی و فعال کنید، سپس مجدداً **`/play`** بزنید.
     - End turn and wait for user.

   - **Case B: `status == "NO_INTERNET"` (اینترنت قطع است):**
     - Inform the user that the internet connection is not reachable yet, and invite them to retry once connected.

   - **Case C: `status == "OK"` (اتصال امن و تأییدشده):**
     - Notify active subagents via `send_message`:
       ```
       send_message(
         Recipient: "<conversationId>",
         Message: "[RESUME] Connection verified and safe. Resume your work."
       )
       ```
     - Output a brief 1-line update:
       > 🟢 **اتصال پایدار و امن تأیید شد. کار از نقطه توقف ادامه می‌یابد.**
     - **Immediately execute the next step** without re-explaining or repeating already finished tasks!
