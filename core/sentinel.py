"""
antigravity-pause: Background Network Sentinel & Auto-Resume Engine
Runs silently in the background on the local machine during /pause.
Monitors network transition and triggers automatic agent wakeup once VPN reconnects safely.
"""

import sys
import time
import json
from typing import Dict, Any, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .network_probe import NetworkProbe, ProbeResult


class NetworkSentinel:
    """
    Local PC background observer.
    Does NOT send traffic to Google Gemini API until connection is 100% verified.
    """

    @classmethod
    def wait_for_safe_connection(
        cls,
        timeout_seconds: int = 900,
        poll_interval: float = 1.5,
        stabilization_checks: int = 2,
    ) -> Dict[str, Any]:
        """
        Polls locally until the network safely transitions to an operational, non-sanctioned state.

        Algorithm:
        1. Capture baseline probe state (IP, country, status).
        2. If baseline was already OK, wait until network drops OR IP changes (the transition).
        3. Once in transition or if baseline was already disconnected:
           Wait until probe returns STATUS_OK for `stabilization_checks` consecutive times.
        4. Return success dict and exit 0.
        """
        start_time = time.time()
        baseline = NetworkProbe.run_full_probe(timeout=2.0)
        initial_ip = baseline.ip
        initial_status = baseline.status

        # If we started from a healthy connection, we need to see a transition first
        # (either network goes down, or IP changes to another VPN server)
        has_transitioned = (initial_status != ProbeResult.STATUS_OK)

        consecutive_ok = 0
        latest_result: Optional[ProbeResult] = None

        while (time.time() - start_time) < timeout_seconds:
            # Quick probe
            current = NetworkProbe.run_full_probe(timeout=2.0)
            latest_result = current

            # Step 1: Detect transition if we started healthy
            if not has_transitioned:
                if current.status != ProbeResult.STATUS_OK:
                    has_transitioned = True
                    consecutive_ok = 0
                elif current.ip and initial_ip and current.ip != initial_ip:
                    # Switched to another VPN IP directly without complete drop
                    has_transitioned = True
                    consecutive_ok = 1
                else:
                    # Still on original unchanged connection; give user time to toggle VPN
                    # If 20 seconds pass without any toggle, treat as deliberate resume
                    if (time.time() - start_time) > 20.0:
                        has_transitioned = True
                    time.sleep(poll_interval)
                    continue

            # Step 2: Once transitioned, require consecutive stable OKs
            if current.status == ProbeResult.STATUS_OK:
                consecutive_ok += 1
                if consecutive_ok >= stabilization_checks:
                    elapsed = round(time.time() - start_time, 2)
                    return {
                        "success": True,
                        "resumed": True,
                        "elapsed_seconds": elapsed,
                        "ip": current.ip,
                        "country": current.country,
                        "latency_ms": current.latency_ms,
                        "message": f"اتصال امن با موفقیت بازیابی شد (IP: {current.ip} | کشور: {current.country}). سیستم به صورت خودکار بیدار شد.",
                    }
            else:
                consecutive_ok = 0

            time.sleep(poll_interval)

        # Timeout reached
        elapsed = round(time.time() - start_time, 2)
        return {
            "success": False,
            "resumed": False,
            "elapsed_seconds": elapsed,
            "error": "TIMEOUT",
            "message": f"مهلت زمانی ({timeout_seconds} ثانیه) به پایان رسید ولی اتصال پایدار و امن برقرار نشد.",
        }


if __name__ == "__main__":
    timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    res = NetworkSentinel.wait_for_safe_connection(timeout_seconds=timeout)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if res.get("success") else 1)
