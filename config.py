"""
Modern Sleek UI Theme & Professional Design System
Provides vector SVG iconography, high-contrast visibility, and proper sidebar toggle mechanics.
"""

CURRENCY_SYMBOLS = {
    "INR (₹)": "₹",
    "USD ($)": "$",
    "EUR (€)": "€",
    "GBP (£)": "£"
}

# Crisp, vector SVG icons (Lucide-inspired)
SVG_ICONS = {
    "wallet": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>""",
    "trending": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
    "percent": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>""",
    "package": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>""",
    "plus": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>""",
    "table": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/></svg>""",
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>"""
}

CUSTOM_CSS = """
<style>
    /* Google Font: Plus Jakarta Sans */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Overall clean light workspace */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    /* Ensure Sidebar Collapse / Expand Button IS ALWAYS VISIBLE */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[kind="header"] {
        display: flex !important;
        visibility: visible !important;
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
        top: 0.75rem !important;
        left: 0.75rem !important;
        z-index: 999999 !important;
    }

    /* Hide only deploy button and watermark footer */
    .stDeployButton, footer, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    /* Header styling - transparent background so button is accessible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Layout Container Alignment */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1250px !important;
    }

    /* High contrast text guarantees */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #0F172A !important;
    }

    h1 {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 0.25rem !important;
    }

    .sub-heading {
        color: #64748B !important;
        font-size: 0.925rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }

    /* Modern Professional Metric Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
        width: 100%;
    }

    .metric-card-pro {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .metric-card-pro:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        border-color: #CBD5E1;
    }

    .card-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 0.775rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748B !important;
    }

    .icon-badge {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F8FAFC;
        border: 1px solid #F1F5F9;
    }

    .card-val {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0F172A !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    .card-note {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B !important;
        margin-top: 4px;
    }

    /* Segmented Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #F1F5F9;
        border-radius: 10px;
        padding: 4px;
        border: none !important;
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 7px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        color: #475569 !important;
        transition: all 0.15s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    }

    /* Form Container Polish */
    .pro-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        margin-bottom: 20px;
    }

    /* Input Fields Alignment & Styling */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        color: #1E293B !important;
        margin-bottom: 4px !important;
    }

    input, select, textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 9px 18px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.15s ease;
    }

    .stButton>button:hover {
        background-color: #1E293B !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* Cross-device Responsiveness */
    @media (max-width: 900px) {
        .metric-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }

    @media (max-width: 600px) {
        .block-container {
            padding: 1.25rem 1rem !important;
        }
        h1 {
            font-size: 1.45rem !important;
        }
        .metric-grid {
            grid-template-columns: 1fr !important;
        }
    }
</style>
"""
