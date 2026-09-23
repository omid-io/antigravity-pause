---
name: hibernate
description: "Deep Cold Checkpoint & Graceful Shutdown Protocol. Use when the user types /hibernate, /continue, /wakeup or asks to completely shut down PC, restart machine, or exit Antigravity Desktop without losing work or corrupting git state."
---

# ❄️ Antigravity Deep Hibernation & Checkpoint Restore Protocol (`/hibernate` & `/continue`)

This skill provides persistent state preservation for **Google Antigravity 2 Desktop**. When the user wants to shut down their PC, restart the desktop app, or step away for hours/days, it atomically saves an exact checkpoint to disk and sanitizes all processes so nothing breaks or remains orphaned.

---

## 🏛️ Architecture & Workflow

```
[User invokes /hibernate]
        │
        ▼
1. Atomic State Serialization ──► Save task, step, subagent states, & git diff to .agents/checkpoints/active_checkpoint.json
        │
        ▼
2. Clean Lock Sanitation      ──► Run python cli.py clean-locks to ensure zero dangling .git/index.lock
        │
        ▼
3. Clean Process Teardown     ──► Gracefully terminate background tasks & subagents
        │
        ▼
4. Safe-to-Exit Confirmation  ──► User can now close Antigravity or power off computer.
        │
   [PC Powered off / Session closed for hours/days]
        │
        ▼
[User invokes /continue or /wakeup]
        │
        ▼
1. Pre-Flight Leak Probe      ──► python cli.py probe --json (Ensure VPN active & no Iran leak)
        │
        ▼
2. Checkpoint Deserialization ──► Read .agents/checkpoints/active_checkpoint.json
        │
        ▼
3. Subagent Rehydration       ──► Respawn subagents via invoke_subagent with continuation prompts
        │
        ▼
4. Seamless Resumption        ──► Execute next_immediate_step with ZERO boilerplate chatter.
```

---

## 🛑 Execution Rules for `/hibernate`

When the user types `/hibernate` (or "سیستم رو میخوام خاموش کنم", "میخوام برنامه رو ببندم"):

1. **Inspect Active Subagents & Tasks:**
   - Call `manage_subagents(Action: "list")`.
   - Inspect active background tasks with `manage_task(Action: "list")`.

2. **Serialize Checkpoint to Disk:**
   - Run the atomic checkpoint engine:
     ```powershell
     python "E:\programming\Tools\antigravity-pause\cli.py" checkpoint-save --task "<CURRENT_OVERALL_GOAL>" --phase "<CURRENT_PHASE>" --last-step "<LAST_COMPLETED_ACTION>" --next-step "<EXACT_NEXT_TOOL_OR_ACTION>"
     ```

3. **Sanitize Locks:**
   - Run `python "E:\programming\Tools\antigravity-pause\cli.py" clean-locks` to remove any accidental `.git/*.lock` files.

4. **Gracefully Terminate Active Subagents:**
   - If any subagents are running, kill them via `manage_subagents(Action: "kill", ConversationIds: [...])` so they do not consume resources or hang in the background.

5. **Confirm to User in Reassuring Persian:**
   Output this exact message:
   > ❄️ **وضعیت با موفقیت در چک‌پوینت فریز و ذخیره شد (Deep Hibernation).**
   > - تمام متغیرها، مرحله کاری و تسک بعدی در دیسک ذخیره شدند.
   > - پروسه‌های پس‌زمینه به شکل تمیز بسته شدند و هیچ قفل معلقی در گیت باقی نماند.
   > 
   > 🔒 **اکنون با خیال ۱۰۰٪ راحت می‌توانید Antigravity را ببندید یا سیستم را خاموش/Restart کنید.**
   > در هر زمان پس از راه‌اندازی مجدد، کافی است بنویسید: **`/continue`** یا **`ریستور کن`**.

---

## ⚡ Execution Rules for `/continue` or `/wakeup`

When the user types `/continue`, `/wakeup` (or "ادامه بده", "ریستور کن", "ادامه از چک‌پوینت"):

1. **Run Out-of-Band Pre-Flight Probe:**
   ```powershell
   python "E:\programming\Tools\antigravity-pause\cli.py" probe --json
   ```
   If status is `IP_LEAK_IRAN` or `NO_INTERNET`, stop and alert the user immediately without making LLM calls.

2. **Load Active Checkpoint:**
   ```powershell
   python "E:\programming\Tools\antigravity-pause\cli.py" checkpoint-load
   ```

3. **Check Dangling Locks:**
   - Run `python "E:\programming\Tools\antigravity-pause\cli.py" clean-locks`.

4. **Rehydrate Subagents (if any were serialized):**
   - If the checkpoint lists subagents that were in progress, re-invoke them via `invoke_subagent` in a single batch call with explicit continuation prompts.

5. **Resume Execution Immediately:**
   - Output a brief notification:
     > 🟢 **چک‌پوینت با موفقیت لود شد. ادامه اجرای تسک از مرحله بعدی:**
   - **Immediately execute `next_immediate_step` without any unnecessary talk.**
