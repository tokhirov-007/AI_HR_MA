from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from app.bot.permissions import BotPermissions
from app.bot.schemas import HRAction
import app.main as main_app # Use for access to global session_manager

router = Router()
permissions = BotPermissions()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    if not permissions.is_hr(message.from_user.id):
        await message.answer("⛔ <b>Access Denied.</b> This bot is for authorized HR only.", parse_mode="HTML")
        return
    
    await message.answer(
        f"👋 <b>Welcome, HR!</b>\n\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Status: 🟢 Authorized\n\n"
        f"You will receive notifications for all completed interviews here.",
        parse_mode="HTML"
    )

@router.callback_query()
async def process_hr_action(callback: CallbackQuery):
    if not permissions.is_hr(callback.from_user.id):
        await callback.answer("Forbidden", show_alert=True)
        return

    # Callback format: action:session_id
    data = callback.data.split(":")
    if len(data) != 2:
        await callback.answer("Invalid Data")
        return

    action_val, session_id = data
    
    # 1. Map to action status
    status_map = {
        HRAction.INVITE.value: "✅ INVITED",
        HRAction.REJECT.value: "❌ REJECTED",
        HRAction.REVIEW.value: "⏳ UNDER REVIEW"
    }
    
    status_text = status_map.get(action_val, "UNKNOWN")

    # 2. Logic to update backend status
    if main_app.session_manager:
        try:
            # We update INTERNAL status immediately
            # We update PUBLIC status ONLY if it's INVITE or REJECT
            # (Review might be an intermediate HR state)
            new_public = action_val if action_val in [HRAction.INVITE.value, HRAction.REJECT.value] else None
            
            await main_app.session_manager.update_status(
                session_id=session_id,
                new_internal=action_val.upper(),
                new_public=new_public,
                actor=f"HR_{callback.from_user.id}"
            )
            print(f"BOT ACTION: HR {callback.from_user.id} updated session {session_id} to {action_val}")
        except Exception as e:
            print(f"Error updating session status: {e}")
    else:
        print(f"BOT ACTION: HR {callback.from_user.id} set session {session_id} to {action_val} (MOCK - Manager not found)")

    # 3. Update the message to show the decision
    new_text = f"{callback.message.text}\n\n<b>───────────────────</b>\n" \
               f"<b>⚖️ HR DECISION:</b> {status_text}\n" \
               f"👤 <b>By:</b> {callback.from_user.full_name}"
    
    try:
        await callback.message.edit_text(text=new_text, parse_mode="HTML", reply_markup=None)
        await callback.answer(f"Decision saved: {status_text}")
    except Exception as e:
        print(f"Failed to update message: {e}")
        await callback.answer("Decision saved, but UI update failed.")
