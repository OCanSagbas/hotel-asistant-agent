"""
agent_node: LLM'i çağırır.
booking_context'teki ID'leri system prompt'a enjekte eder.
Tool call ya da son yanıt üretir.
"""

import os
import datetime
from dotenv import load_dotenv

from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.state import HotelState
from agent.tools import ALL_TOOLS

load_dotenv()

_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
).bind_tools(ALL_TOOLS)


def _build_system_prompt(context: dict) -> str:
    lines = []
    if context.get("room_type_id"):
        lines.append(f"- Seçili oda: {context.get('room_description', 'Oda')} (room_type_id: {context['room_type_id']})")
    if context.get("rate_plan_id"):
        lines.append(f"- Tarife planı: {context['rate_plan_id']}")
    if context.get("booking_reference"):
        lines.append(f"- Rezervasyon referansı: {context['booking_reference']}")
    if context.get("transfer_service_id"):
        lines.append(f"- Havalimanı transferi: Eklendi ({context['transfer_service_id']})")
    if context.get("spa_service_id"):
        lines.append(f"- SPA hizmeti: Eklendi ({context['spa_service_id']})")

    context_block = "\n".join(lines) if lines else "Henüz rezervasyon bilgisi yok."
    today_str = datetime.datetime.now().strftime("%Y-%m-%d %A")

    return f"""Sen Güral Premier Hotels'in yapay zeka asistanısın.
Misafirlere Türkçe, sıcak ve profesyonel bir dille yardım ediyorsun.
(Bugünün Tarihi: {today_str})

Mevcut rezervasyon durumu:
{context_block}

KURALLAR:
1. Asla kendi başına ID üretme — ID'ler sistem tarafından sana arama sonuçlarında (ToolMessage olarak) veya rezervasyon durumunda verilmektedir.
2. Oda aramak için search_rooms, rezervasyon için create_booking, ek hizmet için add_service kullan.
3. Teknik ID'leri (room_type_id vb.) misafire kesinlikle GÖSTERME.
4. create_booking çağrısında, misafirin seçtiği odaya ait room_type_id ve rate_plan_id'yi bulup kullan.
5. add_service çağrısında yukarıdaki booking_reference'ı kullan.
6. İlk aramayı her zaman sadece EN İYİ 1 odayı (limit=1, offset=0) getirecek şekilde yap ve onu öner.
7. Müşteri "başka seçenek var mı?" diye sorarsa, search_rooms aracını offset=1 ve limit=2 (geriye kalan en iyi 2 oda) parametreleri ile GİZLİCE tekrar çağırıp ona alternatifleri sun.
"""


def agent_node(state: HotelState) -> dict:
    """LLM'i booking_context'i dahil eden sistem promptuyla çağırır."""
    system_msg = SystemMessage(content=_build_system_prompt(state.get("booking_context", {})))
    response = _llm.invoke([system_msg] + state["messages"])
    return {"messages": [response]}
