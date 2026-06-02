import datetime
import gradio as gr

# Load settings first (validates OPENAI_API_KEY)
import config.settings as settings

# ------------------------------------------------------------------
# CSS — minimal, cosmetic only, no structural overrides
# ------------------------------------------------------------------

CUSTOM_CSS = """

/* === GLOBAL RESET — minimal === */
body, html {
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

/* === GRADIO CONTAINER === */
.gradio-container {
  max-width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
  background: #F4F4F4 !important;
}

/* === REMOVE GRADIO FOOTER === */
footer { display: none !important; }

/* === CHATBOT BACKGROUND === */
.chatbot, .chatbot > * {
  background: #F4F4F4 !important;
}

/* === AI MESSAGE BUBBLE === */
.message.bot {
  background: #FFFFFF !important;
  color: #1A1446 !important;
  border: 0.5px solid rgba(26,20,70,0.15) !important;
  border-radius: 2px 12px 12px 12px !important;
  font-size: 13px !important;
}
.message.bot * { color: #1A1446 !important; }

/* === USER MESSAGE BUBBLE === */
.message.user,
[data-testid="user"],
.user {
  background: #1A1446 !important;
  color: #FFFFFF !important;
  border-radius: 12px 2px 12px 12px !important;
  font-size: 13px !important;
}
.message.user *,
.message.user p,
.message.user span,
.message.user div,
[data-testid="user"] *,
[data-testid="user"] p,
[data-testid="user"] span,
[data-testid="user"] .prose,
[data-testid="user"] .prose * {
  color: #FFFFFF !important;
  background: transparent !important;
}

/* === HIDE GRADIO ACTION BUTTONS === */
.copy-btn, .share-btn, .like-btn,
.dislike-btn, .retry-btn, .delete-btn,
[data-testid="copy-btn"],
.message-buttons,
div[class*="message-buttons"] {
  display: none !important;
}

/* === INPUT TEXTBOX === */
#msg-input textarea {
  background: #FFFFFF !important;
  border: 1px solid rgba(26,20,70,0.2) !important;
  border-radius: 10px !important;
  color: #1A1446 !important;
  font-size: 13px !important;
  padding: 10px 14px !important;
}

/* === SEND BUTTON === */
#send-btn button {
  background: #FFD000 !important;
  color: #1A1446 !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 700 !important;
  font-size: 16px !important;
}
#send-btn button:hover { background: #E6BB00 !important; }
#send-btn button span { color: #1A1446 !important; }

/* === SIDEBAR BUTTONS === */
#qs-btn-1 button, #qs-btn-2 button,
#qs-btn-3 button, #qs-btn-4 button {
  background: transparent !important;
  color: rgba(255,255,255,0.75) !important;
  border: none !important;
  border-radius: 8px !important;
  text-align: left !important;
  font-size: 13px !important;
  box-shadow: none !important;
  padding: 8px 12px !important;
  width: 100% !important;
}
#qs-btn-1 button span, #qs-btn-2 button span,
#qs-btn-3 button span, #qs-btn-4 button span {
  color: rgba(255,255,255,0.75) !important;
}
#qs-btn-1 button:hover, #qs-btn-2 button:hover,
#qs-btn-3 button:hover, #qs-btn-4 button:hover {
  background: rgba(255,255,255,0.1) !important;
  color: #FFFFFF !important;
}
#qs-btn-1 button {
  background: rgba(255,208,0,0.15) !important;
  color: #FFFFFF !important;
  border-left: 3px solid #FFD000 !important;
}
#qs-btn-1 button span { color: #FFFFFF !important; }

/* === NEW MIGRATION BUTTON === */
#new-migration-btn button {
  background: #FFD000 !important;
  color: #1A1446 !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  width: 100% !important;
  box-shadow: none !important;
}
#new-migration-btn button span { color: #1A1446 !important; }
#new-migration-btn button:hover { background: #E6BB00 !important; }

/* === SIDEBAR COLUMN BACKGROUND === */
#sidebar-col {
  background: #002663 !important;
  border-radius: 0 !important;
}
#sidebar-col > * {
  background: #002663 !important;
}

"""

# ------------------------------------------------------------------
# Fullscreen — JavaScript only, no CSS height/flex overrides
# ------------------------------------------------------------------

