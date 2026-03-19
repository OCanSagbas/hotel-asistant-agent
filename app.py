"""
Güral Premier Hotels — Gradio Chatbot Arayüzü (Yalın Sürüm)
"""

import gradio as gr
from langchain_core.messages import HumanMessage
from agent.graph import hotel_agent


def _render_context(ctx: dict) -> str:
    if not ctx:
        return "*Henüz rezervasyon bilgisi yok.*"

    lines = []
    for key, value in ctx.items():
        if value is not None:
            lines.append(f"- **{key}**: `{value}`")
    return "\n".join(lines)


def chat(user_message: str, history: list, agent_state: dict):
    if not user_message.strip():
        return history, agent_state, _render_context(agent_state.get("booking_context", {})), ""

    # Yeni state oluştur
    if not agent_state.get("messages"):
        new_state = {
            "messages": [HumanMessage(content=user_message)],
            "booking_context": {},
        }
    else:
        new_state = {
            **agent_state,
            "messages": agent_state["messages"] + [HumanMessage(content=user_message)],
        }

    # Ajanı çalıştır
    try:
        result_state = hotel_agent.invoke(new_state, config={"recursion_limit": 20})
    except Exception as e:
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": f"Hata oluştu: {e}"})
        return history, agent_state, _render_context(agent_state.get("booking_context", {})), ""

    # Son asistan mesajını al
    last_msg = result_state["messages"][-1]
    
    if isinstance(last_msg.content, list):
        parts = []
        for block in last_msg.content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        assistant_text = "\n".join(parts)
    else:
        assistant_text = str(last_msg.content)

    # Geçmişi dict formatında tutuyoruz (Gradio 6 uyumlu)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_text})

    # Güncel context markdown
    ctx_md = _render_context(result_state.get("booking_context", {}))

    return history, result_state, ctx_md, ""


def reset_session():
    return [], {}, "*Henüz rezervasyon bilgisi yok.*"


# Daha sade bir arayüz tasarımı
with gr.Blocks(title="Güral Premier Hotels") as demo:

    agent_state = gr.State({})

    gr.Markdown("# 🏨 Güral Premier Hotels")
    gr.Markdown("Yapay zeka asistanınız — oda arama, rezervasyon ve ek hizmetler için buradayım.")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Sohbet", value=[], height=500)
            
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Mesajınızı yazın ve Enter'a basın...", 
                    show_label=False, 
                    scale=5
                )
                send_btn = gr.Button("Gönder", variant="primary", scale=1)
            
            with gr.Row():
                reset_btn = gr.Button("Sohbeti Sıfırla", size="sm")

            gr.Examples(
                examples=[
                    "Hafta sonu için 2 kişilik deniz manzaralı oda arıyorum.",
                    "22-23 Mart tarihleri için müsait odalarınız var mı?",
                    "Premier suite hakkında bilgi alabilir miyim?"
                ],
                inputs=msg_input,
                label="Örnek Mesajlar"
            )

        with gr.Column(scale=1):
            gr.Markdown("### 📋 Rezervasyon Durumu")
            context_display = gr.Markdown(value="*Henüz rezervasyon bilgisi yok.*")
            gr.Markdown("---")
            gr.Markdown("*Agent: Gemini 2.5 Flash*")

    # Enter veya butona basıldığında tetiklenen fonksiyon
    msg_input.submit(
        fn=chat,
        inputs=[msg_input, chatbot, agent_state],
        outputs=[chatbot, agent_state, context_display, msg_input],
    )

    send_btn.click(
        fn=chat,
        inputs=[msg_input, chatbot, agent_state],
        outputs=[chatbot, agent_state, context_display, msg_input],
    )

    reset_btn.click(
        fn=reset_session,
        inputs=[],
        outputs=[chatbot, agent_state, context_display],
    )


if __name__ == "__main__":
    import os
    # .env dosyasından kullanıcı verilerini al, bulamazsa varsayılan admin/1234 kullan.
    admin_user = os.getenv("ADMIN_USER", "revloai")
    admin_pass = os.getenv("ADMIN_PASS", "revloai123")
    
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        show_error=True,
        auth=(admin_user, admin_pass),
        auth_message="🔒 Güral Premier Asistan Girişi"
    )
