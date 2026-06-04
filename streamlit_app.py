# ── SECTION 1 — Page config (FIRST CALL, before any other st call) ───────────
import streamlit as st
import datetime

st.set_page_config(
    page_title="MigrateAI",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── SECTION 2 — Backend imports ───────────────────────────────────────────────
import config.settings as settings  # noqa: F401
from llm.agent import MigrationAgent
from llm.tool_registry import build_default_registry
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

# ── SECTION 3 — CSS ───────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>

/* ── HIDE CHROME ── */
#MainMenu, header[data-testid="stHeader"], footer,
.stDeployButton, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {
  display: none !important;
}

/* ── FULLSCREEN ── */
html, body {
  margin: 0 !important; padding: 0 !important;
  width: 100vw !important; height: 100vh !important;
  overflow: hidden !important;
}

.stApp, [data-testid="stAppViewContainer"] {
  width: 100vw !important; height: 100vh !important;
  max-width: 100vw !important;
  overflow: hidden !important;
  background: #1A1446 !important;
  padding: 0 !important; margin: 0 !important;
}

/* Remove Streamlit centered container */
.main .block-container,
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"] {
  max-width: 100vw !important;
  width: 100vw !important;
  padding: 0 !important;
  margin: 0 !important;
  background: #1A1446 !important;
}

section.main, [data-testid="stMain"] {
  background: #1A1446 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

/* ── HIDE NATIVE SIDEBAR (we use columns instead) ── */
[data-testid="stSidebar"] {
  display: none !important;
  width: 0 !important;
  visibility: hidden !important;
}

/* ── LEFT COLUMN (our fake sidebar) ── */
[data-testid="stHorizontalBlock"] > div:first-child {
  background: #002663 !important;
  height: calc(100vh - 260px) !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  padding: 0 !important;
  padding-bottom: 0 !important;
  border-right: 1px solid rgba(255,255,255,0.08) !important;
}

/* New Migration button container — push to bottom of left column */
[data-testid="stHorizontalBlock"] > div:first-child
  > div:last-child {
  margin-top: auto !important;
  padding: 12px 8px !important;
}

[data-testid="stHorizontalBlock"] > div:first-child * {
  color: rgba(255,255,255,0.75) !important;
}

/* Left column buttons — Quick Start */
[data-testid="stHorizontalBlock"] > div:first-child
  .stButton > button {
  background: transparent !important;
  color: rgba(255,255,255,0.75) !important;
  border: none !important;
  border-radius: 8px !important;
  text-align: left !important;
  width: 100% !important;
  font-size: 13px !important;
  padding: 8px 12px !important;
  box-shadow: none !important;
  margin-bottom: 2px !important;
  justify-content: flex-start !important;
}

[data-testid="stHorizontalBlock"] > div:first-child
  .stButton > button p {
  color: rgba(255,255,255,0.75) !important;
  font-size: 13px !important;
}

[data-testid="stHorizontalBlock"] > div:first-child
  .stButton > button:hover {
  background: rgba(255,255,255,0.1) !important;
}

[data-testid="stHorizontalBlock"] > div:first-child
  .stButton > button:hover p {
  color: #FFFFFF !important;
}

/* New Migration button in left column */
[data-testid="stHorizontalBlock"] > div:first-child
  button[kind="primary"] {
  background: #FFD000 !important;
  color: #1A1446 !important;
  font-weight: 600 !important;
  width: calc(100% - 16px) !important;
  margin: 4px 8px !important;
  border-radius: 8px !important;
  border: none !important;
  box-shadow: none !important;
}

[data-testid="stHorizontalBlock"] > div:first-child
  button[kind="primary"] p {
  color: #1A1446 !important;
  font-weight: 600 !important;
}

/* ── RIGHT COLUMN (chat area) ── */
[data-testid="stHorizontalBlock"] > div:last-child {
  background: #F4F4F4 !important;
  height: calc(100vh - 260px) !important;
  padding: 0 !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  position: relative !important;
}

/* Chat message container — fills column, scrollable */
[data-testid="stHorizontalBlock"] > div:last-child
  [data-testid="stChatMessageContainer"] {
  flex: 1 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding: 16px 20px 80px 20px !important;
  background: #F4F4F4 !important;
}

/* Chat input container — fixed to bottom, left set by JS */
[data-testid="stHorizontalBlock"] > div:last-child
  .stChatFloatingInputContainer,
.stChatFloatingInputContainer {
  position: fixed !important;
  bottom: 0 !important;
  right: 0 !important;
  background: #FFFFFF !important;
  border-top: 0.5px solid rgba(26,20,70,0.13) !important;
  padding: 12px 20px !important;
  z-index: 999 !important;
}

/* ── CHAT BUBBLES ── */
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarUser"] {
  display: none !important;
}

