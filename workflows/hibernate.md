---
name: hibernate
description: خواب عمیق دیسک، ثبت اتمیک چک‌پوینت، پاکسازی قفل‌های گیت و بستن تمیز برنامه‌ها
---

# دستور خواب عمیق (/hibernate)

هنگامی که این دستور فراخوانی می‌شود:
1. وضعیت تسک فعلی، فاز کاری و گام بعدی را با دستور زیر اتمیک در دیسک ثبت کن:
   `python E:\programming\Tools\antigravity-pause\cli.py checkpoint-save --task "..." --phase "..." --last-step "..." --next-step "..."`
2. قفل‌های احتمالی گیت را پاکسازی کن:
   `python E:\programming\Tools\antigravity-pause\cli.py clean-locks`
3. ساب‌ایجنت‌ها و تسک‌های پس‌زمینه را به صورت تمیز ببند (Kill کن تا پروسه معلق نماند).
4. به کاربر اعلام کن که همه چیز در دیسک فریز شده و می‌تواند کامپیوتر را خاموش یا Antigravity را ببندد و بعداً با `/continue` کار را بازیابی کند.