FULLSCREEN_JS = """
<script>
(function() {
  function makeFullscreen() {
    var styles = [
      'width:100vw;max-width:100vw;',
      'height:100vh;min-height:100vh;',
      'margin:0;padding:0;overflow:hidden;'
    ].join('');

    var selectors = [
      '.gradio-container',
      'gradio-app',
      'gradio-app > div',
      '#root',
      'body'
    ];

    selectors.forEach(function(sel) {
      var els = document.querySelectorAll(sel);
      els.forEach(function(el) {
        el.style.cssText += styles;
      });
    });

    var footers = document.querySelectorAll('footer, .footer');
    footers.forEach(function(f) { f.style.display = 'none'; });
  }

  makeFullscreen();
  document.addEventListener('DOMContentLoaded', makeFullscreen);
  setTimeout(makeFullscreen, 500);
  setTimeout(makeFullscreen, 1000);
  setTimeout(makeFullscreen, 2000);
  window.addEventListener('resize', makeFullscreen);
})();
</script>
"""

# ------------------------------------------------------------------
# HTML sections
# ------------------------------------------------------------------

HERO_HTML = """
<div style="
  background:#1A1446;
  width:100%;
  padding:16px 28px 0 28px;
  box-sizing:border-box;
  font-family:system-ui,-apple-system,sans-serif;
">
  <!-- Top row: logo + status -->
  <div style="display:flex;align-items:center;
    justify-content:space-between;margin-bottom:12px;">

    <!-- Logo + wordmark -->
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:42px;height:42px;background:#FFD000;
        border-radius:11px;display:flex;align-items:center;
        justify-content:center;flex-shrink:0;">
        <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
          <rect x="2" y="5" width="8" height="8" rx="2"
            fill="#1A1446"/>
          <rect x="2" y="16" width="8" height="3" rx="1.5"
            fill="rgba(26,20,70,0.3)"/>
          <rect x="16" y="10" width="8" height="8" rx="2"
            fill="#1A1446" opacity="0.8"/>
          <rect x="16" y="21" width="8" height="3" rx="1.5"
            fill="rgba(26,20,70,0.2)"/>
          <path d="M10 9 L13 9 L13 14 L16 14"
            stroke="#1A1446" stroke-width="1.8"
            fill="none" stroke-linecap="round"
            stroke-linejoin="round"/>
          <path d="M14 12 L16 14 L14 16"
            stroke="#1A1446" stroke-width="1.8"
            fill="none" stroke-linecap="round"
            stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <div style="font-size:20px;font-weight:500;
          color:#FFFFFF;line-height:1.2;letter-spacing:-0.3px;">
          Migrate<span style="color:#FFD000;">AI</span>
        </div>
        <div style="font-size:11px;color:rgba(255,255,255,0.45);
          margin-top:2px;">
          Intelligent data migration &middot; powered by GPT-4o
        </div>
      </div>
    </div>

    <!-- Status pill -->
    <div style="display:flex;align-items:center;gap:6px;
      padding:5px 12px;background:rgba(255,255,255,0.08);
      border:0.5px solid rgba(255,255,255,0.15);
      border-radius:20px;font-size:12px;
      color:rgba(255,255,255,0.85);">
      <span style="width:7px;height:7px;border-radius:50%;
        background:#4ADE80;display:inline-block;"></span>
      GPT-4o connected
    </div>
  </div>

  <!-- Description -->
  <div style="margin-bottom:14px;">
    <div style="font-size:14px;font-weight:500;color:#FFFFFF;
      margin-bottom:4px;">
      Move your data
      <span style="color:#FFD000;">anywhere</span>,
      in minutes &mdash; just by having a conversation.
    </div>
    <div style="font-size:12px;color:rgba(255,255,255,0.5);
      line-height:1.6;max-width:700px;">
      No pipelines to build. No scripts to write.
      No engineers needed. Tell MigrateAI your source
      and destination, answer a few questions, and it
      handles the rest &mdash; schema mapping, validation,
      and delivery included.
    </div>
  </div>

  <!-- Capability pills -->
  <div style="display:flex;flex-wrap:wrap;gap:6px;
    margin-bottom:14px;">
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#9889; <strong style="color:#fff;">One-time full loads</strong>
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128737; <strong style="color:#fff;">Pre &amp; post validation</strong>
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128172; <strong style="color:#fff;">Chat-driven config</strong>
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128268; <strong style="color:#fff;">4 sources</strong>
      &mdash; Postgres &middot; CSV &middot; S3 &middot; Mongo
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128452; <strong style="color:#fff;">4 destinations</strong>
      &mdash; BigQuery &middot; SQLite &middot; S3 &middot; Snowflake
    </span>
  </div>

  <!-- Tab bar -->
  <div style="display:flex;border-top:0.5px solid
    rgba(255,255,255,0.12);margin:0 -28px;">
    <span style="padding:10px 20px;font-size:13px;
      color:#FFFFFF;border-bottom:2px solid #FFD000;
      cursor:pointer;">Chat</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">History</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">Output files</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">Settings</span>
  </div>
</div>
"""

