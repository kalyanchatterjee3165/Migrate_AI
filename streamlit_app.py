import streamlit as st
import datetime
import config.settings as settings  # noqa: F401 — validates env on import

from llm.agent import MigrationAgent
from llm.tool_registry import build_default_registry
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

WELCOME_MESSAGE = (
    "👋 Hey! I'm **MigrateAI** — your intelligent data "
    "migration assistant.\n\n"
    "I can help you move data between systems in minutes, "
    "just by having a conversation. "
    "No scripts, no pipelines, no engineers needed.\n\n"
    "**To get started, either:**\n"
    "- Click a **Quick Start** path in the sidebar\n"
    "- Or tell me what you want to migrate in your own words\n\n"
    "**Supported sources:** Postgres · CSV · S3 · MongoDB\n"
    "**Supported destinations:** BigQuery · SQLite · S3 · Snowflake"
)

_COMPLETION_WORDS = {
    "rows", "migrated", "complete", "success", "transferred"
}
_MIGRATION_PAIRS = [
    (("postgres",), ("bigquery",),  "Postgres", "BigQuery"),
    (("csv",),      ("sqlite",),    "CSV",      "SQLite"),
    (("s3",),       ("snowflake",), "S3",       "Snowflake"),
    (("mongo",),    ("s3",),        "Mongo",    "S3"),
]

# ------------------------------------------------------------------
# Page config — must be the FIRST Streamlit call
# ------------------------------------------------------------------

