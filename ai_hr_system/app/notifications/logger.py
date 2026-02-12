from datetime import datetime
import json
import os

class NotificationLogger:
    """
    Logs status changes and notification events for audit trail.
    """
    def __init__(self, log_file: str = "logs/candidate_status.log"):
        self.log_path = os.path.join(os.getcwd(), log_file)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_status_change(self, candidate_id: str, old_status: str, new_status: str, actor: str):
        """Logs when an HR manager changes a candidate status."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "status_change",
            "candidate_id": candidate_id,
            "from": old_status,
            "to": new_status,
            "actor": actor
        }
        self._write(entry)

    def log_notification(self, candidate_id: str, channel: str, status: str, result: str):
        """Logs the result of a notification delivery."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "notification_sent",
            "candidate_id": candidate_id,
            "channel": channel,
            "target_status": status,
            "result": result
        }
        self._write(entry)

    def _write(self, entry: dict):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"AUDIT LOG: {entry['event']} for {entry.get('candidate_id')}")
