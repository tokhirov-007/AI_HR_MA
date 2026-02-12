import os
from typing import List

class BotPermissions:
    """
    Handles HR-only access control for the Telegram Bot.
    """
    
    def __init__(self):
        # Hardcoded IDs (User choice)
        hr_ids_str = "1743337357"
        self.allowed_ids = []
        
        if hr_ids_str:
            try:
                self.allowed_ids = [int(i.strip()) for i in hr_ids_str.split(",") if i.strip()]
            except ValueError:
                print("WARNING: Invalid TELEGRAM_HR_IDS in .env. Should be a comma-separated list of integers.")

    def is_hr(self, user_id: int) -> bool:
        """Checks if a Telegram user ID is in the allowed list."""
        if not self.allowed_ids:
            return False
        return user_id in self.allowed_ids

    def get_hr_ids(self) -> List[int]:
        """Returns the list of all authorized HR IDs."""
        return self.allowed_ids
