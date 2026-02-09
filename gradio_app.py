"""
Abhimanyu Industries – HR RAG Chatbot
Robust Dark UI (Gradio 6.x compatible)
"""

import gradio as gr
from query_engine import HRQueryEngine

engine = None

def get_engine():
    global engine
    if engine is None:
        print("Initializing HR Engine...")
        engine = HRQueryEngine()
    return engine

def respond(message, history):
    """
    Gradio 6.x expects history as list of dicts with 'role' and 'content' keys
    """
    try:
        hr_engine = get_engine()
        answer, sources = hr_engine.answer_question(message)

        response = answer
        if sources:
            response += "\n\n---\n📚 Sources Used:\n"
            for src in sorted(set(sources)):
                response += f"- {src}\n"

        # Gradio 6.x format: list of message dictionaries
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        
        return history, ""

    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return history, ""

# ---------------- UI ----------------

custom_css = """
body, .gradio-container {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    font-family: Inter, system-ui, sans-serif;
}
textarea, input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
}
.message.user {
    background-color: #1e293b !important;
}
.message.bot {
    background-color: #020617 !important;
}
"""

with gr.Blocks() as demo:

    gr.Markdown(
        """
        # 🏢 Abhimanyu Industries – HR Assistant  
        _Internal HR RAG Chatbot_
        """
    )

    chatbot = gr.Chatbot(height=420)  # ✅ Removed 'type' parameter

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask an HR-related question...",
            scale=4
        )
        send = gr.Button("Send", scale=1)

    send.click(respond, [msg, chatbot], [chatbot, msg])
    msg.submit(respond, [msg, chatbot], [chatbot, msg])

    gr.Markdown(
        "⚠️ Answers are generated strictly from internal Abhimanyu Industries documents."
    )

# ---------------- LAUNCH ----------------

if __name__ == "__main__":
    print("🚀 Launching HR RAG Bot...")
    get_engine()

    demo.launch(
        server_name="127.0.0.1",
        server_port=None,
        share=True,
        css=custom_css
    )