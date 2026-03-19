"""
LangGraph State Tanımı
- messages : Özetlenmiş mesaj geçmişi (kısa, insan-okunabilir)
- booking_context : Yapısal veriler — ID'ler, hiç mesaj geçmişine girmez
"""

from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class BookingContext(TypedDict, total=False):
    session_id: Optional[str]
    room_type_id: Optional[str]
    rate_plan_id: Optional[str]
    booking_reference: Optional[str]
    transfer_service_id: Optional[str]
    spa_service_id: Optional[str]
    room_description: Optional[str]
    selected_dates: Optional[dict]
    guest_count: Optional[int]


class HotelState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    booking_context: BookingContext