st.set_page_config(
    page_title="MigrateAI",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# CSS injection
# ------------------------------------------------------------------

CUSTOM_CSS = """
<style>

/* Hide Streamlit default chrome */
#MainMenu { display: none !important; }
header { display: none !important; }
footer { display: none !important; }
.stDeployButton { display: none !important; }

/* Remove default padding from main area */
.main .block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* Sidebar background — dark navy */
section[data-testid="stSidebar"] {
  background: #002663 !important;
  min-width: 240px !important;
  max-width: 240px !important;
}
section[data-testid="stSidebar"] > div {
  background: #002663 !important;
  padding: 0 !important;
}

/* Sidebar text color */
section[data-testid="stSidebar"] * {
  color: rgba(255,255,255,0.75) !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton button {
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
}
section[data-testid="stSidebar"] .stButton button:hover {
  background: rgba(255,255,255,0.1) !important;
  color: #FFFFFF !important;
}

/* New Migration button — yellow */
section[data-testid="stSidebar"] .stButton:last-of-type button {
  background: #FFD000 !important;
  color: #1A1446 !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  margin-top: 8px !important;
}
section[data-testid="stSidebar"] .stButton:last-of-type button:hover {
  background: #E6BB00 !important;
}

/* Chat message — user bubble */
div[data-testid="stChatMessage"]:has(
  div[data-testid="stChatMessageAvatarUser"]
) {
  background: #1A1446 !important;
  border-radius: 12px 2px 12px 12px !important;
  padding: 10px 14px !important;
}
div[data-testid="stChatMessage"]:has(
  div[data-testid="stChatMessageAvatarUser"]
) p {
  color: #FFFFFF !important;
}

/* Chat message — AI bubble */
div[data-testid="stChatMessage"]:has(
  div[data-testid="stChatMessageAvatarAssistant"]
) {
  background: #FFFFFF !important;
  border: 0.5px solid rgba(26,20,70,0.15) !important;
  border-radius: 2px 12px 12px 12px !important;
  padding: 10px 14px !important;
}

/* Chat input */
div[data-testid="stChatInput"] textarea {
  background: #FFFFFF !important;
  border: 1px solid rgba(26,20,70,0.2) !important;
  border-radius: 10px !important;
  color: #1A1446 !important;
  font-size: 13px !important;
}
div[data-testid="stChatInput"] button {
  background: #FFD000 !important;
  color: #1A1446 !important;
  border-radius: 8px !important;
}

/* Main area background */
.main {
  background: #F4F4F4 !important;
}

hr {
  margin: 8px 0 !important;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# Hero header
# ------------------------------------------------------------------

HERO_HTML = """
<div style="
  background:#1A1446;width:100%;
  padding:16px 28px 0;box-sizing:border-box;
  font-family:system-ui,-apple-system,sans-serif;
  margin-bottom:0;
">
  <div style="display:flex;align-items:center;
    justify-content:space-between;margin-bottom:12px;">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:42px;height:42px;background:#FFD000;
        border-radius:11px;display:flex;align-items:center;
        justify-content:center;flex-shrink:0;">
        <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
          <rect x="2" y="5" width="8" height="8" rx="2" fill="#1A1446"/>
          <rect x="2" y="16" width="8" height="3" rx="1.5"
            fill="rgba(26,20,70,0.3)"/>
          <rect x="16" y="10" width="8" height="8" rx="2"
            fill="#1A1446" opacity="0.8"/>
          <rect x="16" y="21" width="8" height="3" rx="1.5"
            fill="rgba(26,20,70,0.2)"/>
          <path d="M10 9L13 9L13 14L16 14" stroke="#1A1446"
            stroke-width="1.8" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 12L16 14L14 16" stroke="#1A1446"
            stroke-width="1.8" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <div style="font-size:20px;font-weight:500;
          color:#FFFFFF;letter-spacing:-0.3px;">
          Migrate<span style="color:#FFD000;">AI</span>
        </div>
        <div style="font-size:11px;color:rgba(255,255,255,0.45);
          margin-top:2px;">
          Intelligent data migration &middot; powered by GPT-4o
        </div>
      </div>
    </div>
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

  <div style="margin-bottom:14px;">
    <div style="font-size:14px;font-weight:500;color:#FFFFFF;
      margin-bottom:4px;">
      Move your data <span style="color:#FFD000;">anywhere</span>,
      in minutes &mdash; just by having a conversation.
    </div>
    <div style="font-size:12px;color:rgba(255,255,255,0.5);
      line-height:1.6;max-width:700px;">
      No pipelines to build. No scripts to write. No engineers needed.
      Tell MigrateAI your source and destination, answer a few
      questions, and it handles the rest &mdash; schema mapping,
      validation, and delivery included.
    </div>
  </div>

  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;">
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);border-radius:7px;
      font-size:12px;color:rgba(255,255,255,0.8);">
      &#9889; <strong style="color:#fff;">One-time full loads</strong>
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);border-radius:7px;
      font-size:12px;color:rgba(255,255,255,0.8);">
      &#128737;
      <strong style="color:#fff;">Pre &amp; post validation</strong>
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);border-radius:7px;
      font-size:12px;color:rgba(255,255,255,0.8);">
      &#128172;
      <strong style="color:#fff;">Chat-driven config</strong>
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);border-radius:7px;
      font-size:12px;color:rgba(255,255,255,0.8);">
      &#128268; <strong style="color:#fff;">4 sources</strong>
      &mdash; Postgres &middot; CSV &middot; S3 &middot; Mongo
    </span>
    <span style="display:inline-flex;align-items:center;gap:6px;
      padding:5px 11px;background:rgba(255,255,255,0.07);
      border:0.5px solid rgba(255,255,255,0.13);border-radius:7px;
      font-size:12px;color:rgba(255,255,255,0.8);">
      &#128452; <strong style="color:#fff;">4 destinations</strong>
      &mdash; BigQuery &middot; SQLite &middot; S3 &middot; Snowflake
    </span>
  </div>

  <div style="display:flex;border-top:0.5px solid
    rgba(255,255,255,0.12);margin:0 -28px;">
    <span style="padding:10px 20px;font-size:13px;color:#FFFFFF;
      border-bottom:2px solid #FFD000;cursor:pointer;">Chat</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">History</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">Output files</span>
    <span style="padding:10px 20px;font-size:13px;
      color:rgba(255,255,255,0.4);cursor:pointer;">Settings</span>
  </div>
