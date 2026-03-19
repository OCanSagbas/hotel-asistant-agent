"""
Mock Tool: Oda Arama (Akıllı Puanlama ve Sıralamalı)
Gerçek API'yi simüle eden dinamik hesaplama yapar.
"""

import json
import uuid
from langchain_core.tools import tool

ALL_ROOMS = [
    {
        "room_type_id": "RT-DLXSEA-456",
        "rate_plan_id": "RP-BB-FLEX-789",
        "internal_room_code": "ROOM_DLX_SEA_FLOOR3",
        "room_name": "Deluxe Deniz Manzaralı Oda",
        "description": "3. katta, balkonu bulunan deniz manzaralı lüks oda.",
        "floor": 3,
        "size_sqm": 45,
        "max_occupancy": 2,
        "beds": [{"type": "king", "count": 1}],
        "amenities": ["minibar", "safe", "bathtub", "balcony", "sea_view", "deniz"],
        "pricing": {
            "base_price_per_night": 4500.00,
            "taxes": 810.00,
            "service_charge": 225.00,
            "total_per_night": 5535.00,
            "total_stay": 11070.00,
            "currency": "TRY",
            "meal_plan": "Kahvaltı dahil",
            "cancellation_policy_id": "CP-FREE72H",
            "cancellation_policy": "72 saat öncesine kadar ücretsiz iptal.",
        },
        "availability": {"available": True, "min_stay_nights": 1, "booking_window_id": "BW-001", "last_available_rooms": 2},
        "images": ["https://cdn.hotel.example/rooms/dlx-sea-01.jpg"],
    },
    {
        "room_type_id": "RT-STDGRD-101",
        "rate_plan_id": "RP-RO-FLEX-200",
        "internal_room_code": "ROOM_STD_GRD_FLOOR1",
        "room_name": "Standart Bahçe Manzaralı Oda",
        "description": "1. katta bahçeye bakan standart oda.",
        "floor": 1,
        "size_sqm": 30,
        "max_occupancy": 2,
        "beds": [{"type": "double", "count": 1}],
        "amenities": ["minibar", "safe", "shower", "garden_view", "bahçe"],
        "pricing": {
            "base_price_per_night": 2800.00,
            "taxes": 504.00,
            "service_charge": 140.00,
            "total_per_night": 3444.00,
            "total_stay": 6888.00,
            "currency": "TRY",
            "meal_plan": "Sadece oda",
            "cancellation_policy_id": "CP-FREE48H",
            "cancellation_policy": "48 saat öncesine kadar ücretsiz iptal.",
        },
        "availability": {"available": True, "min_stay_nights": 2, "booking_window_id": "BW-002", "last_available_rooms": 5},
        "images": ["https://cdn.hotel.example/rooms/std-grd-01.jpg"],
    },
    {
        "room_type_id": "RT-KING-999",
        "rate_plan_id": "RP-ALL-FLEX-999",
        "internal_room_code": "ROOM_KING_FLOOR5",
        "room_name": "Premium Kral Dairesi",
        "description": "5. katta panoramik deniz manzaralı, jakuzili özel süit.",
        "floor": 5,
        "size_sqm": 120,
        "max_occupancy": 3,
        "beds": [{"type": "king", "count": 1}, {"type": "sofa", "count": 1}],
        "amenities": ["jakuzi", "minibar", "safe", "sea_view", "deniz", "butler", "süit", "lüks"],
        "pricing": {
            "base_price_per_night": 15000.00,
            "taxes": 2700.00,
            "service_charge": 750.00,
            "total_per_night": 18450.00,
            "total_stay": 36900.00,
            "currency": "TRY",
            "meal_plan": "Her şey dahil",
            "cancellation_policy_id": "CP-FREE72H",
            "cancellation_policy": "72 saat öncesine kadar ücretsiz iptal.",
        },
        "availability": {"available": True, "min_stay_nights": 1, "booking_window_id": "BW-003", "last_available_rooms": 1},
        "images": ["https://cdn.hotel.example/rooms/king-01.jpg"],
    },
    {
        "room_type_id": "RT-FAM-505",
        "rate_plan_id": "RP-HB-FLEX-500",
        "internal_room_code": "ROOM_FAM_SEA_FLOOR2",
        "room_name": "Geniş Aile Odası",
        "description": "2 ara kapılı yatak odasından oluşan, deniz veya havuz manzaralı aile odası.",
        "floor": 2,
        "size_sqm": 70,
        "max_occupancy": 5,
        "beds": [{"type": "queen", "count": 1}, {"type": "single", "count": 3}],
        "amenities": ["minibar", "safe", "bathtub", "balcony", "aile", "çocuk"],
        "pricing": {
            "base_price_per_night": 7000.00,
            "taxes": 1260.00,
            "service_charge": 350.00,
            "total_per_night": 8610.00,
            "total_stay": 17220.00,
            "currency": "TRY",
            "meal_plan": "Yarım Pansiyon",
            "cancellation_policy_id": "CP-FREE48H",
            "cancellation_policy": "48 saat öncesine kadar ücretsiz iptal.",
        },
        "availability": {"available": True, "min_stay_nights": 2, "booking_window_id": "BW-004", "last_available_rooms": 3},
        "images": ["https://cdn.hotel.example/rooms/fam-01.jpg"],
    },
    {
        "room_type_id": "RT-ECO-005",
        "rate_plan_id": "RP-RO-NONREF",
        "internal_room_code": "ROOM_ECO_BASEMENT",
        "room_name": "Ekonomik Fırsat Odası",
        "description": "Otelin iç kısımlarına bakan, kompakt 2 kişilik oda.",
        "floor": 0,
        "size_sqm": 22,
        "max_occupancy": 2,
        "beds": [{"type": "double", "count": 1}],
        "amenities": ["safe", "shower", "ekonomik", "ucuz"],
        "pricing": {
            "base_price_per_night": 1500.00,
            "taxes": 270.00,
            "service_charge": 75.00,
            "total_per_night": 1845.00,
            "total_stay": 3690.00,
            "currency": "TRY",
            "meal_plan": "Sadece oda",
            "cancellation_policy_id": "CP-NONREF",
            "cancellation_policy": "İptal edilemez, iade yapılmaz.",
        },
        "availability": {"available": True, "min_stay_nights": 1, "booking_window_id": "BW-005", "last_available_rooms": 10},
        "images": ["https://cdn.hotel.example/rooms/eco-01.jpg"],
    }
]


