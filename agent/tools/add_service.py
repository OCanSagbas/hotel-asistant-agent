"""
Mock Tool: Ek Hizmet Ekle (Havalimanı Transferi veya SPA)
"""

import json
import uuid
from langchain_core.tools import tool


@tool
def add_service(booking_reference: str, service_type: str, details: str = "") -> str:
    """
    Rezervasyona ek hizmet ekler.

    Args:
        booking_reference: Rezervasyon referans numarası
        service_type: Hizmet türü: 'airport_transfer' veya 'spa'
        details: Ek detaylar (uçuş no, SPA paketi vb.)
    """
    service_id = f"SVC-{uuid.uuid4().hex[:8].upper()}"

    if service_type == "airport_transfer":
        service_data = {
            "service_id": service_id,
            "service_type": "airport_transfer",
            "transfer_service_id": service_id,
            "provider": "VIP Transfer Co.",
            "provider_id": "PROV-VIP-TR-007",
            "vehicle": "Mercedes Vito",
            "vehicle_capacity": 8,
            "driver_id": "DRV-4521",
            "pickup_airport": "IST",
            "pickup_terminal": "Terminal 1",
            "hotel_address": "Çırağan Caddesi No:1, Beşiktaş, İstanbul",
            "estimated_duration_min": 45,
            "price": 1200.00,
            "currency": "TRY",
            "tracking_url": f"https://transfer.hotel.example/track/{service_id}",
        }
    elif service_type == "spa":
        service_data = {
            "service_id": service_id,
            "service_type": "spa",
            "spa_service_id": service_id,
            "package_name": "Güral Premier Rahatlama Paketi",
            "package_id": "SPA-PKG-BSP-002",
            "duration_min": 120,
            "includes": ["Swedish masaj (60 dk)", "Türk hamamı (30 dk)", "Aromaterapi (30 dk)"],
            "therapist_id": "THERA-0088",
            "available_slots": ["10:00", "14:00", "16:30"],
            "session_date": "2025-03-22",
            "price": 2500.00,
            "currency": "TRY",
            "spa_location": "Bodrum Kat, Havuz Kenarı",
        }
    else:
        service_data = {"error": "Bilinmeyen hizmet türü", "service_type": service_type}

    return json.dumps({
        "status": "success",
        "booking_reference": booking_reference,
        "service": service_data,
        "updated_booking_total": 13770.00 if service_type == "airport_transfer" else 13570.00,
        "meta": {"added_at": "2025-03-18T10:10:00Z", "operator_id": "OP-CONCIERGE-12"},
    }, ensure_ascii=False, indent=2)
