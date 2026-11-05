
class SimulationLogger:
    def __init__(self):
        self.logs = []

    def log(self, time: float, category: str, message: str):
        log_entry = f"[{time:05.1f}] [{category}] {message}"
        self.logs.append(log_entry)

    def get_logs(self):
        return self.logs