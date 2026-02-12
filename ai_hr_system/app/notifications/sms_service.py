import asyncio

class SMSService:
    """
    Simulates a fallback SMS delivery service.
    """
    async def send_sms(self, phone: str, text: str) -> bool:
        """
        Sends an SMS. In production, this would use Twilio/Gateways.
        """
        print(f"SMS SERVICE: Sending to {phone}...")
        print(f"   Text: {text}")
        
        await asyncio.sleep(0.3)
        
        print(f"SMS SERVICE: Sent alert to {phone}")
        return True