@tool
def search_rooms(check_in: str, check_out: str, guests: int = 1, preference: str = "", limit: int = 1, offset: int = 0) -> str:
    """
    Belirtilen tarihlerde uygun otel odalarını arar ve müşteri isteklerine göre (kişi sayısı, tercih) puanlayarak sıralar.

    Args:
        check_in: Giriş tarihi (YYYY-MM-DD)
        check_out: Çıkış tarihi (YYYY-MM-DD)
        guests: Misafir sayısı (varsayılan: 1)
        preference: Oda tercihi (varsayılan boş, örn: 'deniz')
        limit: Döndürülecek maksimum oda sayısı (varsayılan 1)
        offset: Atlanacak oda sayısı (varsayılan 0)
    """
    scored_results = []
    
    for room in ALL_ROOMS:
        # Kopya alıp hesaplama yapacağız
        room_data = dict(room)
        score = 0.0
        
        # 1. Kapasite Filtresi ve Puanlaması
        max_occ = room_data["max_occupancy"]
        if max_occ < guests:
            # Misafir sayısı oda kapasitesini aşıyorsa eliyoruz (göstermeye gerek yok)
            continue
            
        if max_occ == guests:
            score += 50.0  # Tam isabet kapasite
            room_data["match_reason"] = "Tam Kapasite Uyumu"
        else:
            # Oda istenenden büyükse, israf durumu: biraz daha az paun ver (her +1 kapasite için -5 puan düselim, ama 0'ın altına düşmesin)
            penalty = (max_occ - guests) * 5.0
            score += max(0.0, 30.0 - penalty)
            room_data["match_reason"] = "Kapasite Yeterli (Büyük Oda)"

        # 2. Tercih (Preference) Uyumu
        if preference:
            pref_lower = preference.lower()
            # Özelliklerde, isminde veya açıklamasında geçiyor mu?
            matches_pref = False
            for am in room_data["amenities"]:
                if pref_lower in am.lower() or am.lower() in pref_lower:
                    matches_pref = True
            
            if pref_lower in room_data["room_name"].lower() or pref_lower in room_data["description"].lower():
                 matches_pref = True
                 
            if matches_pref:
                score += 40.0
                room_data["match_reason"] += " + Tercih Uyumu!"
            else:
                score -= 10.0 # İstediği şey bu odada yoksa geriye düşsün
        
        # 3. Fiyat Uyumu (Ucuz olan çok az miktar daha öne geçsin, 1000 TL başına ~1 puan)
        price = room_data["pricing"]["total_per_night"]
        score += max(0.0, (20000 - price) / 1000.0)

        # Sonuç
        room_data["score"] = round(score, 2)
        scored_results.append(room_data)

    # Scored_results listesini puana göre azalan (descending) sırala
    scored_results.sort(key=lambda x: x["score"], reverse=True)

    # Offset ve limit (sayfalama) uygula
    total_found = len(scored_results)
    paginated_results = scored_results[offset : offset + limit]

    return json.dumps({
        "status": "success",
        "session_id": f"SES-{uuid.uuid4().hex[:10].upper()}",
        "search_metadata": {
            "search_id": f"SRCH-{uuid.uuid4().hex[:8].upper()}",
            "timestamp": "2026-03-19T10:00:00Z",
            "engine_version": "4.0.0 (Scoring Enabled)",
        },
        "search_params": {
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "preference": preference,
            "limit": limit,
            "offset": offset,
        },
        "results": paginated_results,
        "total_results": total_found,
    }, ensure_ascii=False, indent=2)
