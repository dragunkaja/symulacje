from environment import SandboxSimulation
from agents import GoalOrientedRiskAwareAgent

"""Abstract sandbox-boundary simulation demo.

This is a safe, synthetic model. It does not execute commands, exploits,
or interact with real containers or operating systems.

Run:
    python src/main.py
"""

def main() -> None:
    env = SandboxSimulation(seed=1, monitoring=True, budget=12)
    agent = GoalOrientedRiskAwareAgent(risk_weight=0.8, goal_bonus=3.0)
    for line in env.run(agent):
        print(line)


if __name__ == "__main__":
    main()