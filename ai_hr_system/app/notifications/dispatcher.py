import os
import re
from typing import Dict, Optional
from app.notifications.email_service import EmailService
from app.notifications.sms_service import SMSService
from app.notifications.logger import NotificationLogger

class NotificationDispatcher:
    """
    Central dispatcher for all candidate notifications.
    Handles template parsing, language selection, and delivery tracking.
    """
    def __init__(self):
        self.email_svc = EmailService()
        self.sms_svc = SMSService()
        self.logger = NotificationLogger()
        self.template_path = os.path.join(os.path.dirname(__file__), "templates")

    async def send_final_decision(self, 
                                 candidate_id: str, 
                                 name: str, 
                                 email: str, 
                                 phone: str, 
                                 status_public: str, 
                                 lang: str = "en") -> bool:
        """
        Orchestrates the notification flow.
        1. Select template based on status.
        2. Select language variant.
        3. Try Email -> Fallback to SMS.
        """
        template_file = f"{status_public.lower()}.txt"
        content = self._get_template_content(template_file, lang, name)
        
        if not content:
            print(f"? DISPATCHER: Template not found for {status_public} in {lang}")
            return False

        # Try Email first
        subject = f"Interview Update - {status_public.upper()}"
        success = await self.email_svc.send_email(email, subject, content)
        
        if success:
            self.logger.log_notification(candidate_id, "EMAIL", status_public, "SUCCESS")
            return True
        
        # Fallback to SMS
        print(f"?? DISPATCHER: Email failed for {candidate_id}, trying SMS fallback...")
        sms_text = f"Update on your application: {status_public.upper()}. Check your email for details."
        sms_success = await self.sms_svc.send_sms(phone, sms_text)
        
        if sms_success:
            self.logger.log_notification(candidate_id, "SMS", status_public, "SUCCESS")
        else:
            self.logger.log_notification(candidate_id, "ALL", status_public, "FAILED")
            
        return sms_success

    def _get_template_content(self, filename: str, lang: str, name: str) -> Optional[str]:
        """Parses the multi-language template file."""
        path = os.path.join(self.template_path, filename)
        if not os.path.exists(path):
            return None
            
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()

        # Extract language block: [RU] ... [EN]
        pattern = rf"\[{lang.upper()}\]\n(.*?)(?=\n\[|$)"
        match = re.search(pattern, raw, re.DOTALL)
        
        if not match:
            # Fallback to EN if requested lang missing
            match = re.search(r"\[EN\]\n(.*?)(?=\n\[|$)", raw, re.DOTALL)
            
        if match:
            text = match.group(1).strip()
            # Basic variable substitution
            return text.replace("{{name}}", name)
            
        return None
