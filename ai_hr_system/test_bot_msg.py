import asyncio
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot

# Add current dir to path to find app module
sys.path.append(os.getcwd())

from app.bot.notifications import BotNotificationManager
from app.scoring.schemas import FinalRecommendation, ScoreBreakdown, RecommendationLevel

async def test_send_notification():
    load_dotenv()
    
    # Hardcoded token
    token = "8302463815:AAEtgldpuQm0QW0jv3xJCSbmNExmuJ4yb1M"
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env")
        return

    print("🚀 Initializing test notification...")
    
    bot = Bot(token=token)
    notification_manager = BotNotificationManager(bot)

    # 1. Create a dummy recommendation (Simulation of Step 7 output)
    mock_rec = FinalRecommendation(
        session_id="test_session_123",
        candidate_name="Алексей Программистов",
        final_score=88,
        decision=RecommendationLevel.STRONG_HIRE,
        confidence="high",
        hr_comment="Excellent technical depth and perfectly authentic answers.",
        score_breakdown=ScoreBreakdown(
            knowledge_score=95.0,
            honesty_score=92.0,
            time_behavior_score=85.0,
            problem_solving_score=80.0
        ),
        flags=["Candidate is highly proficient", "No suspicious markers detected"],
        metadata={"difficulty_mix": "hard"}
    )

    # 2. Send notification to HR
    print(f"📬 Sending mock report for {mock_rec.candidate_name} to HR IDs...")
    
    try:
        await notification_manager.notify_new_candidate(mock_rec)
        print("✅ Notification task finished. Check your Telegram!")
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_send_notification())
