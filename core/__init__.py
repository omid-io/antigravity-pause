"""
antigravity-pause: Core resilience and checkpointing engine for Antigravity agents.
"""

from .network_probe import NetworkProbe, ProbeResult
from .engine import CheckpointEngine
from .kill_switch import AntigravityKillSwitch
from .sentinel import NetworkSentinel

__version__ = "0.3.0"
__all__ = ["NetworkProbe", "ProbeResult", "CheckpointEngine", "AntigravityKillSwitch", "NetworkSentinel"]
