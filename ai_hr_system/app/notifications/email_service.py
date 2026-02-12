import asyncio

class EmailService:
    """
    Simulates an asynchronous Email delivery service (SMTP/SendGrid/SES).
    """
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Sends an email. In production, this would use a real provider.
        """
        print(f"EMAIL SERVICE: Sending to {to_email}...")
        print(f"   Subject: {subject}")
        print(f"   Body: {body[:50]}...")
        
        # Simulate network latency
        await asyncio.sleep(0.5)
        
        print(f"EMAIL SERVICE: Successfully delivered to {to_email}")
        return True
