"""
Mapper: add_service tool çıktısı (havalimanı transferi ve SPA)
Ham JSON'dan sadece kritik alanları alır, booking_context'e yazar.
"""

import json


def map_service_output(raw_output: str, context: dict) -> tuple[str, dict]:
    """
    add_service çıktısını işler.
    Çıkarılan alanlar: transfer_service_id veya spa_service_id
    """
    updated = dict(context)

    try:
        data = json.loads(raw_output)   
    except (json.JSONDecodeError, TypeError):
        return " Hizmet yanıtı işlenemedi.", updated

    if data.get("status") != "success":
        return " Hizmet eklenemedi.", updated

    service = data.get("service", {})
    service_type = service.get("service_type")

    if service_type == "airport_transfer":
        # Kritik ID'yi state'e yaz
        updated["transfer_service_id"] = service.get("transfer_service_id") or service.get("service_id")
        vehicle = service.get("vehicle", "")
        duration = service.get("estimated_duration_min", "?")
        price = service.get("price", "?")
        summary = (
            f"Havalimanı transferi eklendi! "
            f"{vehicle} ile ~{duration} dk. Ücret: {price} TL."
        )

    elif service_type == "spa":
        # Kritik ID'yi state'e yaz
        updated["spa_service_id"] = service.get("spa_service_id") or service.get("service_id")
        package = service.get("package_name", "SPA Paketi")
        duration = service.get("duration_min", "?")
        price = service.get("price", "?")
        summary = (
            f"SPA rezervasyonu eklendi! "
            f"{package} ({duration} dk). Ücret: {price} TL."
        )

    else:
        summary = "Ek hizmet eklendi."

    return summary, updated
