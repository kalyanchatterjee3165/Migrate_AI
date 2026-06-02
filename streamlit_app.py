import streamlit as st
import datetime


def _html(raw: str) -> str:
    """Strip per-line leading whitespace so Markdown never treats indented lines as code blocks."""
    return "\n".join(line.lstrip() for line in raw.splitlines())

st.set_page_config(
    page_title="MigrateAI",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# All other imports AFTER set_page_config
import config.settings as settings  # noqa: E402
from llm.agent import MigrationAgent  # noqa: E402
from llm.tool_registry import build_default_registry  # noqa: E402
from migrations.executor import (  # noqa: E402
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

# ── SECTION B — CSS (all in one block) ────────────────────────────
CUSTOM_CSS = """
<style>

/* ── 1. HIDE ALL STREAMLIT CHROME ── */
#MainMenu,
header[data-testid="stHeader"],
footer,
.stDeployButton,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
  display: none !important;
  height: 0 !important;
  visibility: hidden !important;
}

/* ── 2. TRUE FULLSCREEN ── */
html, body {
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
  width: 100vw !important;
  height: 100vh !important;
}

.stApp {
  background: #F4F4F4 !important;
  overflow: hidden !important;
}

[data-testid="stAppViewContainer"] {
  background: #F4F4F4 !important;
  padding: 0 !important;
  overflow: hidden !important;
  height: 100vh !important;
}

/* Remove Streamlit centered container max-width */
[data-testid="stAppViewBlockContainer"],
.main .block-container,
div[class*="block-container"] {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* ── 3. SIDEBAR ── */
[data-testid="stSidebar"] {
  background: #002663 !important;
  min-width: 240px !important;
  max-width: 240px !important;
  width: 240px !important;
  padding: 0 !important;
}

[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebarContent"] {
  background: #002663 !important;
  padding: 0 8px !important;
}

/* All sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
  color: rgba(255,255,255,0.75) !important;
}

/* Sidebar quick start buttons */
[data-testid="stSidebar"] .stButton > button {
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
  display: flex !important;
  justify-content: flex-start !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.1) !important;
  color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stButton > button p {
  color: rgba(255,255,255,0.75) !important;
  font-size: 13px !important;
}

[data-testid="stSidebar"] .stButton > button:hover p {
  color: #FFFFFF !important;
}

/* New Migration button — must be targeted by key */
[data-testid="stSidebar"] [data-testid="baseButton-secondary"]:last-of-type,
#reset_btn > button,
button[kind="secondary"][data-testid*="reset"] {
  background: #FFD000 !important;
  color: #1A1446 !important;
  font-weight: 600 !important;
}

/* ── 4. CHAT MESSAGES ── */

/* Container background */
[data-testid="stChatMessageContainer"] {
  background: #F4F4F4 !important;
  padding: 16px !important;
}

/* AI message bubble */
[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarAssistant"]
) {
  background: #FFFFFF !important;
  border: 0.5px solid rgba(26,20,70,0.13) !important;
  border-radius: 2px 12px 12px 12px !important;
  padding: 10px 14px !important;
  max-width: 80% !important;
  align-self: flex-start !important;
  margin-bottom: 10px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}

[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarAssistant"]
) p,
[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarAssistant"]
) li,
[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarAssistant"]
) * {
  color: #1A1446 !important;
  font-size: 13px !important;
}

/* User message bubble */
[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarUser"]
) {
  background: #1A1446 !important;
  border-radius: 12px 2px 12px 12px !important;
  padding: 10px 14px !important;
  max-width: 80% !important;
  align-self: flex-end !important;
  margin-left: auto !important;
  margin-bottom: 10px !important;
}

[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarUser"]
) p,
[data-testid="stChatMessage"]:has(
  [data-testid="stChatMessageAvatarUser"]
) * {
  color: #FFFFFF !important;
  font-size: 13px !important;
}

/* Hide avatars — we don't need them */
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarUser"] {
  display: none !important;
}

/* Hide copy/action buttons on messages */
[data-testid="stChatMessage"] button,
[data-testid="stCopyButton"],
.stChatMessage button {
  display: none !important;
}

/* ── 5. CHAT INPUT ── */
[data-testid="stChatInput"] {
  border: 1px solid rgba(26,20,70,0.2) !important;
  border-radius: 10px !important;
  background: #FFFFFF !important;
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
  color: #1A1446 !important;
  border-radius: 8px !important;
  border: none !important;
}

[data-testid="stChatInput"] button svg {
  fill: #1A1446 !important;
}

/* Chat input container — pin to bottom */
.stChatFloatingInputContainer {
  background: #FFFFFF !important;
  border-top: 0.5px solid rgba(26,20,70,0.13) !important;
  padding: 10px 16px !important;
  bottom: 0 !important;
  left: 240px !important;
  right: 0 !important;
  position: fixed !important;
  z-index: 999 !important;
}

/* Add padding to bottom of chat so last message
   not hidden behind fixed input bar */
[data-testid="stChatMessageContainer"] {
  padding-bottom: 80px !important;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── SECTION C — Constants ──────────────────────────────────────────
WELCOME_MESSAGE = (
    "👋 Hey! I'm **MigrateAI** — your intelligent "
    "data migration assistant.\n\n"
    "I can help you move data between systems in minutes, "
    "just by having a conversation. "
    "No scripts, no pipelines, no engineers needed.\n\n"
    "**To get started, either:**\n"
    "- Click a **Quick Start** path in the sidebar\n"
    "- Or tell me what you want to migrate\n\n"
    "**Supported sources:** Postgres · CSV · S3 · MongoDB\n"
    "**Supported destinations:** "
    "BigQuery · SQLite · S3 · Snowflake"
)

_COMPLETION_WORDS = {
    "rows", "migrated", "complete",
    "success", "transferred"
}

_MIGRATION_PAIRS = [
    (("postgres",), ("bigquery",),  "Postgres", "BigQuery"),
    (("csv",),      ("sqlite",),    "CSV",      "SQLite"),
    (("s3",),       ("snowflake",), "S3",       "Snowflake"),
    (("mongo",),    ("s3",),        "Mongo",    "S3"),
]

# ── SECTION D — Hero HTML ──────────────────────────────────────────
HERO_HTML = """
<div style="background:#1A1446;width:100%;
  padding:16px 28px 0;box-sizing:border-box;
  font-family:system-ui,-apple-system,sans-serif;
  margin:0;">

  <!-- Row 1: Logo + Status -->
  <div style="display:flex;align-items:center;
    justify-content:space-between;margin-bottom:12px;">

    <!-- Logo mark + wordmark -->
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:42px;height:42px;
        background:#FFD000;border-radius:11px;
        display:flex;align-items:center;
        justify-content:center;flex-shrink:0;">
        <svg width="26" height="26"
          viewBox="0 0 26 26" fill="none">
          <rect x="2" y="5" width="8" height="8"
            rx="2" fill="#1A1446"/>
          <rect x="2" y="16" width="8" height="3"
            rx="1.5" fill="rgba(26,20,70,0.3)"/>
          <rect x="16" y="10" width="8" height="8"
            rx="2" fill="#1A1446" opacity="0.8"/>
          <rect x="16" y="21" width="8" height="3"
            rx="1.5" fill="rgba(26,20,70,0.2)"/>
          <path d="M10 9L13 9L13 14L16 14"
            stroke="#1A1446" stroke-width="1.8"
            fill="none" stroke-linecap="round"
            stroke-linejoin="round"/>
          <path d="M14 12L16 14L14 16"
            stroke="#1A1446" stroke-width="1.8"
            fill="none" stroke-linecap="round"
            stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <div style="font-size:20px;font-weight:500;
          color:#FFFFFF;letter-spacing:-0.3px;
          line-height:1.2;">
          Migrate<span style="color:#FFD000;">AI</span>
        </div>
        <div style="font-size:11px;margin-top:2px;
          color:rgba(255,255,255,0.45);">
          Intelligent data migration
          &middot; powered by GPT-4o
        </div>
      </div>
    </div>

    <!-- Status pill -->
    <div style="display:flex;align-items:center;
      gap:6px;padding:5px 12px;
      background:rgba(255,255,255,0.08);
      border:0.5px solid rgba(255,255,255,0.15);
      border-radius:20px;font-size:12px;
      color:rgba(255,255,255,0.85);">
      <span style="width:7px;height:7px;
        border-radius:50%;background:#4ADE80;
        display:inline-block;"></span>
      GPT-4o connected
    </div>
  </div>

  <!-- Row 2: Description -->
  <div style="margin-bottom:14px;">
    <div style="font-size:14px;font-weight:500;
      color:#FFFFFF;margin-bottom:5px;">
      Move your data
      <span style="color:#FFD000;">anywhere</span>,
      in minutes &mdash; just by having a conversation.
    </div>
    <div style="font-size:12px;line-height:1.6;
      color:rgba(255,255,255,0.5);max-width:700px;">
      No pipelines to build. No scripts to write.
      No engineers needed. Tell MigrateAI your source
      and destination, answer a few questions, and it
      handles the rest &mdash; schema mapping,
      validation, and delivery included.
    </div>
  </div>

  <!-- Row 3: Capability pills -->
  <div style="display:flex;flex-wrap:wrap;
    gap:6px;margin-bottom:14px;">
    <span style="display:inline-flex;
      align-items:center;gap:6px;padding:5px 11px;
      background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#9889;
      <strong style="color:#fff;">
        One-time full loads</strong>
    </span>
    <span style="display:inline-flex;
      align-items:center;gap:6px;padding:5px 11px;
      background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128737;
      <strong style="color:#fff;">
        Pre &amp; post validation</strong>
    </span>
    <span style="display:inline-flex;
      align-items:center;gap:6px;padding:5px 11px;
      background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128172;
      <strong style="color:#fff;">
        Chat-driven config</strong>
    </span>
    <span style="display:inline-flex;
      align-items:center;gap:6px;padding:5px 11px;
      background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128268;
      <strong style="color:#fff;">4 sources</strong>
      &mdash; Postgres &middot; CSV
      &middot; S3 &middot; Mongo
    </span>
    <span style="display:inline-flex;
      align-items:center;gap:6px;padding:5px 11px;
      background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);
      border-radius:7px;font-size:12px;
      color:rgba(255,255,255,0.8);">
      &#128452;
      <strong style="color:#fff;">4 destinations</strong>
      &mdash; BigQuery &middot; SQLite
      &middot; S3 &middot; Snowflake
    </span>
  </div>

  <!-- Row 4: Tab bar -->
  <div style="display:flex;border-top:0.5px solid
    rgba(255,255,255,0.12);margin:0 -28px;">
    <span style="padding:10px 20px;font-size:13px;
      color:#FFFFFF;cursor:pointer;
      border-bottom:2px solid #FFD000;">
      Chat</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">
      History</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">
      Output files</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">
      Settings</span>
  </div>
</div>
"""

# ── SECTION E — Session state ──────────────────────────────────────
if "agent" not in st.session_state:
    registry = build_default_registry(
        migrate_pg_to_bq      = migrate_postgres_to_bigquery,
        migrate_csv_to_sqlite = migrate_csv_to_sqlite,
        migrate_s3_to_sf      = migrate_s3_to_snowflake,
        migrate_mongo_to_s3   = migrate_mongo_to_s3,
    )
    st.session_state.agent = MigrationAgent(
        registry=registry
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

if "last_migrations" not in st.session_state:
    st.session_state.last_migrations = []


# ── SECTION F — Helper functions ───────────────────────────────────
def detect_and_record(text: str) -> None:
    lower = text.lower()
    if not any(w in lower for w in _COMPLETION_WORDS):
        return
    for src_k, dst_k, src_l, dst_l in _MIGRATION_PAIRS:
        if (any(k in lower for k in src_k) and
                any(k in lower for k in dst_k)):
            entry = {
                "label": f"{src_l} → {dst_l}",
                "detail": "done",
                "time": datetime.datetime.now()
                    .strftime("%H:%M"),
            }
            st.session_state.last_migrations.insert(
                0, entry
            )
            st.session_state.last_migrations = \
                st.session_state.last_migrations[:3]
            return


def send_message(prompt: str) -> None:
    """
    Core message handler used by both the chat input
    and quick start buttons.
    Appends user message, gets reply, appends reply,
    detects migration completion, triggers rerun.
    """
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    reply = st.session_state.agent.chat(prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    detect_and_record(reply)
    detect_and_record(prompt)


# ── SECTION G — Render hero ────────────────────────────────────────
# Hero must render BEFORE sidebar and chat
# so it appears above everything
st.markdown(_html(HERO_HTML), unsafe_allow_html=True)


# ── SECTION H — Sidebar ────────────────────────────────────────────
def build_last_migration_html() -> str:
    entries = st.session_state.last_migrations
    if not entries:
        badges = """
        <div style="font-size:11px;
          color:rgba(255,255,255,0.3);
          font-style:italic;padding:4px 0;">
          No migrations yet
        </div>
        """
    else:
        badges = ""
        for e in entries:
            badges += f"""
            <div style="display:flex;
              align-items:center;
              justify-content:space-between;
              padding:5px 8px;
              background:rgba(255,255,255,0.05);
              border-radius:6px;margin-bottom:3px;
              font-size:11px;
              color:rgba(255,255,255,0.6);">
              <span>
                <span style="width:5px;height:5px;
                  border-radius:50%;
                  background:#FFD000;
                  display:inline-block;
                  margin-right:5px;"></span>
                {e['label']}
              </span>
              <span>{e['detail']}</span>
            </div>
            """
    return _html(f"""
    <div style="padding:12px 4px;
      font-family:system-ui,-apple-system,sans-serif;">
      <div style="font-size:10px;font-weight:500;
        color:rgba(255,255,255,0.35);
        letter-spacing:0.08em;
        text-transform:uppercase;margin-bottom:8px;">
        Last Migration
      </div>
      {badges}
    </div>
    """)


with st.sidebar:

    # Quick Start label
    st.markdown(_html("""
    <div style="padding:14px 4px 6px;
      font-family:system-ui,-apple-system,sans-serif;">
      <div style="font-size:10px;font-weight:500;
        color:rgba(255,255,255,0.35);
        letter-spacing:0.08em;
        text-transform:uppercase;margin-bottom:4px;">
        Quick Start
      </div>
    </div>
    """), unsafe_allow_html=True)

    # Quick start buttons — each calls send_message() then st.rerun()
    if st.button(
        "🗄  Postgres → BigQuery",
        key="qs_pg_bq",
        use_container_width=True
    ):
        send_message(
            "I want to migrate data from "
            "Postgres to BigQuery"
        )
        st.rerun()

    if st.button(
        "📄  CSV → SQLite",
        key="qs_csv_sl",
        use_container_width=True
    ):
        send_message(
            "I need to load a CSV file into SQLite"
        )
        st.rerun()

    if st.button(
        "☁️   S3 → Snowflake",
        key="qs_s3_sf",
        use_container_width=True
    ):
        send_message(
            "I want to migrate data from "
            "S3 to Snowflake"
        )
        st.rerun()

    if st.button(
        "🍃  Mongo → S3",
        key="qs_mg_s3",
        use_container_width=True
    ):
        send_message(
            "I want to export a MongoDB collection to S3"
        )
        st.rerun()

    # Divider
    st.markdown("""
    <hr style="border:none;
      border-top:0.5px solid rgba(255,255,255,0.1);
      margin:12px 0;">
    """, unsafe_allow_html=True)

    # Last migration — rendered as HTML
    st.markdown(
        build_last_migration_html(),
        unsafe_allow_html=True
    )

    # Spacer to push New Migration to bottom
    st.markdown(
        "<div style='flex:1;min-height:20px;'></div>",
        unsafe_allow_html=True
    )

    # New Migration button — uses unique key so CSS can target it
    if st.button(
        "+ New Migration",
        key="reset_btn",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.agent.reset()
        st.session_state.messages = [
            {"role": "assistant",
             "content": WELCOME_MESSAGE}
        ]
        st.session_state.last_migrations = []
        st.rerun()


# ── SECTION I — Chat messages ──────────────────────────────────────
# Render all messages from session state
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── SECTION J — Chat input ─────────────────────────────────────────
# st.chat_input() is automatically pinned to bottom
# Returns string when submitted, None otherwise
if prompt := st.chat_input("Type your reply…"):
    send_message(prompt)
    st.rerun()


# ── SECTION K — New Migration button CSS override ──────────────────
# Added AFTER all components are rendered
# so it targets the correct rendered button
st.markdown("""
<style>
/* Target New Migration by its Streamlit key */
div[data-testid="stSidebar"]
  button[kind="primary"] {
  background: #FFD000 !important;
  color: #1A1446 !important;
  font-weight: 600 !important;
  border: none !important;
  box-shadow: none !important;
}
div[data-testid="stSidebar"]
  button[kind="primary"] p {
  color: #1A1446 !important;
}
div[data-testid="stSidebar"]
  button[kind="primary"]:hover {
  background: #E6BB00 !important;
}
</style>
""", unsafe_allow_html=True)
