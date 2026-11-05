from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table


class SimulationLogger:
    def __init__(self):
        self.console = Console()
        self.logs = []

    def log(self, time: float, category: str, message: str):
        log_entry = {
            "time": time,
            "category": category,
            "message": message
        }

        self.logs.append(log_entry)

    def get_logs(self):
        return self.logs

    def display(self):
    # Kolory przypisane do kategorii komunikatów.
        colors = {
            "START": "bold cyan",
            "AGENT": "bold blue",
            "ACTION": "blue",
            "DIAGNOSTIC_COMPLETED": "cyan",
            "ATTEMPT_RESOLVED": "yellow",
            "NO_DETECTION": "green",
            "DETECTION": "bold red",
            "ACCESS_GRANTED": "bold green",
            "ACCESS_DENIED": "bold red",
            "BOUNDARY_CROSSED": "bold magenta",
            "DEFENSE": "bold red",
            "END": "bold white",
            "INFO": "white"
        }

        self.console.print()

        for entry in self.logs:
            time = entry["time"]
            category = entry["category"]
            message = entry["message"]

            color = colors.get(category, "white")

            # Tworzymy tekst pojedynczego komunikatu.
            line = Text()
            line.append(f"[{time:05.1f}] ", style="dim")
            line.append(f"{category:<22}", style=color)
            line.append(message)

            self.console.print(line)