"""
tool_node: LLM'in seçtiği tool'u çalıştırır.
Ham JSON'u doğrudan history'ye koymaz — mapper'a gönderir.
Mapper'dan dönen kısa özet history'ye eklenir, ID'ler booking_context'e yazılır.
"""

from langchain_core.messages import AIMessage, ToolMessage

from agent.state import HotelState
from agent.tools import ALL_TOOLS
from agent.mappers import MAPPER_REGISTRY

_TOOLS_BY_NAME = {t.name: t for t in ALL_TOOLS}


def tool_node(state: HotelState) -> dict:
    """
    1. LLM'in istediği tool'u çalıştır  → ham JSON
    2. Ham JSON'u mapper'a gönder        → kısa özet + güncel context
    3. Kısa özeti ToolMessage olarak ekle (HAM JSON GİRMİYOR)
    4. Güncel context'i state'e yaz
    """
    last_msg: AIMessage = state["messages"][-1]
    updated_context = dict(state.get("booking_context", {}))
    new_messages = []

    for call in last_msg.tool_calls:
        tool_name = call["name"]
        tool_fn = _TOOLS_BY_NAME.get(tool_name)

        # Tool'u çalıştır
        if tool_fn is None:
            raw = f'{{"error": "Bilinmeyen tool: {tool_name}"}}'
        else:
            try:
                raw = tool_fn.invoke(call["args"])
            except Exception as e:
                raw = f'{{"error": "{e}"}}'

        # Mapper: ham JSON → kısa özet + state güncelleme
        mapper = MAPPER_REGISTRY.get(tool_name)
        if mapper:
            summary, updated_context = mapper(raw, updated_context)
        else:
            summary = f"{tool_name} tamamlandı."

        # History'ye sadece kısa özet giriyor, ham JSON asla girmez
        new_messages.append(ToolMessage(
            content=summary,
            tool_call_id=call["id"],
            name=tool_name,
        ))

    return {
        "messages": new_messages,
        "booking_context": updated_context,
    }