[data-testid="stChatMessage"] button,
[data-testid="stCopyButton"] {
  display: none !important;
}

[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarAssistant"]
) {
  background: #FFFFFF !important;
  border: 0.5px solid rgba(26,20,70,0.13) !important;
  border-radius: 2px 12px 12px 12px !important;
  padding: 10px 14px !important;
  max-width: 80% !important;
  margin-bottom: 10px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}

[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarAssistant"]
) * {
  color: #1A1446 !important;
  font-size: 13px !important;
}

[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarUser"]
) {
  background: #1A1446 !important;
  border-radius: 12px 2px 12px 12px !important;
  padding: 10px 14px !important;
  max-width: 80% !important;
  margin-left: auto !important;
  margin-bottom: 10px !important;
}

[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarUser"]
) * {
  color: #FFFFFF !important;
  font-size: 13px !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
  background: #FFFFFF !important;
  border: 1px solid rgba(26,20,70,0.2) !important;
  border-radius: 10px !important;
}

[data-testid="stChatInput"] textarea {
  background: #FFFFFF !important;
  color: #1A1446 !important;
  font-size: 13px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
  color: rgba(26,20,70,0.35) !important;
}

[data-testid="stChatInput"] button {
  background: #FFD000 !important;
  border-radius: 8px !important;
  border: none !important;
}

[data-testid="stChatInput"] button svg {
  fill: #1A1446 !important;
}

/* ── CHAT CONTAINER BACKGROUND (fallback) ── */
[data-testid="stChatMessageContainer"] {
  background: #F4F4F4 !important;
}

