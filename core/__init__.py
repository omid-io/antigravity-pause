"""
antigravity-pause: Core resilience and checkpointing engine for Antigravity agents.
"""

from .network_probe import NetworkProbe, ProbeResult
from .engine import CheckpointEngine
from .kill_switch import AntigravityKillSwitch

__version__ = "0.2.0"
__all__ = ["NetworkProbe", "ProbeResult", "CheckpointEngine", "AntigravityKillSwitch"]
