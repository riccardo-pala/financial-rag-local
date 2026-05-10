APP_CSS = """
<style>
:root {
    --surface: #f8fafc;
    --panel: #ffffff;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #dbe3ef;
    --accent: #0f766e;
    --accent-soft: #ccfbf1;
}
.stApp {
    background:
        radial-gradient(circle at 20% 0%, rgba(20, 184, 166, 0.10), transparent 28rem),
        linear-gradient(180deg, #f8fafc 0%, #eef4f8 100%);
}
.main .block-container {
    max-width: 1040px;
    padding-top: 2rem;
}
[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * {
    color: var(--ink);
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: var(--ink);
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: var(--muted);
}
.hero-panel {
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid var(--line);
    border-radius: 16px;
    box-shadow: 0 18px 55px rgba(15, 23, 42, 0.08);
    margin-bottom: 1.25rem;
    padding: 1.35rem 1.45rem 1.25rem;
    position: relative;
}
.hero-panel:before {
    background: linear-gradient(90deg, #0f766e, #2563eb);
    border-radius: 16px 16px 0 0;
    content: "";
    height: 4px;
    left: -1px;
    position: absolute;
    right: -1px;
    top: -1px;
}
.app-kicker {
    color: var(--accent);
    font-size: 0.84rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
}
.app-title {
    color: var(--ink);
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: 0;
    line-height: 1.08;
    margin-bottom: 0.35rem;
}
.app-subtitle {
    color: #475569;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 0;
}
.doc-row {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 10px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
    margin-bottom: 0.45rem;
    padding: 0.65rem 0.7rem;
}
.doc-name {
    color: var(--ink);
    font-size: 0.88rem;
    font-weight: 700;
    line-height: 1.25;
    overflow-wrap: anywhere;
}
.doc-meta {
    color: var(--muted);
    font-size: 0.76rem;
    margin-top: 0.22rem;
}
.doc-badge {
    background: var(--accent-soft);
    border-radius: 999px;
    color: #115e59;
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 800;
    margin-top: 0.42rem;
    padding: 0.12rem 0.45rem;
    text-transform: uppercase;
}
.status-pill {
    border-radius: 999px;
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    padding: 0.28rem 0.65rem;
}
.status-ready {
    background: #dcfce7;
    color: #166534;
}
.status-missing {
    background: #fee2e2;
    color: #991b1b;
}
div[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.74);
    border: 1px solid rgba(219, 227, 239, 0.85);
    border-radius: 10px;
    padding: 0.55rem;
}
div.stButton > button {
    border-radius: 10px;
    border-color: var(--line);
    font-weight: 700;
}
div.stButton > button:hover {
    border-color: var(--accent);
    color: var(--accent);
}
</style>
"""