/* ── COLUMNS GAP REMOVAL ── */
[data-testid="stHorizontalBlock"] {
  gap: 0 !important;
  padding: 0 !important;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── SECTION 4 — Constants ─────────────────────────────────────────────────────

WELCOME_MESSAGE = (
    "👋 Hey! I'm **MigrateAI** — your intelligent data "
    "migration assistant.\n\n"
    "I can help you move data between systems in minutes, just by "
    "having a conversation. No scripts, no pipelines, no engineers "
    "needed.\n\n"
    "**To get started, either:**\n"
    "- Click a **Quick Start** path in the sidebar\n"
    "- Or tell me what you want to migrate in your own words\n\n"
    "**Supported sources:** Postgres · CSV · S3 · MongoDB\n"
    "**Supported destinations:** BigQuery · SQLite · S3 · Snowflake"
)

_COMPLETION_WORDS = {"rows", "migrated", "complete", "success", "transferred"}
_MIGRATION_PAIRS = [
    (("postgres",), ("bigquery",),  "Postgres", "BigQuery"),
    (("csv",),      ("sqlite",),    "CSV",      "SQLite"),
    (("s3",),       ("snowflake",), "S3",       "Snowflake"),
    (("mongo",),    ("s3",),        "Mongo",    "S3"),
]

# ── SECTION 5 — HERO_HTML string (inline styles only) ────────────────────────
# Uses string concatenation so no line starts with 4+ spaces,
# which would cause Streamlit's Markdown parser to treat it as a code block.

_LOGO_SVG = (
'<svg viewBox="0 0 26 26" width="26" height="26" xmlns="http://www.w3.org/2000/svg">'
'<rect x="2" y="5" width="8" height="8" rx="2" fill="#1A1446"/>'
'<rect x="2" y="16" width="8" height="3" rx="1.5" fill="rgba(26,20,70,0.3)"/>'
'<rect x="16" y="10" width="8" height="8" rx="2" fill="#1A1446" opacity="0.8"/>'
'<rect x="16" y="21" width="8" height="3" rx="1.5" fill="rgba(26,20,70,0.2)"/>'
'<path d="M10 9L13 9L13 14L16 14" stroke="#1A1446" stroke-width="1.8"'
' fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
'<path d="M14 12L16 14L14 16" stroke="#1A1446" stroke-width="1.8"'
' fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
'</svg>'
)

_PILL = (
'<span style="display:inline-flex;align-items:center;gap:6px;padding:5px 11px;'
'background:rgba(255,255,255,0.07);border:0.5px solid rgba(255,255,255,0.13);'
'border-radius:7px;font-size:12px;color:rgba(255,255,255,0.8);">'
)

HERO_HTML = (
# outer wrapper — inline styles provide background; no CSS id needed
'<div style="width:100%;background:#1A1446;box-sizing:border-box;'
'padding:16px 28px 0;font-family:system-ui,-apple-system,sans-serif;">'

# ── ROW 1: logo + wordmark LEFT | status pill RIGHT ──────────────────────────
'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1vh;">'
# logo box
'<div style="display:flex;align-items:center;gap:12px;">'
'<div style="width:42px;height:42px;background:#FFD000;border-radius:11px;'
'display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
+ _LOGO_SVG +
'</div>'
# wordmark
'<div>'
'<div style="font-size:20px;font-weight:500;letter-spacing:-0.3px;line-height:1.2;">'
'<span style="color:#fff;">Migrate</span><span style="color:#FFD000;">AI</span>'
'</div>'
'<div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:1px;">'
'Intelligent data migration &middot; powered by GPT-4o'
'</div>'
'</div>'
'</div>'
# status pill
'<div style="display:flex;align-items:center;gap:6px;padding:5px 12px;'
'background:rgba(255,255,255,0.08);border:0.5px solid rgba(255,255,255,0.15);'
'border-radius:20px;font-size:12px;color:rgba(255,255,255,0.85);">'
'<span style="width:7px;height:7px;background:#4ADE80;border-radius:50%;'
'display:inline-block;flex-shrink:0;"></span>'
'GPT-4o connected'
'</div>'
'</div>'

# ── ROW 2: headline + body ────────────────────────────────────────────────────
'<div style="margin-bottom:1.2vh;">'
'<div style="font-size:14px;font-weight:500;color:#fff;margin-bottom:4px;">'
'Move your data <span style="color:#FFD000;">anywhere</span>, in minutes &mdash; '
'just by having a conversation.'
'</div>'
'<div style="font-size:12px;color:rgba(255,255,255,0.5);max-width:700px;line-height:1.5;">'
'No pipelines to build. No scripts to write. No engineers needed. '
'Tell MigrateAI your source and destination, answer a few questions, '
'and it handles the rest &mdash; schema mapping, validation, and delivery included.'
'</div>'
'</div>'

# ── ROW 3: capability pills ───────────────────────────────────────────────────
'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1.2vh;">'
+ _PILL + '&#9889; <strong style="color:#fff;">One-time full loads</strong></span>'
+ _PILL + '&#128737; <strong style="color:#fff;">Pre &amp; post validation</strong></span>'
+ _PILL + '&#128172; <strong style="color:#fff;">Chat-driven config</strong></span>'
+ _PILL + '&#128268; <strong style="color:#fff;">4 sources</strong> &mdash; Postgres &middot; CSV &middot; S3 &middot; Mongo</span>'
+ _PILL + '&#128451; <strong style="color:#fff;">4 destinations</strong> &mdash; BigQuery &middot; SQLite &middot; S3 &middot; Snowflake</span>'
+ '</div>'

# ── ROW 4: tab bar (bleeds full width via negative margin) ────────────────────
'<div style="display:flex;border-top:0.5px solid rgba(255,255,255,0.12);margin:0 -28px;">'
'<span style="padding:10px 20px;font-size:13px;color:#fff;border-bottom:2px solid #FFD000;cursor:default;">Chat</span>'
'<span style="padding:10px 20px;font-size:13px;color:rgba(255,255,255,0.4);cursor:default;">History</span>'
'<span style="padding:10px 20px;font-size:13px;color:rgba(255,255,255,0.4);cursor:default;">Output files</span>'
'<span style="padding:10px 20px;font-size:13px;color:rgba(255,255,255,0.4);cursor:default;">Settings</span>'
'</div>'

'</div>'
)

# ── SECTION 6 — Session state init ───────────────────────────────────────────

if "agent" not in st.session_state:
    registry = build_default_registry(
        migrate_pg_to_bq      = migrate_postgres_to_bigquery,
        migrate_csv_to_sqlite = migrate_csv_to_sqlite,
        migrate_s3_to_sf      = migrate_s3_to_snowflake,
        migrate_mongo_to_s3   = migrate_mongo_to_s3,
    )
    st.session_state.agent = MigrationAgent(registry=registry)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]
if "last_migrations" not in st.session_state:
    st.session_state.last_migrations = []

# ── SECTION 7 — Helpers ───────────────────────────────────────────────────────

def detect_and_record(text: str) -> None:
    low = text.lower()
    if not any(w in low for w in _COMPLETION_WORDS):
        return
    for src_keys, dst_keys, src_label, dst_label in _MIGRATION_PAIRS:
        if any(k in low for k in src_keys) and any(k in low for k in dst_keys):
            entry = {
                "label":  f"{src_label} → {dst_label}",
                "detail": "done",
                "time":   datetime.datetime.now().strftime("%H:%M"),
            }
            st.session_state.last_migrations.insert(0, entry)
            st.session_state.last_migrations = st.session_state.last_migrations[:3]
            return