SIDEBAR_TOP_HTML = """
<div style="
  padding:14px 10px 6px;
  font-family:system-ui,-apple-system,sans-serif;
">
  <div style="font-size:10px;font-weight:500;
    color:rgba(255,255,255,0.35);letter-spacing:0.08em;
    text-transform:uppercase;padding:0 8px;margin-bottom:6px;">
    Quick Start
  </div>
</div>
"""

# ------------------------------------------------------------------
# Agent wiring
# ------------------------------------------------------------------

from llm.agent import MigrationAgent
from llm.tool_registry import build_default_registry
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

registry = build_default_registry(
    migrate_pg_to_bq      = migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite = migrate_csv_to_sqlite,
    migrate_s3_to_sf      = migrate_s3_to_snowflake,
    migrate_mongo_to_s3   = migrate_mongo_to_s3,
)

agent = MigrationAgent(registry=registry)

WELCOME_MESSAGE = (
    "👋 Hey! I'm **MigrateAI** — your intelligent data migration assistant.\n\n"
    "I can help you move data between systems in minutes, "
    "just by having a conversation. No scripts, no pipelines, no engineers needed.\n\n"
    "**To get started, either:**\n"
    "- Click a **Quick Start** path in the sidebar →\n"
    "- Or tell me what you want to migrate in your own words\n\n"
    "**Supported sources:** Postgres · CSV · S3 · MongoDB\n"
    "**Supported destinations:** BigQuery · SQLite · S3 · Snowflake"
)

# ------------------------------------------------------------------
# Last migration tracker
# ------------------------------------------------------------------

last_migration_store = {"entries": []}


def update_last_migration(source: str, dest: str, rows: int = None) -> None:
    entry = {
        "label": f"{source} → {dest}",
        "detail": f"{rows} rows" if rows else "done",
        "time": datetime.datetime.now().strftime("%H:%M"),
    }
    last_migration_store["entries"].insert(0, entry)
    last_migration_store["entries"] = last_migration_store["entries"][:3]


def get_sidebar_bottom_html() -> str:
    entries = last_migration_store.get("entries", [])

    if not entries:
        badges = """
        <div style="font-size:11px;color:rgba(255,255,255,0.3);
          padding:4px 8px;font-style:italic;">
          No migrations yet
        </div>
        """
    else:
        badges = ""
        for e in entries:
            badges += f"""
            <div style="display:flex;align-items:center;
              justify-content:space-between;padding:5px 8px;
              background:rgba(255,255,255,0.05);
              border-radius:6px;margin-bottom:3px;
              font-size:11px;color:rgba(255,255,255,0.6);">
              <span>
                <span style="width:5px;height:5px;
                  border-radius:50%;background:#FFD000;
                  display:inline-block;margin-right:5px;">
                </span>
                {e['label']}
              </span>
              <span>{e['detail']}</span>
            </div>
            """

    return f"""
    <div style="
      padding:12px 10px;
      margin-top:12px;
      border-top:0.5px solid rgba(255,255,255,0.1);
      font-family:system-ui,-apple-system,sans-serif;
    ">
      <div style="font-size:10px;font-weight:500;
        color:rgba(255,255,255,0.35);letter-spacing:0.08em;
        text-transform:uppercase;margin-bottom:8px;">
        Last Migration
      </div>
      {badges}
    </div>
    """


_COMPLETION_WORDS = {"rows", "migrated", "complete", "success", "transferred"}
_MIGRATION_PAIRS = [
    (("postgres",), ("bigquery",), "Postgres", "BigQuery"),
    (("csv",),      ("sqlite",),   "CSV",      "SQLite"),
    (("s3",),       ("snowflake",),"S3",       "Snowflake"),
    (("mongo",),    ("s3",),       "Mongo",    "S3"),
]


def _detect_and_record_migration(text: str) -> None:
    lower = text.lower()
    if not any(w in lower for w in _COMPLETION_WORDS):
        return
    for src_keys, dst_keys, src_label, dst_label in _MIGRATION_PAIRS:
        if any(k in lower for k in src_keys) and any(k in lower for k in dst_keys):
            update_last_migration(src_label, dst_label)
            return


