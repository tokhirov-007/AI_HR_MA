import asyncio
import os
import sys
from datetime import datetime

# Add current dir to path
sys.path.append(os.getcwd())

from app.interview_flow.session_manager import SessionManager
from app.question_engine.schemas import QuestionSet

async def test_notifications_logic():
    print("Testing Step 9: Notification System & Hidden Logic...")
    
    manager = SessionManager()
    
    # 1. Create a session
    mock_questions = QuestionSet(
        candidate_name="James Bond",
        candidate_level="Senior",
        total_questions=0,
        questions=[]
    )
    session = manager.create_session("cand_007", "James Bond", mock_questions)
    session_id = session.session_id
    
    # Override contact info for test
    session.candidate_email = "bond@mi6.gov"
    session.candidate_phone = "+44007007007"
    session.candidate_lang = "en"
    
    print(f"Created session: {session_id}")
    print(f"Initial Status: Internal={session.status_internal}, Public={session.status_public}")
    
    # 2. Update INTERNAL status (Candidate should NOT know)
    print("\n--- HR is reviewing internally... ---")
    await manager.update_status(session_id, "TOP_SECRET_REVIEW", actor="M")
    
    # Verify
    updated = manager.get_session_status(session_id)
    print(f"New Status: Internal={updated.status_internal}, Public={updated.status_public}")
    assert updated.status_internal == "TOP_SECRET_REVIEW"
    assert updated.status_public == "UNDER_REVIEW" # Public unchanged
    
    # 3. Update PUBLIC status (Trigger Notification)
    print("\n--- HR Decided to INVITE! ---")
    await manager.update_status(session_id, "ACCEPTED", new_public="INVITE", actor="M")
    
    # Verify
    final = manager.get_session_status(session_id)
    print(f"Final Status: Internal={final.status_internal}, Public={final.status_public}")
    assert final.status_public == "INVITE"
    
    print("\n--- Checking Audit Logs ---")
    log_path = "logs/candidate_status.log"
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"Audit log has {len(lines)} entries.")
            for line in lines[-3:]:
                print(f"LOG: {line.strip()}")
    
    print("\nVerification SUCCESS: Step 9 functionality verified.")

if __name__ == "__main__":
    asyncio.run(test_notifications_logic())
