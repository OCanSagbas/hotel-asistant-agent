"""
Mapper: search_rooms tool çıktısı
Ham JSON'dan sadece kritik alanları alır, booking_context'e yazar.
Mesaj geçmişine kısa özet döner.
"""

import json


def map_search_output(raw_output: str, context: dict) -> tuple[str, dict]:
    """
    search_rooms çıktısını işler.
    Çıkarılan alanlar: room_type_id, rate_plan_id, session_id, room_description
    """
    updated = dict(context)

    try:
        data = json.loads(raw_output)
    except (json.JSONDecodeError, TypeError):
        return " Oda arama sonucu işlenemedi.", updated

    if data.get("status") != "success":
        return " Oda arama başarısız oldu.", updated

    results = data.get("results", [])
    if not results:
        return " Kriterlerinize uygun oda bulunamadı.", updated

    # Tüm odaları listele
    room_lines = []
    for i, r in enumerate(results):  # En fazla 3 odayı listele
        room_name = r.get("room_name", "")
        price = r.get("pricing", {}).get("total_per_night", "?")
        rt_id = r.get("room_type_id", "")
        rp_id = r.get("rate_plan_id", "")
        meal = r.get("pricing", {}).get("meal_plan", "")
        room_lines.append(f"- {room_name} ({price} TL, {meal}) [room_type_id: {rt_id}, rate_plan_id: {rp_id}]")
    
    summary = f"{len(results)} uygun oda bulundu:\n" + "\n".join(room_lines)
    
    # En iyi eşleşmeyi varsayılan olarak contex'e yaz
    best = results[0]
    updated["room_type_id"] = best.get("room_type_id")
    updated["rate_plan_id"] = best.get("rate_plan_id")
    updated["room_description"] = best.get("room_name", "Seçili oda")
    if session_id := data.get("session_id"):
        updated["session_id"] = session_id

    return summary, updated
