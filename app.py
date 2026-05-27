import gradio as gr

# Load settings first (validates OPENAI_API_KEY)
import config.settings  # noqa: F401

# ------------------------------------------------------------------
# Liberty Mutual brand CSS
# ------------------------------------------------------------------

LM_CSS = """
:root {
    --lm-blue:       #1A1446;
    --lm-yellow:     #FFD000;
    --lm-dark-navy:  #002663;
    --lm-white:      #FFFFFF;
    --lm-light-gray: #F4F4F4;
    --lm-text-dark:  #1A1446;
    --lm-text-light: #FFFFFF;
}

/* ── Page shell ───────────────────────────────────────────────── */
body, .gradio-container {
    background-color: var(--lm-light-gray) !important;
}
.gradio-container {
    max-width: 880px !important;
    margin: 0 auto !important;
}

/* ── Header banner ────────────────────────────────────────────── */
#lm-header {
    background-color: var(--lm-blue);
    padding: 24px 28px 20px;
    border-radius: 8px;
    margin-bottom: 4px;
}
#lm-header h1 {
    color: var(--lm-white);
    margin: 0 0 6px;
    font-size: 1.6rem;
}
#lm-header p {
    color: var(--lm-white);
    margin: 0 0 4px;
    opacity: 0.92;
}
#lm-header code {
    background-color: rgba(255, 255, 255, 0.12);
    color: var(--lm-yellow);
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.88em;
}

/* ── Chatbot container ────────────────────────────────────────── */
.chatbot {
    background-color: var(--lm-white) !important;
    border: 1px solid rgba(26, 20, 70, 0.15) !important;
    border-radius: 8px !important;
}

/* ── Bubble backgrounds ───────────────────────────────────────── */
.message.bot  .bubble-wrap { background-color: var(--lm-blue)   !important; }
.message.user .bubble-wrap { background-color: var(--lm-yellow) !important; }

/* ── Bubble text — JS luminance overrides these at runtime ───── */
.message.bot  .bubble-wrap,
.message.bot  .bubble-wrap * { color: var(--lm-white) !important; }
.message.user .bubble-wrap,
.message.user .bubble-wrap * { color: var(--lm-blue)  !important; }

/* ── Minimum width so short messages aren't a sliver ─────────── */
.message .bubble-wrap {
    min-width: 80px !important;
    width: fit-content !important;
    max-width: 80% !important;
    box-sizing: border-box !important;
}
.message.user { justify-content: flex-end !important; }
.message.bot  { justify-content: flex-start !important; }

/* ── Primary button (Send) ────────────────────────────────────── */
button.primary {
    background-color: var(--lm-yellow) !important;
    color: var(--lm-blue) !important;
    border: none !important;
    font-weight: 700 !important;
}
button.primary:hover {
    background-color: #E6BB00 !important;
    color: var(--lm-blue) !important;
}

/* ── Secondary button (New Migration) ────────────────────────── */
button.secondary {
    background-color: transparent !important;
    color: var(--lm-blue) !important;
    border: 2px solid var(--lm-blue) !important;
    font-weight: 600 !important;
}
button.secondary:hover {
    background-color: var(--lm-blue) !important;
    color: var(--lm-white) !important;
}

/* ── Text input ───────────────────────────────────────────────── */
input[type=text], textarea {
    background-color: var(--lm-white) !important;
    border: 1px solid rgba(26, 20, 70, 0.3) !important;
    color: var(--lm-text-dark) !important;
    border-radius: 6px !important;
}
input[type=text]:focus, textarea:focus {
    border-color: var(--lm-blue) !important;
    box-shadow: 0 0 0 3px rgba(26, 20, 70, 0.14) !important;
    outline: none !important;
}

/* ── Examples ─────────────────────────────────────────────────── */
.examples-holder {
    background-color: var(--lm-white) !important;
    border: 1px solid rgba(26, 20, 70, 0.12) !important;
    border-radius: 8px !important;
}
.examples-holder .example {
    background-color: var(--lm-light-gray) !important;
    color: var(--lm-blue) !important;
    border: 1px solid rgba(26, 20, 70, 0.18) !important;
    border-radius: 6px !important;
}
.examples-holder .example:hover {
    background-color: var(--lm-blue) !important;
    color: var(--lm-yellow) !important;
    border-color: var(--lm-blue) !important;
}

/* ── Labels ───────────────────────────────────────────────────── */
label span, .label-wrap span {
    color: var(--lm-text-dark) !important;
    font-weight: 600 !important;
}

/* ── Gradio footer ────────────────────────────────────────────── */
footer {
    background-color: var(--lm-dark-navy) !important;
    padding: 12px 24px !important;
}
footer a, footer span {
    color: var(--lm-yellow) !important;
}
"""

