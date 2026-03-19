"""
response_node: Konuşmanın son yanıtını doğrular ve temizler.
LLM'den gelen AI mesajı tool call içermiyorsa bu node çalışır.
Gerekirse burada misafir için final formatlama yapılabilir.
"""

from agent.state import HotelState


def response_node(state: HotelState) -> dict:
    """
    Şu an pass-through görevi görüyor.
    İleride: yanıtı formatla, loglama ekle, session kapat vb.
    """
    # Son mesaj zaten agent_node'dan geldi, state değişmeden geçer
    return {}