# ------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------

def respond(user_message: str, history: list[dict]) -> tuple:
    if not user_message.strip():
        return history, "", get_sidebar_bottom_html()
    reply = agent.chat(user_message)
    history.append({"role": "user",      "content": user_message})
    history.append({"role": "assistant", "content": reply})
    _detect_and_record_migration(reply)
    return history, "", get_sidebar_bottom_html()


def run_quick_start(prompt: str, history: list[dict]) -> tuple:
    reply = agent.chat(prompt)
    history = history + [
        {"role": "user",      "content": prompt},
        {"role": "assistant", "content": reply},
    ]
    _detect_and_record_migration(reply)
    _detect_and_record_migration(prompt)
    return history, "", get_sidebar_bottom_html()


def reset_session() -> tuple:
    agent.reset()
    last_migration_store["entries"] = []
    return [{"role": "assistant", "content": WELCOME_MESSAGE}], "", get_sidebar_bottom_html()


# ------------------------------------------------------------------
# UI
# ------------------------------------------------------------------

with gr.Blocks(title="MigrateAI") as demo:

    gr.HTML(FULLSCREEN_JS)

    gr.HTML(HERO_HTML)

    with gr.Row(equal_height=True):

        with gr.Column(scale=0, min_width=240, elem_id="sidebar-col"):
            gr.HTML(SIDEBAR_TOP_HTML)
            btn_pg_bq  = gr.Button(
                "🗄  Postgres → BigQuery",
                elem_id="qs-btn-1",
                variant="secondary",
                size="sm",
            )
            btn_csv_sl = gr.Button(
                "📄  CSV → SQLite",
                elem_id="qs-btn-2",
                variant="secondary",
                size="sm",
            )
            btn_s3_sf  = gr.Button(
                "☁️   S3 → Snowflake",
                elem_id="qs-btn-3",
                variant="secondary",
                size="sm",
            )
            btn_mg_s3  = gr.Button(
                "🍃  Mongo → S3",
                elem_id="qs-btn-4",
                variant="secondary",
                size="sm",
            )
            sidebar_bottom = gr.HTML(
                value=get_sidebar_bottom_html(),
                elem_id="sidebar-bottom",
            )
            reset_btn = gr.Button(
                "+ New Migration",
                elem_id="new-migration-btn",
                variant="primary",
                size="sm",
            )

        with gr.Column(scale=1, elem_id="chat-col"):
            chatbot = gr.Chatbot(
                value=[{"role": "assistant", "content": WELCOME_MESSAGE}],
                label="",
                height=500,
                show_label=False,
                elem_id="chatbot",
            )
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Type your reply…",
                    show_label=False,
                    lines=1,
                    scale=9,
                    container=False,
                    elem_id="msg-input",
                )
                send_btn = gr.Button(
                    "↑",
                    variant="primary",
                    scale=0,
                    min_width=48,
                    elem_id="send-btn",
                )

    # Event bindings
    send_btn.click(
        fn=respond,
        inputs=[msg_input, chatbot],
        outputs=[chatbot, msg_input, sidebar_bottom],
    )
    msg_input.submit(
        fn=respond,
        inputs=[msg_input, chatbot],
        outputs=[chatbot, msg_input, sidebar_bottom],
    )

    btn_pg_bq.click(
        fn=lambda h: run_quick_start(
            "I want to migrate data from Postgres to BigQuery", h
        ),
        inputs=[chatbot],
        outputs=[chatbot, msg_input, sidebar_bottom],
    )
    btn_csv_sl.click(
        fn=lambda h: run_quick_start(
            "I need to load a CSV file into SQLite", h
        ),
        inputs=[chatbot],
        outputs=[chatbot, msg_input, sidebar_bottom],
    )
    btn_s3_sf.click(
        fn=lambda h: run_quick_start(
            "I want to migrate data from S3 to Snowflake", h
        ),
        inputs=[chatbot],
        outputs=[chatbot, msg_input, sidebar_bottom],
    )
    btn_mg_s3.click(
        fn=lambda h: run_quick_start(
            "I want to export a MongoDB collection to S3", h
        ),
        inputs=[chatbot],
        outputs=[chatbot, msg_input, sidebar_bottom],
    )
    reset_btn.click(
        fn=reset_session,
        outputs=[chatbot, msg_input, sidebar_bottom],
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        auth=(settings.APP_USERNAME, settings.APP_PASSWORD),
        auth_message="migrate.ai — please log in to continue",
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS,
    )
