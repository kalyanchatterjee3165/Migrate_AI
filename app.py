import gradio as gr

# Load settings first (validates OPENAI_API_KEY)
import config.settings as settings

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
.chatbot,
.chatbot > div,
.chatbot .wrap,
.chatbot .scroll-hide {
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

/* ── Examples / Quick starts (Gradio 6 uses .dataset) ────────── */
.dataset {
    background-color: var(--lm-white) !important;
    border: 1px solid rgba(26, 20, 70, 0.12) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
.dataset table {
    background-color: var(--lm-white) !important;
    width: 100% !important;
}
.dataset tbody tr {
    background-color: var(--lm-light-gray) !important;
    cursor: pointer !important;
    transition: background-color 0.15s ease, color 0.15s ease !important;
}
.dataset tbody tr:hover {
    background-color: var(--lm-blue) !important;
}
.dataset tbody tr td,
.dataset tbody tr td * {
    color: var(--lm-blue) !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
}
.dataset tbody tr:hover td,
.dataset tbody tr:hover td * {
    color: var(--lm-yellow) !important;
}

/* ════════════════════════════════════════════════════════════════
   LOGIN / AUTH PAGE — Liberty Mutual brand palette
   ════════════════════════════════════════════════════════════════ */

/* ── Page background ──────────────────────────────────────────── */
body:has(.login) {
    background-color: var(--lm-light-gray) !important;
    min-height: 100vh !important;
}

/* ── Card ─────────────────────────────────────────────────────── */
.login {
    background-color: var(--lm-white) !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(26, 20, 70, 0.08),
                0 8px 32px rgba(26, 20, 70, 0.12) !important;
    overflow: hidden !important;  /* lets the header strip sit flush */
}

/* ── Blue header strip at top of card ────────────────────────── */
.login::before {
    content: "migrate.ai" !important;
    display: block !important;
    background-color: var(--lm-blue) !important;
    color: var(--lm-white) !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 14px 28px !important;
}

/* ── Title ────────────────────────────────────────────────────── */
.login h1 {
    color: var(--lm-blue) !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin: 0 0 4px !important;
}

/* ── Auth message (subtitle) ──────────────────────────────────── */
.login .auth-message {
    color: #444 !important;
    font-size: 0.9rem !important;
    margin-bottom: 22px !important;
}

/* ── Labels ───────────────────────────────────────────────────── */
.login label,
.login label span {
    color: var(--lm-text-dark) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
}

/* ── Placeholders ─────────────────────────────────────────────── */
.login input::placeholder {
    color: rgba(26, 20, 70, 0.35) !important;
}

/* ── Input fields ─────────────────────────────────────────────── */
.login input[type=text],
.login input[type=password] {
    background-color: var(--lm-white) !important;
    border: 1.5px solid rgba(26, 20, 70, 0.25) !important;
    border-radius: 6px !important;
    color: var(--lm-text-dark) !important;
    padding: 10px 14px !important;
    width: 100% !important;
    font-size: 0.95rem !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
.login input[type=text]:focus,
.login input[type=password]:focus {
    border-color: var(--lm-blue) !important;
    box-shadow: 0 0 0 3px rgba(26, 20, 70, 0.13) !important;
    outline: none !important;
}
.login input[type=text]:hover,
.login input[type=password]:hover {
    border-color: rgba(26, 20, 70, 0.5) !important;
}

/* ── Primary login button ─────────────────────────────────────── */
.login button[type=submit],
.login button.primary {
    background-color: var(--lm-yellow) !important;
    color: var(--lm-blue) !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 11px 20px !important;
    margin-top: 18px !important;
    cursor: pointer !important;
    letter-spacing: 0.02em !important;
    transition: background-color 0.15s ease !important;
}
.login button[type=submit]:hover,
.login button.primary:hover {
    background-color: #E6BB00 !important;
}
.login button[type=submit]:active,
.login button.primary:active {
    background-color: #D4AC00 !important;
}

/* ── Secondary / outline buttons ─────────────────────────────── */
.login button.secondary {
    background-color: transparent !important;
    color: var(--lm-blue) !important;
    border: 1.5px solid var(--lm-blue) !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
    transition: background-color 0.15s ease, color 0.15s ease !important;
}
.login button.secondary:hover {
    background-color: var(--lm-blue) !important;
    color: var(--lm-white) !important;
}

/* ── Links (Forgot password / Sign up) ───────────────────────── */
.login a {
    color: var(--lm-blue) !important;
    text-decoration: underline !important;
    font-weight: 500 !important;
}
.login a:hover {
    color: var(--lm-dark-navy) !important;
    text-decoration-thickness: 2px !important;
}

/* ── Icons on light background ────────────────────────────────── */
.login svg,
.login .icon {
    color: var(--lm-blue) !important;
    fill: var(--lm-blue) !important;
}

/* ── Error messages ───────────────────────────────────────────── */
.login .error,
.login [class*="error"] {
    color: #C0392B !important;
    background-color: #FDF0EE !important;
    border: 1px solid rgba(192, 57, 43, 0.25) !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

/* ── Success states ───────────────────────────────────────────── */
.login .success,
.login [class*="success"] {
    color: #1E6B3C !important;
    background-color: #EEF7F2 !important;
    border: 1px solid rgba(30, 107, 60, 0.25) !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-size: 0.88rem !important;
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
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

# ------------------------------------------------------------------
# Wire everything together
# ------------------------------------------------------------------

registry = build_default_registry(
    migrate_pg_to_bq      = migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite = migrate_csv_to_sqlite,
    migrate_s3_to_sf      = migrate_s3_to_snowflake,
    migrate_mongo_to_s3   = migrate_mongo_to_s3,
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
    # ── Liberty Mutual Gradio theme ────────────────────────────────
    # gr.Blocks(css=...) only reaches the main app page.
    # The /login page is a separate Gradio route that only responds
    # to the theme object — so all login colours are set here.
    lm_theme = gr.themes.Default().set(
        # Page & container backgrounds
        body_background_fill="#F4F4F4",
        block_background_fill="#FFFFFF",
        panel_background_fill="#FFFFFF",
        # Primary button → Liberty Yellow
        button_primary_background_fill="#FFD000",
        button_primary_background_fill_hover="#E6BB00",
        button_primary_background_fill_dark="#FFD000",
        button_primary_text_color="#1A1446",
        button_primary_text_color_hover="#1A1446",
        button_primary_border_color="#FFD000",
        button_primary_border_color_hover="#E6BB00",
        # Secondary button → outlined Liberty Blue
        button_secondary_background_fill="#FFFFFF",
        button_secondary_background_fill_hover="#1A1446",
        button_secondary_text_color="#1A1446",
        button_secondary_text_color_hover="#FFFFFF",
        button_secondary_border_color="#1A1446",
        # Input fields
        input_background_fill="#FFFFFF",
        input_border_color="rgba(26,20,70,0.25)",
        input_border_color_focus="#1A1446",
        input_border_color_hover="rgba(26,20,70,0.5)",
        input_shadow_focus="0 0 0 3px rgba(26,20,70,0.13)",
        # Text
        body_text_color="#1A1446",
        block_title_text_color="#1A1446",
        block_label_text_color="#1A1446",
        link_text_color="#1A1446",
        link_text_color_hover="#002663",
        link_text_color_active="#002663",
        link_text_color_visited="#1A1446",
        # Borders & shadows
        block_border_color="rgba(26,20,70,0.15)",
        block_shadow="0 2px 8px rgba(26,20,70,0.08), 0 8px 32px rgba(26,20,70,0.10)",
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        inbrowser=True,
        auth=(settings.APP_USERNAME, settings.APP_PASSWORD),
        auth_message="migrate.ai — please log in to continue",
        theme=lm_theme,
    )