# ------------------------------------------------------------------
# Dynamic text-color JS (WCAG luminance — runs in browser)
# ------------------------------------------------------------------

LM_JS = """
() => {
    function relativeLuminance(r, g, b) {
        return [r, g, b].reduce((acc, c, i) => {
            const v = c / 255;
            const lin = v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
            return acc + lin * [0.2126, 0.7152, 0.0722][i];
        }, 0);
    }

    function applyTextColor(bubble) {
        const bg = window.getComputedStyle(bubble).backgroundColor;
        const m  = bg.match(/[\\d.]+/g);
        if (!m || m.length < 3) return;
        // WCAG: white text when luminance < 0.179 (dark bg), dark otherwise
        const lum   = relativeLuminance(+m[0], +m[1], +m[2]);
        const color = lum < 0.179 ? '#FFFFFF' : '#1A1446';
        bubble.style.setProperty('color', color, 'important');
        bubble.querySelectorAll('p, span, a, strong, em, li, code, pre, td').forEach(el => {
            el.style.setProperty('color', 'inherit', 'important');
        });
    }

    function processBubbles() {
        document.querySelectorAll('.bubble-wrap').forEach(applyTextColor);
    }

    processBubbles();
    new MutationObserver(processBubbles).observe(document.body, {
        childList: true,
        subtree:   true,
    });
}
"""

from llm.agent import MigrationAgent
from llm.tool_registry import build_default_registry
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_postgres,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

# ------------------------------------------------------------------
# Wire everything together
# ------------------------------------------------------------------

registry = build_default_registry(
    migrate_pg_to_bq    = migrate_postgres_to_bigquery,
    migrate_csv_to_pg   = migrate_csv_to_postgres,
    migrate_s3_to_sf    = migrate_s3_to_snowflake,
    migrate_mongo_to_s3 = migrate_mongo_to_s3,
)

agent = MigrationAgent(registry=registry)

# ------------------------------------------------------------------
# Gradio callbacks
# ------------------------------------------------------------------

def respond(user_message: str, history: list[dict]) -> tuple:
    """Called on every user message."""
    if not user_message.strip():
        return history, ""
    reply = agent.chat(user_message)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    return history, ""


def reset_session() -> tuple:
    """Called when the user clicks 'New Migration'."""
    agent.reset()
    return [], ""


# ------------------------------------------------------------------
# Gradio UI
# ------------------------------------------------------------------

with gr.Blocks(title="migrate.ai", css=LM_CSS, js=LM_JS) as demo:

    gr.HTML(
        """
        <div id="lm-header">
            <h1>migrate.ai</h1>
            <p><strong>AI-powered data migration assistant</strong></p>
            <p>
                Tell me what you want to migrate and I'll guide you through it.<br>
                Sources: <code>postgres</code> <code>csv</code> <code>s3</code> <code>mongo</code>
                &nbsp;→&nbsp;
                Destinations: <code>bigquery</code> <code>postgres</code> <code>s3</code> <code>snowflake</code>
            </p>
        </div>
        """
    )

    chatbot = gr.Chatbot(
        label="Migration Chat",
        height=480,
    )

    with gr.Row():
        msg_input = gr.Textbox(
            placeholder="e.g. I want to migrate my Postgres table to BigQuery",
            show_label=False,
            scale=9,
        )
        send_btn = gr.Button("Send", variant="primary", scale=1)

    with gr.Row():
        reset_btn = gr.Button("🔄 New Migration", variant="secondary")

    gr.Examples(
        examples=[
            "I want to migrate data from Postgres to BigQuery",
            "I need to load a CSV file into Postgres",
            "Export a MongoDB collection to S3",
            "Move data from S3 to Snowflake",
        ],
        inputs=msg_input,
        label="Quick starts",
    )

    # Event bindings
    send_btn.click(respond, [msg_input, chatbot], [chatbot, msg_input])
    msg_input.submit(respond, [msg_input, chatbot], [chatbot, msg_input])
    reset_btn.click(reset_session, outputs=[chatbot, msg_input])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)