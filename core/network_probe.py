"""
antigravity-pause: Network Probe & IP Leak Detector
Designed for resilient agentic workflows under unstable networks and geo-restrictions.
"""

import socket
import ssl
import json
import time
import sys
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ProbeResult:
    STATUS_OK = "OK"
    STATUS_NO_INTERNET = "NO_INTERNET"
    STATUS_IP_LEAK_IRAN = "IP_LEAK_IRAN"
    STATUS_DEGRADED = "DEGRADED"

    def __init__(
        self,
        status: str,
        latency_ms: float,
        ip: Optional[str] = None,
        country: Optional[str] = None,
        message: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status = status
        self.latency_ms = latency_ms
        self.ip = ip
        self.country = country
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "latency_ms": round(self.latency_ms, 2),
            "ip": self.ip,
            "country": self.country,
            "message": self.message,
            "details": self.details,
            "safe_to_connect": self.status == self.STATUS_OK,
        }

    def __repr__(self) -> str:
        return f"<ProbeResult status={self.status} latency={self.latency_ms:.1f}ms country={self.country}>"


class NetworkProbe:
    """
    Sub-second, zero-dependency network validator.
    Verifies that connections to AI API hosts are operational and that Iran IP is not leaking.
    """

    DEFAULT_AI_HOST = "generativelanguage.googleapis.com"
    DEFAULT_AI_PORT = 443

    GEO_IP_PROVIDERS = [
        "https://ipwho.is/",
        "https://api.ipify.org?format=json",
    ]

    @classmethod
    def test_tcp_reachability(cls, host: str = DEFAULT_AI_HOST, port: int = DEFAULT_AI_PORT, timeout: float = 2.0) -> (bool, float):
        """Measures TCP handshake latency to the destination host."""
        start = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                latency = (time.perf_counter() - start) * 1000.0
                return True, latency
        except Exception:
            return False, -1.0

    @classmethod
    def check_gemini_endpoint(cls, timeout: float = 2.5) -> (bool, int, str):
        """
        Sends a quick HTTPS request to the Gemini API host.
        If Google responds with 403 Forbidden (Region blocked), returns (False, 403, reason).
        """
        url = f"https://{cls.DEFAULT_AI_HOST}/"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Antigravity-NetworkProbe/1.0"},
            method="GET",
        )
        ctx = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                return True, response.status, "Connected"
        except urllib.error.HTTPError as e:
            # 404 is normal for root endpoint; 403 indicates geoblock or authorization error
            if e.code == 404:
                return True, 404, "Reachable"
            if e.code == 403:
                return False, 403, "Geoblocked / Region Restricted"
            return True, e.code, str(e.reason)
        except Exception as e:
            return False, -1, str(e)

    @classmethod
    def detect_public_ip(cls, timeout: float = 2.0) -> (Optional[str], Optional[str]):
        """Detects current public IP and Country Code without heavy dependencies."""
        try:
            req = urllib.request.Request(
                "https://ipwho.is/",
                headers={"User-Agent": "Antigravity-Probe/1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as res:
                data = json.loads(res.read().decode("utf-8"))
                ip = data.get("ip")
                country = data.get("country_code", "").upper()
                return ip, country
        except Exception:
            pass

        # Fallback to ipify for IP only
        try:
            req = urllib.request.Request(
                "https://api.ipify.org?format=json",
                headers={"User-Agent": "Antigravity-Probe/1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as res:
                data = json.loads(res.read().decode("utf-8"))
                return data.get("ip"), None
        except Exception:
            return None, None

    @classmethod
    def run_full_probe(cls, timeout: float = 3.0) -> ProbeResult:
        """
        Runs comprehensive out-of-band validation:
        1. Fast TCP connection test.
        2. Gemini API endpoint reachability check.
        3. Public IP and Iran leak detection.
        """
        start_time = time.perf_counter()

        # Step 1: TCP Handshake
        tcp_ok, tcp_latency = cls.test_tcp_reachability(timeout=timeout)
        if not tcp_ok:
            return ProbeResult(
                status=ProbeResult.STATUS_NO_INTERNET,
                latency_ms=(time.perf_counter() - start_time) * 1000.0,
                message="اتصال اینترنت قطع است یا مسیر اتصال به سرورهای هوش مصنوعی مسدود می‌باشد.",
                details={"tcp_ok": False},
            )

        # Step 2: Gemini Endpoint HTTP Check
        api_ok, http_code, http_reason = cls.check_gemini_endpoint(timeout=timeout)
        if not api_ok and http_code == 403:
            return ProbeResult(
                status=ProbeResult.STATUS_IP_LEAK_IRAN,
                latency_ms=tcp_latency,
                message="هشدار نشت IP: ترافیک اینترنت از منطقه تحریم‌شده (احتمالاً ایران) ارسال می‌شود (کد ۴۰۳ گوگل).",
                details={"http_code": http_code, "reason": http_reason},
            )

        # Step 3: Fast GeoIP Check
        ip, country = cls.detect_public_ip(timeout=1.5)
        if country in ["IR", "IRAN"]:
            return ProbeResult(
                status=ProbeResult.STATUS_IP_LEAK_IRAN,
                latency_ms=tcp_latency,
                ip=ip,
                country=country,
                message=f"هشدار نشت آی‌پی ایران شناسایی شد (IP: {ip}, Country: {country}). درخواست لغو شد تا خطای تحریم دریافت نشود.",
                details={"ip": ip, "country": country},
            )

        total_latency = (time.perf_counter() - start_time) * 1000.0
        return ProbeResult(
            status=ProbeResult.STATUS_OK,
            latency_ms=total_latency,
            ip=ip,
            country=country or "Non-IR",
            message="اتصال پایدار است و شرایط برای ارسال درخواست به هوش مصنوعی ۱۰۰٪ امن می‌باشد.",
            details={"tcp_latency_ms": tcp_latency, "http_status": http_code},
        )


if __name__ == "__main__":
    result = NetworkProbe.run_full_probe()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