</div>
"""

st.markdown(HERO_HTML, unsafe_allow_html=True)

# ------------------------------------------------------------------
# Session state — initialised once on first load
# ------------------------------------------------------------------

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

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def detect_and_record_migration(text: str) -> None:
    lower = text.lower()
    if not any(w in lower for w in _COMPLETION_WORDS):
        return
    for src_keys, dst_keys, src_label, dst_label in _MIGRATION_PAIRS:
        if (any(k in lower for k in src_keys) and
                any(k in lower for k in dst_keys)):
            entry = {
                "label": f"{src_label} → {dst_label}",
                "detail": "done",
                "time": datetime.datetime.now().strftime("%H:%M"),
            }
            st.session_state.last_migrations.insert(0, entry)
            st.session_state.last_migrations = \
                st.session_state.last_migrations[:3]
            return

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="padding:14px 10px 6px;
          font-family:system-ui,-apple-system,sans-serif;">
          <div style="font-size:10px;font-weight:500;
            color:rgba(255,255,255,0.35);letter-spacing:0.08em;
            text-transform:uppercase;padding:0 8px;
            margin-bottom:6px;">
            Quick Start
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗄  Postgres → BigQuery", key="qs1",
                 use_container_width=True):
        prompt = "I want to migrate data from Postgres to BigQuery"
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        reply = st.session_state.agent.chat(prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        detect_and_record_migration(reply)
        st.rerun()

    if st.button("📄  CSV → SQLite", key="qs2",
                 use_container_width=True):
        prompt = "I need to load a CSV file into SQLite"
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        reply = st.session_state.agent.chat(prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        detect_and_record_migration(reply)
        st.rerun()

    if st.button("☁️  S3 → Snowflake", key="qs3",
                 use_container_width=True):
        prompt = "I want to migrate data from S3 to Snowflake"
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        reply = st.session_state.agent.chat(prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        detect_and_record_migration(reply)
        st.rerun()

    if st.button("🍃  Mongo → S3", key="qs4",
                 use_container_width=True):
        prompt = "I want to export a MongoDB collection to S3"
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        reply = st.session_state.agent.chat(prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        detect_and_record_migration(reply)
        st.rerun()

    st.markdown(
        """<hr style="border:0.5px solid rgba(255,255,255,0.1);
          margin:12px 0;">""",
        unsafe_allow_html=True,
    )

    last_migs = st.session_state.last_migrations
    last_html = """
    <div style="padding:0 10px;
      font-family:system-ui,-apple-system,sans-serif;">
      <div style="font-size:10px;font-weight:500;
        color:rgba(255,255,255,0.35);letter-spacing:0.08em;
        text-transform:uppercase;margin-bottom:8px;">
        Last Migration
      </div>
    """
    if not last_migs:
        last_html += """
      <div style="font-size:11px;color:rgba(255,255,255,0.3);
        font-style:italic;">No migrations yet</div>
        """
    else:
        for e in last_migs:
            last_html += f"""
      <div style="display:flex;align-items:center;
        justify-content:space-between;padding:5px 8px;
        background:rgba(255,255,255,0.05);border-radius:6px;
        margin-bottom:3px;font-size:11px;
        color:rgba(255,255,255,0.6);">
        <span>
          <span style="width:5px;height:5px;border-radius:50%;
            background:#FFD000;display:inline-block;
            margin-right:5px;"></span>
          {e['label']}
        </span>
        <span>{e['detail']}</span>
      </div>
            """
    last_html += "</div>"
    st.markdown(last_html, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if st.button("＋ New Migration", key="reset",
                 use_container_width=True):
        st.session_state.agent.reset()
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]
        st.session_state.last_migrations = []
        st.rerun()

# ------------------------------------------------------------------
# Chat area
# ------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------------------------------
# Chat input
# ------------------------------------------------------------------

if user_input := st.chat_input("Type your reply…"):
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner(""):
            reply = st.session_state.agent.chat(user_input)
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    detect_and_record_migration(reply)
    st.rerun()
