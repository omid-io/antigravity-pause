---
name: killswitch
description: "Windows Firewall Outbound Kill Switch for Antigravity. Use when the user types /killswitch, asks to check firewall status, or wants to enable/disable outbound IP leak protection on physical adapters."
---

# 🛡️ Antigravity Windows Firewall Kill Switch (`/killswitch`)

This skill controls the hardware-level Windows Defender Firewall outbound rules designed to prevent **IP leaks and 403 Forbidden geoblock penalties** when VPN TUN connections drop unexpectedly.

---

## 🏛️ How It Works

* **Target Processes:** `Antigravity.exe` and `language_server.exe`.
* **Outbound Policy:** Restricts outgoing traffic so that Antigravity **ONLY** communicates via virtual VPN adapters (TUN, TAP, wintun, WireGuard). Outbound packets to physical adapters (`Wi-Fi`, `Ethernet`) are blocked locally by Windows kernel.
* **Failure Mode:** If VPN disconnects, packets are dropped locally. Zero bytes are leaked to the physical ISP, preventing Google from seeing Iran IPs.

---

## ⚡ Agent Control & Commands

When the user asks about the Kill Switch, or types `/killswitch`:

### 1. Check Status (`/killswitch status` or `/killswitch`)
Execute the machine-readable CLI check:
```powershell
python "E:\programming\Tools\antigravity-pause\cli.py" killswitch status --json
```

**Evaluating the JSON Output:**
- `kill_switch_enabled == true`: Kill switch is active and protecting Antigravity.
- `kill_switch_enabled == false`: Kill switch is inactive. Traffic flows normally over all interfaces.

### 2. Enable Kill Switch (`/killswitch on` or `/killswitch enable`)
Execute:
```powershell
python "E:\programming\Tools\antigravity-pause\cli.py" killswitch enable
```
*(Note: If executed in non-admin prompt, an automated Windows UAC prompt will appear for user confirmation).*

Confirm to user in Persian:
> 🛡️ **کیل‌سوئیچ فایروال با موفقیت فعال شد.**
> ترافیک Antigravity روی کارت‌های فیزیکی (Wi-Fi / Ethernet) مسدود شد. در صورت قطعی ناگهانی فیلترشکن، هیچ ترافیکی از اینترنت ایران عبور نخواهد کرد.

### 3. Disable Kill Switch (`/killswitch off` or `/killswitch disable`)
Execute:
```powershell
python "E:\programming\Tools\antigravity-pause\cli.py" killswitch disable
```

Confirm to user in Persian:
> ⚪ **کیل‌سوئیچ فایروال غیرفعال شد.**
> تمامی رول‌های فایروال حذف شدند و ترافیک به حالت استاندارد بازگشت.