def send_message(prompt: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    reply = st.session_state.agent.chat(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    detect_and_record(reply)
    detect_and_record(prompt)


def build_last_migration_html() -> str:
    label_style = (
        "font-size:10px;font-weight:500;color:rgba(255,255,255,0.35);"
        "text-transform:uppercase;letter-spacing:0.08em;"
        "display:block;margin-bottom:6px;"
    )
    html = f'<span style="{label_style}">Last Migration</span>'
    if not st.session_state.last_migrations:
        html += (
            '<span style="font-size:11px;font-style:italic;'
            'color:rgba(255,255,255,0.35);">No migrations yet</span>'
        )
        return html
    for m in st.session_state.last_migrations:
        html += (
            '<div style="background:rgba(255,255,255,0.05);border-radius:6px;'
            'padding:5px 8px;font-size:11px;display:flex;'
            'justify-content:space-between;align-items:center;margin-bottom:4px;">'
            '<span style="display:flex;align-items:center;gap:5px;'
            'color:rgba(255,255,255,0.8);">'
            '<span style="width:5px;height:5px;background:#FFD000;'
            'border-radius:50%;display:inline-block;flex-shrink:0;"></span>'
            f'{m["label"]}</span>'
            f'<span style="color:rgba(255,255,255,0.4);">{m["detail"]}</span>'
            '</div>'
        )
    return html

# ── SECTION 8 — Hero (full width, above columns) ─────────────────────────────

st.markdown(HERO_HTML, unsafe_allow_html=True)

# ── SECTION 9 — Two-column layout (sidebar + chat) ───────────────────────────

col_sidebar, col_chat = st.columns([1, 4], gap="small")

# ── Left column — sidebar replacement ────────────────────────────────────────

with col_sidebar:
    st.markdown("""
    <div style="
      padding: 14px 4px 6px;
      font-family: system-ui,-apple-system,sans-serif;
    ">
      <div style="
        font-size: 10px; font-weight: 500;
        color: rgba(255,255,255,0.35);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0 8px; margin-bottom: 6px;
      ">Quick Start</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗄  Postgres → BigQuery",
                 key="qs1", use_container_width=True):
        send_message("I want to migrate data from Postgres to BigQuery")
        st.rerun()

    if st.button("📄  CSV → SQLite",
                 key="qs2", use_container_width=True):
        send_message("I need to load a CSV file into SQLite")
        st.rerun()

    if st.button("☁️  S3 → Snowflake",
                 key="qs3", use_container_width=True):
        send_message("I want to migrate data from S3 to Snowflake")
        st.rerun()

    if st.button("🍃  Mongo → S3",
                 key="qs4", use_container_width=True):
        send_message("I want to export a MongoDB collection to S3")
        st.rerun()

    st.markdown("""
    <hr style="border:none;
      border-top:0.5px solid rgba(255,255,255,0.1);
      margin:12px 0;">
    """, unsafe_allow_html=True)

    st.markdown(build_last_migration_html(), unsafe_allow_html=True)

    st.markdown(
        "<div style='flex:1; min-height:20px;'></div>",
        unsafe_allow_html=True,
    )

    if st.button("＋ New Migration", key="reset",
                 use_container_width=True, type="primary"):
        st.session_state.agent.reset()
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]
        st.session_state.last_migrations = []
        st.rerun()

# ── Right column — chat area ──────────────────────────────────────────────────

with col_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your reply…"):
        send_message(prompt)
        st.rerun()

# ── SECTION 10 — JS: pin input bar + sync sidebar bottom ─────────────────────

st.markdown("""
<script>
(function() {
  function fixLayout() {
    var blocks = document.querySelectorAll(
      '[data-testid="stHorizontalBlock"]'
    );
    if (!blocks.length) return;
    var block = blocks[blocks.length - 1];
    var cols = Array.from(block.children);
    if (cols.length < 2) return;

    var leftCol  = cols[0];
    var rightCol = cols[cols.length - 1];
    var rightRect = rightCol.getBoundingClientRect();
    var leftPos   = Math.round(rightRect.left);

    // Pin chat input bar to start of right column
    var inputs = document.querySelectorAll(
      '.stChatFloatingInputContainer'
    );
    inputs.forEach(function(el) {
      el.style.setProperty('left',     leftPos + 'px', 'important');
      el.style.setProperty('right',    '0',            'important');
      el.style.setProperty('bottom',   '0',            'important');
      el.style.setProperty('position', 'fixed',        'important');
    });

    // Sync left column bottom padding with input bar height
    var inputBar = document.querySelector(
      '.stChatFloatingInputContainer'
    );
    if (inputBar && leftCol) {
      var h = inputBar.offsetHeight || 70;
      leftCol.style.paddingBottom = h + 'px';
    }
  }

  // Run multiple times to catch Streamlit's async renders
  [300, 600, 1000, 2000].forEach(function(t) {
    setTimeout(fixLayout, t);
  });
  window.addEventListener('resize', fixLayout);
})();
</script>
""", unsafe_allow_html=True)
