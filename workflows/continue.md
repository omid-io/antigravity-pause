---
name: continue
description: بررسی سلامت شبکه، خواندن چک‌پوینت ذخیره‌شده و ادامه هوشمندانه تسک از همان نقطه
---

# دستور بازیابی چک‌پوینت (/continue)

هنگامی که این دستور فراخوانی می‌شود:
1. ابتدا پروب سلامت شبکه را بسنج:
   `python E:\programming\Tools\antigravity-pause\cli.py probe --json`
2. چک‌پوینت ذخیره‌شده در دیسک را بخوان:
   `python E:\programming\Tools\antigravity-pause\cli.py checkpoint-load`
3. قفل‌های احتمالی گیت را پاکسازی کن:
   `python E:\programming\Tools\antigravity-pause\cli.py clean-locks`
4. اگر ساب‌ایجنتی در چک‌پوینت بوده، با پرامپت ریکاوری مجدداً آن را راه‌اندازی کن.
5. تسک والد را از گام بعدی ثبت‌شده ادامه بده بدون هیچ توضیح اضافه یا تکرار کارهای گذشته.
