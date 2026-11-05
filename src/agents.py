from models import Action, Permission

from typing import Any


class GoalOrientedRiskAwareAgent:
    """Rule-based agent: diagnose candidate nodes, then rank them by utility."""
    """
    Agent podejmujący decyzje na podstawie:
    - możliwości osiągnięcia celu,
    - ryzyka wykrycia,
    - kosztu działania.
    """

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
