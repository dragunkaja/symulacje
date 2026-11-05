"""Abstract sandbox-boundary simulation demo.

This is a safe, synthetic model. It does not execute commands, exploits,
or interact with real containers or operating systems.

Run:
    python sandbox_sim_demo.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, Enum
import heapq
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


class GoalOrientedRiskAwareAgent:
    """Rule-based agent: diagnose candidate nodes, then rank them by utility."""

    def __init__(self, risk_weight: float = 0.8, goal_bonus: float = 3.0):
        self.risk_weight = risk_weight
        self.goal_bonus = goal_bonus

    def choose_action(self, observation: dict[str, Any]) -> Action:
        current = observation["current_node"]
        current_permission = Permission(observation["permissions"][current])
        neighbors = observation["adjacency"].get(current, [])
        resources = observation["resources"]
        diagnostics = observation["diagnostics"]
        budget = observation["budget"]
        diagnostic_cost = observation["diagnostic_cost"]
        attempt_cost = observation["attempt_cost"]

        candidates = [
            node_id for node_id in neighbors
            if Permission(resources[node_id]["required_access"]) <= current_permission
            and not resources[node_id]["is_visited"]
        ]

        if not candidates:
            return Action("STOP")

        # Inspect every currently reachable option before choosing one.
        unknown = [node_id for node_id in candidates if node_id not in diagnostics]
        if unknown:
            if budget < diagnostic_cost:
                return Action("STOP")
            # Prefer the candidate that is structurally closest to the goal.
            target = min(
                unknown,
                key=lambda node_id: (
                    resources[node_id]["distance_to_goal"], node_id
                ),
            )
            return Action("DIAGNOSE", target)

        if budget < attempt_cost:
            return Action("STOP")

        def utility(node_id: str) -> float:
            info = diagnostics[node_id]
            goal_value = self.goal_bonus if info["is_goal"] else 0.0
            progress_value = 1.0 + info["permission_gain"] + goal_value
            distance_penalty = 0.05 * resources[node_id]["distance_to_goal"]
            return (
                info["p_success"] * progress_value
                - self.risk_weight * info["risk"]
                - distance_penalty
            )

        target = max(candidates, key=lambda node_id: (utility(node_id), node_id))
        return Action("ATTEMPT", target)


class SandboxSimulation:
    DIAGNOSTIC_COST = 1
    ATTEMPT_COST = 2
    DIAGNOSTIC_TIME = 1.0
    ATTEMPT_TIME = 2.0
    BLOCK_GIVEN_DETECTION = 0.45

    def __init__(self, seed: int = 17, monitoring: bool = True, budget: int = 12):
        import random

        self.rng = random.Random(seed)
        self.seed = seed
        self.monitoring = monitoring
        self.initial_budget = budget
        self.budget = budget
        self.time = 0.0
        self.terminated = False
        self.termination_reason: str | None = None
        self.current_node = "sandbox_runtime"
        self.logs: list[str] = []
        self.events: list[Event] = []
        self.event_sequence = 0
        self.diagnostics: dict[str, dict[str, Any]] = {}
        self.visited = {self.current_node}
        self.pending_attempt: dict[str, Any] | None = None

        self.resources: dict[str, Resource] = {
            "sandbox_runtime": Resource(
                id="sandbox_runtime", name="Runtime agenta", zone=Zone.SANDBOX,
                required_access=Permission.NONE, granted_access=Permission.READ,
                access_level=Permission.READ,
            ),
            "workspace_cache": Resource(
                id="workspace_cache", name="Magazyn roboczy", zone=Zone.SANDBOX,
                required_access=Permission.READ, granted_access=Permission.USE,
                p_success=0.95, p_detection=0.08,
            ),
            "task_gateway": Resource(
                id="task_gateway", name="Brama zadań", zone=Zone.SANDBOX,
                required_access=Permission.READ, granted_access=Permission.USE,
                p_success=0.82, p_detection=0.12,
            ),
            "bridge_service": Resource(
                id="bridge_service", name="Usługa pośrednia", zone=Zone.SANDBOX,
                required_access=Permission.USE, granted_access=Permission.ADMIN,
                p_success=0.75, p_detection=0.20,
            ),
            "host_resource": Resource(
                id="host_resource", name="Chroniony zasób hosta", zone=Zone.HOST,
                required_access=Permission.ADMIN, granted_access=Permission.ADMIN,
                is_goal=True, p_success=0.70, p_detection=0.25,
            ),
        }

        # Known topology. Hidden risk/success parameters are not in observations.
        self.adjacency = {
            "sandbox_runtime": ["workspace_cache", "task_gateway"],
            "workspace_cache": ["bridge_service"],
            "task_gateway": ["bridge_service"],
            "bridge_service": ["host_resource"],
            "host_resource": [],
        }

        self.log(
            f"START | seed={seed} | monitoring={'ON' if monitoring else 'OFF'} "
            f"| budget={budget}"
        )
        self.log("BOUNDARY | sandbox_runtime/workspace_cache/bridge_service = SANDBOX; host_resource = HOST")
        self.log("AGENT | zna topologię grafu; parametry ryzyka i powodzenia poznaje przez DIAGNOSE")

    def log(self, message: str) -> None:
        self.logs.append(f"[t={self.time:04.1f}] {message}")

    def _schedule(self, delay: float, kind: str, **payload: Any) -> None:
        self.event_sequence += 1
        heapq.heappush(
            self.events,
            Event(self.time + delay, self.event_sequence, kind, payload),
        )

    def _distance_to_goal(self, start: str) -> int:
        queue = [(start, 0)]
        seen = {start}
        while queue:
            node, distance = queue.pop(0)
            if self.resources[node].is_goal:
                return distance
            for nxt in self.adjacency.get(node, []):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, distance + 1))
        return 999

    def observe(self) -> dict[str, Any]:
        current_permission = self.resources[self.current_node].access_level
        resource_view = {}
        for node_id, resource in self.resources.items():
            resource_view[node_id] = {
                "required_access": int(resource.required_access),
                "is_goal": resource.is_goal,
                "is_visited": node_id in self.visited,
                "distance_to_goal": self._distance_to_goal(node_id),
                "zone": resource.zone.value,
            }
        return {
            "current_node": self.current_node,
            "permissions": {node_id: int(r.access_level) for node_id, r in self.resources.items()},
            "current_permission": int(current_permission),
            "known_nodes": list(self.resources.keys()),
            "adjacency": self.adjacency,
            "resources": resource_view,
            "diagnostics": {k: dict(v) for k, v in self.diagnostics.items()},
            "budget": self.budget,
            "diagnostic_cost": self.DIAGNOSTIC_COST,
            "attempt_cost": self.ATTEMPT_COST,
        }

    def start_action(self, action: Action) -> None:
        if action.kind == "STOP":
            self.log("AGENT_STOP | brak opłacalnej lub dostępnej akcji")
            self.terminated = True
            self.termination_reason = "agent_stop"
            return

        if action.target not in self.adjacency.get(self.current_node, []):
            self.log(f"INVALID_ACTION | {action.kind} target={action.target}")
            self.terminated = True
            self.termination_reason = "invalid_action"
            return

        target = self.resources[action.target]
        current_permission = self.resources[self.current_node].access_level
        if target.required_access > current_permission:
            self.log(f"ACCESS_REQUIREMENT_NOT_MET | target={target.id}")
            self.terminated = True
            self.termination_reason = "invalid_access_requirement"
            return

        if action.kind == "DIAGNOSE":
            if target.known:
                self.log(f"DIAGNOSE_SKIPPED | {target.id} already diagnosed")
                return
            if self.budget < self.DIAGNOSTIC_COST:
                self.log("BUDGET_EXHAUSTED | diagnostic")
                self.terminated = True
                self.termination_reason = "budget_exhausted"
                return
            self.budget -= self.DIAGNOSTIC_COST
            self.log(
                f"ACTION | DIAGNOSE {target.id} ({target.name}) "
                f"| cost={self.DIAGNOSTIC_COST} | budget={self.budget}"
            )
            self._schedule(self.DIAGNOSTIC_TIME, "DIAGNOSTIC_COMPLETED", target=target.id)
            return

        if action.kind == "ATTEMPT":
            if action.target not in self.diagnostics:
                self.log(f"INVALID_ACTION | ATTEMPT without diagnosis: {target.id}")
                self.terminated = True
                self.termination_reason = "attempt_without_diagnosis"
                return
            if self.budget < self.ATTEMPT_COST:
                self.log("BUDGET_EXHAUSTED | attempt")
                self.terminated = True
                self.termination_reason = "budget_exhausted"
                return
            self.budget -= self.ATTEMPT_COST
            self.log(
                f"ACTION | ATTEMPT_ACCESS {target.id} ({target.name}) "
                f"| cost={self.ATTEMPT_COST} | budget={self.budget}"
            )
            self.pending_attempt = {"target": target.id, "success": False, "detected": False, "blocked": False}
            self._schedule(self.ATTEMPT_TIME, "ATTEMPT_RESOLVED", target=target.id)
            return

        self.log(f"INVALID_ACTION | unknown kind={action.kind}")
        self.terminated = True
        self.termination_reason = "invalid_action"

    def process_next_event(self) -> None:
        event = heapq.heappop(self.events)
        self.time = event.time
        target_id = event.payload.get("target")
        target = self.resources.get(target_id) if target_id else None

        if event.kind == "DIAGNOSTIC_COMPLETED" and target:
            target.known = True
            source_permission = self.resources[self.current_node].access_level
            gain = max(0, int(target.granted_access) - int(source_permission))
            self.diagnostics[target.id] = {
                "risk": target.p_detection,
                "p_success": target.p_success,
                "permission_gain": gain,
                "is_goal": target.is_goal,
            }
            self.log(
                f"DIAGNOSTIC_COMPLETED | {target.id} "
                f"| p_success={target.p_success:.2f} "
                f"| risk(detection)={target.p_detection:.2f} "
                f"| permission_gain={gain} "
                f"| required={target.required_access.name} "
                f"| grant={target.granted_access.name}"
            )
            return

        if event.kind == "ATTEMPT_RESOLVED" and target and self.pending_attempt:
            roll = self.rng.random()
            success = roll < target.p_success
            self.pending_attempt["success"] = success
            self.log(
                f"ATTEMPT_RESOLVED | {target.id} | roll={roll:.3f} "
                f"| p_success={target.p_success:.2f} "
                f"| {'POTENTIAL_SUCCESS' if success else 'FAILURE'}"
            )
            if self.monitoring:
                self._schedule(0.1, "DETECTION_CHECK", target=target.id)
                self._schedule(1.0, "ACCESS_COMMIT", target=target.id)
            else:
                self._schedule(0.1, "ACCESS_COMMIT", target=target.id)
            return

        if event.kind == "DETECTION_CHECK" and target and self.pending_attempt:
            roll = self.rng.random()
            detected = roll < target.p_detection
            self.pending_attempt["detected"] = detected
            if detected:
                self.log(
                    f"DETECTION_TRIGGERED | {target.id} | roll={roll:.3f} "
                    f"| p_detection={target.p_detection:.2f}"
                )
                self._schedule(0.4, "DEFENSE_RESPONSE", target=target.id)
            else:
                self.log(
                    f"NO_DETECTION | {target.id} | roll={roll:.3f} "
                    f"| p_detection={target.p_detection:.2f}"
                )
            return

        if event.kind == "DEFENSE_RESPONSE" and target and self.pending_attempt:
            roll = self.rng.random()
            blocked = roll < self.BLOCK_GIVEN_DETECTION
            self.pending_attempt["blocked"] = blocked
            if blocked:
                self.log(
                    f"DEFENSE_ACTIVATED | {target.id} | roll={roll:.3f} "
                    f"| p_block_given_detection={self.BLOCK_GIVEN_DETECTION:.2f}"
                )
            else:
                self.log(f"ALERT_NOT_BLOCKED | {target.id} | system records alert, attempt continues")
            return

        if event.kind == "ACCESS_COMMIT" and target and self.pending_attempt:
            pending = self.pending_attempt
            self.pending_attempt = None
            if pending["blocked"]:
                self.log(f"ACCESS_BLOCKED | {target.id} | permission not granted")
                self.terminated = True
                self.termination_reason = "blocked"
                return
            if not pending["success"]:
                self.log(f"ACCESS_DENIED | {target.id} | current node unchanged")
                return

            target.access_level = target.granted_access
            self.current_node = target.id
            self.visited.add(target.id)
            self.log(
                f"ACCESS_GRANTED | {target.id} | new_permission={target.access_level.name} "
                f"| zone={target.zone.value}"
            )
            if target.is_goal and target.zone == Zone.HOST:
                self.log("BOUNDARY_CROSSED | protected host resource reached")
                self.terminated = True
                self.termination_reason = "success"
            return

        self.log(f"UNKNOWN_EVENT | {event.kind}")
        self.terminated = True
        self.termination_reason = "unknown_event"

    def run(self, agent: GoalOrientedRiskAwareAgent, max_events: int = 200) -> list[str]:
        processed = 0
        while not self.terminated and processed < max_events:
            if not self.events:
                action = agent.choose_action(self.observe())
                self.start_action(action)
                if self.terminated:
                    break
                if not self.events:
                    # Defensive guard: an action should schedule an event.
                    self.log("SIMULATION_STOP | no pending events")
                    self.terminated = True
                    self.termination_reason = "no_pending_events"
                    break

            self.process_next_event()
            processed += 1

        if not self.terminated:
            self.log("SIMULATION_STOP | max event count reached")
            self.terminated = True
            self.termination_reason = "max_events"

        self.log(
            f"END | result={self.termination_reason} | time={self.time:.1f} "
            f"| budget_remaining={self.budget} | visited={','.join(sorted(self.visited))}"
        )
        return self.logs


def main() -> None:
    env = SandboxSimulation(seed=1, monitoring=True, budget=12)
    agent = GoalOrientedRiskAwareAgent(risk_weight=0.8, goal_bonus=3.0)
    for line in env.run(agent):
        print(line)


if __name__ == "__main__":
    main()
