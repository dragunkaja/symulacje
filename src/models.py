from dataclasses import dataclass, field
from enum import IntEnum, Enum
from typing import Any

class Permission(IntEnum):
    NONE = 0
    READ = 1
    USE = 2
    ADMIN = 3

class Zone(str, Enum):
    SANDBOX = "SANDBOX"
    HOST = "HOST"

@dataclass
class Resource:
    id: str
    name: str
    zone: Zone
    required_access: Permission
    granted_access: Permission
    is_goal: bool = False
    # `access_level` is the permission currently held on this resource.
    access_level: Permission = Permission.NONE
    # `known` means its hidden parameters have been diagnosed.
    # The agent still knows the node ID and graph topology from the start.
    known: bool = False
    # Hidden environment parameters; they are exposed only by DIAGNOSE.
    p_success: float = 0.0
    p_detection: float = 0.0

@dataclass(order=True)
class Event:
    time: float
    sequence: int
    kind: str = field(compare=False)
    payload: dict[str, Any] = field(default_factory=dict, compare=False)


@dataclass(frozen=True)
class Action:
    kind: str  # DIAGNOSE, ATTEMPT, STOP
    target: str | None = None

