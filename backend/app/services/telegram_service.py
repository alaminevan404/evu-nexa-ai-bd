import httpx
from typing import Dict, Any
from app.core.config import settings

class TelegramService:
    @staticmethod
    async def send_signal_notification(analysis_data: Dict[str, Any]):
        """Dispatches formatted HTML signal notification to Telegram channel/bot."""
        if not settings.TELEGRAM_BOT_TOKEN or "Dummy" in settings.TELEGRAM_BOT_TOKEN:
            return {"status": "skipped", "reason": "No valid Telegram bot token configured."}

        direction = analysis_data.get("direction")
        emoji = "🟢 <b>BULLISH CALL</b>" if direction == "BULLISH_CALL" else ("🔴 <b>BEARISH PUT</b>" if direction == "BEARISH_PUT" else "⚠️ <b>NEUTRAL</b>")
        
        message = (
            f"🚀 <b>EVU NEXA AI - HIGH CONFIDENCE SIGNAL</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Asset:</b> <code>{analysis_data.get('asset_symbol')}</code>\n"
            f"<b>Timeframe:</b> <code>{analysis_data.get('timeframe')}</code>\n"
            f"<b>Action:</b> {emoji}\n"
            f"<b>Confidence Score:</b> <code>{analysis_data.get('confidence_score')}%</code>\n"
            f"<b>Risk Level:</b> <code>{analysis_data.get('risk_level')}</code>\n"
            f"<b>Recommended Expiry:</b> <code>{analysis_data.get('recommended_expiry')}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 <b>AI Reasoning:</b>\n"
            f"<i>{analysis_data.get('ai_reasoning')[:300]}...</i>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚡ <i>EVU NEXA AI Terminal | Support: {settings.TELEGRAM_SUPPORT_USERNAME}</i>"
        )

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHANNEL_ID or "@evu_nexa_signals",
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(url, json=payload)
                return resp.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

telegram_service = TelegramService()
