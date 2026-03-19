"""
Mapper: create_booking tool çıktısı
Ham JSON'dan sadece kritik alanları alır, booking_context'e yazar.
"""

import json


def map_booking_output(raw_output: str, context: dict) -> tuple[str, dict]:
    """
    create_booking çıktısını işler.
    Çıkarılan alanlar: booking_reference, session_id
    """
    updated = dict(context)

    try:
        data = json.loads(raw_output)
    except (json.JSONDecodeError, TypeError):
        return "Rezervasyon yanıtı işlenemedi.", updated

    if data.get("status") != "confirmed":
        return "Rezervasyon oluşturulamadı.", updated

    # Kritik ID'leri state'e yaz
    updated["booking_reference"] = data.get("booking_reference")
    if session_id := data.get("session_id"):
        updated["session_id"] = session_id

    confirmation = data.get("confirmation_number", "")
    ref = data.get("booking_reference", "")

    summary = (
        f"Rezervasyon oluşturuldu! "
        f"Onay numaranız: **{confirmation}** (Referans: {ref})."
    )
    return summary, updated
