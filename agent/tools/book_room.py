"""
Mock Tool: Rezervasyon Oluştur
"""

import json
import uuid
import random
from langchain_core.tools import tool


@tool
def create_booking(
    room_type_id: str,
    rate_plan_id: str,
    check_in: str,
    check_out: str,
    guest_name: str,
    guest_count: int,
) -> str:
    """
    Seçilen oda için rezervasyon oluşturur.

    Args:
        room_type_id: Oda tipi ID'si
        rate_plan_id: Tarife planı ID'si
        check_in: Giriş tarihi (YYYY-MM-DD)
        check_out: Çıkış tarihi (YYYY-MM-DD)
        guest_name: Misafir adı soyadı
        guest_count: Misafir sayısı
    """
    booking_id = f"BK-{uuid.uuid4().hex[:8].upper()}"
    session_id = f"SES-{uuid.uuid4().hex[:10].upper()}"
    payment_token = f"PAY-{uuid.uuid4().hex[:16].upper()}"

    return json.dumps({
        "status": "confirmed",
        "booking_reference": booking_id,
        "session_id": session_id,
        "confirmation_number": f"CONF-{random.randint(100000, 999999)}",
        "booking_details": {
            "room_type_id": room_type_id,
            "rate_plan_id": rate_plan_id,
            "check_in": check_in,
            "check_out": check_out,
            "guest_name": guest_name,
            "guest_count": guest_count,
            "meal_plan": "Kahvaltı dahil",
        },
        "payment": {
            "payment_token": payment_token,
            "payment_gateway_id": "GW-STRIPE-TR-001",
            "total_amount": 11070.00,
            "currency": "TRY",
            "installment_options": [1, 3, 6, 9, 12],
            "payment_status": "pending",
            "payment_due": "2025-03-20T23:59:00Z",
        },
        "cancellation": {
            "policy_id": "CP-FREE72H",
            "free_cancel_until": "2025-03-20T10:00:00Z",
            "cancel_url": f"https://hotel.example/cancel/{booking_id}",
        },
        "services_included": [],
        "meta": {
            "created_at": "2025-03-18T10:05:00Z",
            "source_channel": "chatbot",
            "property_name": "Güral Premier Hotels",
        },
    }, ensure_ascii=False, indent=2)
