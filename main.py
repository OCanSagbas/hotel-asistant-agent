"""
Demo Senaryo — Case Study'deki iki turlu konuşmayı çalıştırır.
"""

from langchain_core.messages import HumanMessage
from agent.graph import hotel_agent
from agent.state import HotelState


def print_state(state: HotelState, label: str):
    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'='*60}")

    print(f"\nMESAJ GEÇMİŞİ ({len(state['messages'])} mesaj):")
    for i, msg in enumerate(state["messages"]):
        content = str(msg.content)
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"  [{i}] {type(msg).__name__}: {preview}")

    print(f"\n BOOKING CONTEXT:")
    ctx = state.get("booking_context", {})
    if ctx:
        for k, v in ctx.items():
            if v is not None:
                print(f"  {k}: {v}")
    else:
        print("  (boş)")

    tool_msgs = [m for m in state["messages"] if type(m).__name__ == "ToolMessage"]
    if tool_msgs:
        max_len = max(len(str(m.content)) for m in tool_msgs)
        icon = "✅" if max_len < 300 else "UZUN!"
        print(f"\n En uzun tool mesajı: {max_len} karakter {icon}")


# ── Tur 1: Oda Arama ──────────────────────────────────────────────────

print("\n🏨 OTEL ASİSTANI DEMO BAŞLIYOR...\n")
print("👤 Kullanıcı: Hafta sonu için 2 kişilik deniz manzaralı oda arıyorum.")

state = hotel_agent.invoke(
    {
        "messages": [HumanMessage(content="Hafta sonu için 2 kişilik deniz manzaralı bir oda arıyorum. (22-23 Mart 2025)")],
        "booking_context": {},
    },
    config={"recursion_limit": 10},
)

print_state(state, "Tur 1 — Oda Arama")
print(f"\n🤖 Asistan: {state['messages'][-1].content}")

# ── Tur 2: Rezervasyon + Transfer + SPA ───────────────────────────────

print("\n" + "-"*60)
print("👤 Kullanıcı: Harika, bu odayı ayırt. Havalimanı transferi ve SPA da ekler misin?")

state = hotel_agent.invoke(
    {
        **state,
        "messages": state["messages"] + [
            HumanMessage(
                content=(
                    "Harika, bu odayı benim adıma ayırt lütfen. "
                    "Adım: Ahmet Yılmaz, 22-23 Mart 2025, 2 kişi. "
                    "Havalimanı transferi ve SPA paketi de ekler misin?"
                )
            )
        ],
    },
    config={"recursion_limit": 20},
)

print_state(state, "Tur 2 — Rezervasyon + Transfer + SPA")
print(f"\n🤖 Asistan: {state['messages'][-1].content}")

# ── Doğrulama ─────────────────────────────────────────────────────────

print("\n" + "="*60)
print("🧪 OTOMATİK KONTROLLER")
print("="*60)

ctx = state.get("booking_context", {})
tool_msgs = [m for m in state["messages"] if type(m).__name__ == "ToolMessage"]

checks = [
    ("room_type_id state'te dolu", bool(ctx.get("room_type_id"))),
    ("rate_plan_id state'te dolu", bool(ctx.get("rate_plan_id"))),
    ("booking_reference state'te dolu", bool(ctx.get("booking_reference"))),
    ("transfer_service_id state'te dolu", bool(ctx.get("transfer_service_id"))),
    ("spa_service_id state'te dolu", bool(ctx.get("spa_service_id"))),
    ("Tool mesajları kısa (<300 karakter)",
     all(len(str(m.content)) < 300 for m in tool_msgs) if tool_msgs else True),
]

for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")

if all(ok for _, ok in checks):
    print("\n🎉 Tüm kontroller geçti! Context Rot önleme başarılı.")
else:
    print("\n⚠️ Bazı kontroller başarısız.")
