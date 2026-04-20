"""
O'zbekiston To'lov Balansi — v10.0
python -m streamlit run dashboard.py
"""
import io, datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="O'zbekiston · To'lov Balansi",
    page_icon="🇺🇿", layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════
# TRANSLATIONS  (to'liq, xatosiz)
# ═══════════════════════════════════════
T = {
"uz": dict(
    title        = "To'lov Balansi",
    country      = "O'zbekiston Respublikasi",
    method       = "IMF BPM6",
    lang_lbl     = "Til",
    dtype_lbl    = "Ma'lumot turi",
    quarterly    = "Choraklik",
    annual       = "Yillik",
    yr_range     = "Yil oralig'i",
    yr_from      = "Boshlanish",
    yr_to        = "Tugash",
    focus        = "Alohida yil",
    all_         = "Barchasi",
    sections     = "Bo'limlar",
    p_ca         = "Joriy hisob",
    p_tr         = "Savdo",
    p_fi         = "Investitsiyalar",
    p_re         = "Zaxiralar",
    p_an         = "Tahlil",
    source       = "Manba: O'zbekiston Markaziy banki",
    updated      = "Yangilangan",
    qtrs         = "chorak",
    surplus      = "Profitsit",
    deficit      = "Defitsit",
    latest       = "so'nggi qiymat",
    period       = "Davr",
    mln          = "mln $",
    # Tab nomlari
    t1="Bosh sahifa", t2="Joriy hisob",
    t3="Moliyaviy hisob", t4="Zaxiralar",
    t5="Tahlil", t6="Ma'lumotlar",
    # KPI
    k_ca   = "Joriy hisob saldosi",
    k_fi   = "Moliyaviy hisob",
    k_res  = "Zaxira aktivlari",
    k_ex   = "Eksport",
    k_im   = "Import",
    k_tr   = "Savdo saldosi",
    # Grafik sarlavhalari
    g_ca       = "Joriy hisob saldosi",
    g_fi       = "Moliyaviy hisob",
    g_res      = "Zaxira aktivlari",
    g_trade    = "Eksport va Import",
    g_net      = "Savdo saldosi",
    g_ex_str   = "Eksport tarkibi",
    g_im_str   = "Import tarkibi",
    g_cov      = "Eksport/Import nisbati",
    g_income   = "Birlamchi va ikkilamchi daromadlar",
    g_fdi      = "To'g'ridan-to'g'ri investitsiyalar",
    g_port     = "Portfel investitsiyalar",
    g_other    = "Boshqa investitsiyalar",
    g_netfl    = "Sof investitsiya oqimlari",
    g_fistack  = "Moliyaviy hisob tarkibi",
    g_bal      = "Umumiy balans va Zaxiralar",
    g_err      = "Sof xatolar va yo'qotishlar",
    g_cum      = "Kumulyativ zaxira",
    g_yoy      = "Yillik o'zgarish (%)",
    g_scatter  = "Eksport va joriy hisob korrelyatsiyasi",
    g_hist     = "Savdo saldosi taqsimoti",
    g_heatmap  = "Joriy hisob: yil × chorak",
    g_vol      = "Savdo hajmi",
    g_ratio    = "Eksport/Import nisbati",
    g_funnel   = "BOP tarkibiy tahlili",
    g_annual   = "Yillik ko'rsatkichlar",
    g_allcomp  = "Asosiy komponentlar",
    # Ustun nomlari
    c_period   = "Davr",
    c_ca       = "Joriy hisob",
    c_ex       = "Eksport",
    c_im       = "Import",
    c_net      = "Savdo saldosi",
    c_fi       = "Moliyaviy hisob",
    c_fdia     = "TII aktivlar",
    c_fdim     = "TII majburiyatlar",
    c_err      = "Sof xatolar",
    c_ov       = "Umumiy balans",
    c_re       = "Zaxira aktivlari",
    c_exg      = "Tovar eksporti",
    c_exs      = "Xizmat eksporti",
    c_img      = "Tovar importi",
    c_ims      = "Xizmat importi",
    c_p1       = "Birlamchi daromad (kreditlar)",
    c_p2       = "Birlamchi daromad (debetlar)",
    c_s1       = "Ikkilamchi daromad (kreditlar)",
    c_s2       = "Ikkilamchi daromad (debetlar)",
    c_ratio    = "Eks/Imp %",
    # Boshqalar
    assets     = "Aktivlar",
    liab       = "Majburiyatlar",
    rolling    = "4 davrli o'rtacha",
    trend      = "Trend",
    net_fdi    = "TII sof",
    net_port   = "Portfel sof",
    net_oth    = "Boshqa sof",
    tdi_in     = "TII (kiruvchi)",
    port_in    = "Portfel (kiruvchi)",
    oth_in     = "Boshqa (kiruvchi)",
    cumul      = "Kumulyativ",
    distrib    = "Taqsimot",
    boxlbl     = "Quti diagrammasi",
    cov_lbl    = "Qoplash nisbati",
    tradeVol   = "Savdo hajmi",
    threshold  = "100% (muvozanat chegarasi)",
    dl_csv     = "CSV yuklab olish",
    dl_xl      = "Excel yuklab olish",
    footer     = "O'zbekiston Respublikasi To'lov Balansi · IMF BPM6 metodologiyasi",
),
"en": dict(
    title        = "Balance of Payments",
    country      = "Republic of Uzbekistan",
    method       = "IMF BPM6",
    lang_lbl     = "Language",
    dtype_lbl    = "Data type",
    quarterly    = "Quarterly",
    annual       = "Annual",
    yr_range     = "Year range",
    yr_from      = "From",
    yr_to        = "To",
    focus        = "Single year",
    all_         = "All",
    sections     = "Sections",
    p_ca         = "Current account",
    p_tr         = "Trade",
    p_fi         = "Investments",
    p_re         = "Reserves",
    p_an         = "Analytics",
    source       = "Source: Central Bank of Uzbekistan",
    updated      = "Updated",
    qtrs         = "quarters",
    surplus      = "Surplus",
    deficit      = "Deficit",
    latest       = "latest value",
    period       = "Period",
    mln          = "mln $",
    t1="Overview", t2="Current account",
    t3="Financial account", t4="Reserves",
    t5="Analytics", t6="Data",
    k_ca   = "Current account balance",
    k_fi   = "Financial account",
    k_res  = "Reserve assets",
    k_ex   = "Exports",
    k_im   = "Imports",
    k_tr   = "Trade balance",
    g_ca       = "Current account balance",
    g_fi       = "Financial account",
    g_res      = "Reserve assets",
    g_trade    = "Exports & Imports",
    g_net      = "Trade balance",
    g_ex_str   = "Export structure",
    g_im_str   = "Import structure",
    g_cov      = "Export/Import ratio",
    g_income   = "Primary and secondary income",
    g_fdi      = "Foreign direct investment",
    g_port     = "Portfolio investment",
    g_other    = "Other investment",
    g_netfl    = "Net investment flows",
    g_fistack  = "Financial account structure",
    g_bal      = "Overall balance & Reserves",
    g_err      = "Net errors & omissions",
    g_cum      = "Cumulative reserves",
    g_yoy      = "Year-on-year change (%)",
    g_scatter  = "Exports vs current account correlation",
    g_hist     = "Trade balance distribution",
    g_heatmap  = "Current account: year × quarter",
    g_vol      = "Trade volume",
    g_ratio    = "Export/Import ratio",
    g_funnel   = "BOP structural analysis",
    g_annual   = "Annual figures",
    g_allcomp  = "Main components",
    c_period   = "Period",
    c_ca       = "Current account",
    c_ex       = "Exports",
    c_im       = "Imports",
    c_net      = "Trade balance",
    c_fi       = "Financial account",
    c_fdia     = "FDI assets",
    c_fdim     = "FDI liabilities",
    c_err      = "Net errors",
    c_ov       = "Overall balance",
    c_re       = "Reserve assets",
    c_exg      = "Goods exports",
    c_exs      = "Services exports",
    c_img      = "Goods imports",
    c_ims      = "Services imports",
    c_p1       = "Primary income (credits)",
    c_p2       = "Primary income (debits)",
    c_s1       = "Secondary income (credits)",
    c_s2       = "Secondary income (debits)",
    c_ratio    = "Exp/Imp %",
    assets     = "Assets",
    liab       = "Liabilities",
    rolling    = "4-period average",
    trend      = "Trend",
    net_fdi    = "FDI net",
    net_port   = "Portfolio net",
    net_oth    = "Other net",
    tdi_in     = "FDI (inward)",
    port_in    = "Portfolio (inward)",
    oth_in     = "Other (inward)",
    cumul      = "Cumulative",
    distrib    = "Distribution",
    boxlbl     = "Box plot",
    cov_lbl    = "Coverage ratio",
    tradeVol   = "Trade volume",
    threshold  = "100% (equilibrium)",
    dl_csv     = "Download CSV",
    dl_xl      = "Download Excel",
    footer     = "Republic of Uzbekistan Balance of Payments · IMF BPM6 Methodology",
),
"ru": dict(
    title        = "Платёжный баланс",
    country      = "Республика Узбекистан",
    method       = "МВФ BPM6",
    lang_lbl     = "Язык",
    dtype_lbl    = "Тип данных",
    quarterly    = "Квартальные",
    annual       = "Годовые",
    yr_range     = "Диапазон лет",
    yr_from      = "Начало",
    yr_to        = "Конец",
    focus        = "Отдельный год",
    all_         = "Все",
    sections     = "Разделы",
    p_ca         = "Текущий счёт",
    p_tr         = "Торговля",
    p_fi         = "Инвестиции",
    p_re         = "Резервы",
    p_an         = "Аналитика",
    source       = "Источник: Центральный банк Узбекистана",
    updated      = "Обновлено",
    qtrs         = "кварталов",
    surplus      = "Профицит",
    deficit      = "Дефицит",
    latest       = "последнее значение",
    period       = "Период",
    mln          = "млн $",
    t1="Обзор", t2="Текущий счёт",
    t3="Финансовый счёт", t4="Резервы",
    t5="Аналитика", t6="Данные",
    k_ca   = "Сальдо текущего счёта",
    k_fi   = "Финансовый счёт",
    k_res  = "Резервные активы",
    k_ex   = "Экспорт",
    k_im   = "Импорт",
    k_tr   = "Торговый баланс",
    g_ca       = "Сальдо текущего счёта",
    g_fi       = "Финансовый счёт",
    g_res      = "Резервные активы",
    g_trade    = "Экспорт и Импорт",
    g_net      = "Торговый баланс",
    g_ex_str   = "Структура экспорта",
    g_im_str   = "Структура импорта",
    g_cov      = "Соотношение экспорта/импорта",
    g_income   = "Первичные и вторичные доходы",
    g_fdi      = "Прямые иностранные инвестиции",
    g_port     = "Портфельные инвестиции",
    g_other    = "Прочие инвестиции",
    g_netfl    = "Чистые инвестиционные потоки",
    g_fistack  = "Структура финансового счёта",
    g_bal      = "Общий баланс и резервы",
    g_err      = "Чистые ошибки и пропуски",
    g_cum      = "Накопленные резервы",
    g_yoy      = "Изменение год к году (%)",
    g_scatter  = "Корреляция экспорта и текущего счёта",
    g_hist     = "Распределение торгового баланса",
    g_heatmap  = "Текущий счёт: год × квартал",
    g_vol      = "Объём торговли",
    g_ratio    = "Соотношение экспорта/импорта",
    g_funnel   = "Структурный анализ ПБ",
    g_annual   = "Годовые показатели",
    g_allcomp  = "Основные компоненты",
    c_period   = "Период",
    c_ca       = "Текущий счёт",
    c_ex       = "Экспорт",
    c_im       = "Импорт",
    c_net      = "Торговый баланс",
    c_fi       = "Финансовый счёт",
    c_fdia     = "ПИИ активы",
    c_fdim     = "ПИИ обязательства",
    c_err      = "Чистые ошибки",
    c_ov       = "Общий баланс",
    c_re       = "Резервные активы",
    c_exg      = "Товарный экспорт",
    c_exs      = "Экспорт услуг",
    c_img      = "Товарный импорт",
    c_ims      = "Импорт услуг",
    c_p1       = "Первичные доходы (кредиты)",
    c_p2       = "Первичные доходы (дебеты)",
    c_s1       = "Вторичные доходы (кредиты)",
    c_s2       = "Вторичные доходы (дебеты)",
    c_ratio    = "Экс/Имп %",
    assets     = "Активы",
    liab       = "Обязательства",
    rolling    = "Среднее за 4 периода",
    trend      = "Тренд",
    net_fdi    = "ПИИ нетто",
    net_port   = "Портфель нетто",
    net_oth    = "Прочие нетто",
    tdi_in     = "ПИИ (входящие)",
    port_in    = "Портфель (входящие)",
    oth_in     = "Прочие (входящие)",
    cumul      = "Накопленный",
    distrib    = "Распределение",
    boxlbl     = "Ящик с усами",
    cov_lbl    = "Коэффициент покрытия",
    tradeVol   = "Объём торговли",
    threshold  = "100% (граница равновесия)",
    dl_csv     = "Скачать CSV",
    dl_xl      = "Скачать Excel",
    footer     = "Платёжный баланс Республики Узбекистан · МВФ BPM6",
),
}

# ═══════════════════════════════════════
# DESIGN TOKENS
# ═══════════════════════════════════════
# Asosiy ranglar — Slate + Indigo (zamonaviy va rasmiy)
P_BG     = "#F8F9FC"   # sahifa foni
P_WHITE  = "#FFFFFF"
P_BORDER = "#E4E8EF"   # chegara
P_DARK   = "#0F172A"   # asosiy matn
P_MED    = "#475569"   # ikkinchi darajali matn
P_MUTED  = "#94A3B8"   # past matn
P_SIDE   = "#1E293B"   # sidebar foni
P_SIDEB  = "#334155"   # sidebar border

# Aksent ranglar
A_BLUE   = "#2563EB"   # primary
A_LBLUE  = "#93C5FD"   # light blue
A_GREEN  = "#16A34A"   # positive
A_RED    = "#DC2626"   # negative
A_AMBER  = "#D97706"   # warning / import
A_TEAL   = "#0891B2"   # secondary
A_PURPLE = "#7C3AED"   # accent

# Plotly ranglar (chart-friendly)
CH = dict(
    blue   = "#2563EB",
    lblue  = "#60A5FA",
    green  = "#16A34A",
    lgreen = "#4ADE80",
    red    = "#DC2626",
    lred   = "#F87171",
    amber  = "#D97706",
    lamber = "#FCD34D",
    teal   = "#0891B2",
    lteal  = "#38BDF8",
    purple = "#7C3AED",
    lpurp  = "#A78BFA",
    grey   = "#64748B",
)

FILLS = {
    CH["blue"]:   "rgba(37,99,235,0.55)",
    CH["teal"]:   "rgba(8,145,178,0.55)",
    CH["green"]:  "rgba(22,163,74,0.55)",
    CH["amber"]:  "rgba(217,119,6,0.55)",
    CH["purple"]: "rgba(124,58,237,0.55)",
}

# ═══════════════════════════════════════
# CSS
# ═══════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=DM+Mono:wght@400;500&display=swap');

*,html,body,[class*="css"]{{font-family:'DM Sans',sans-serif!important;}}
.stApp,.main{{background:{P_BG}!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{{
    background:{P_SIDE}!important;border-right:1px solid {P_SIDEB}!important;
    min-width:200px!important;max-width:200px!important;
}}
[data-testid="stSidebar"]>div{{padding:0!important;}}
[data-testid="stSidebar"] *{{color:#94A3B8!important;}}
[data-testid="stSidebar"] hr{{border:none!important;border-top:1px solid {P_SIDEB}!important;margin:0!important;}}
[data-testid="stSidebar"] .stRadio label span,
[data-testid="stSidebar"] .stCheckbox span p{{color:#CBD5E1!important;font-size:13px!important;font-weight:400!important;}}
[data-testid="stSidebar"] [data-baseweb="select"]>div{{
    background:rgba(255,255,255,0.05)!important;border:1px solid {P_SIDEB}!important;
    border-radius:6px!important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] span{{color:#E2E8F0!important;font-size:13px!important;}}
[data-testid="stSidebar"] [data-baseweb="select"] svg{{fill:#475569!important;}}
[data-testid="stSidebar"] [data-baseweb="checkbox"]>div:first-child{{
    border-color:#475569!important;border-radius:4px!important;background:rgba(255,255,255,0.04)!important;
}}
[data-testid="stSidebar"] .stButton>button{{
    border-radius:6px!important;font-size:12px!important;font-weight:600!important;
    padding:6px 0!important;border:1px solid #334155!important;
    background:rgba(255,255,255,0.04)!important;color:#94A3B8!important;
    transition:all 0.15s!important;letter-spacing:0.3px!important;
}}
[data-testid="stSidebar"] .stButton>button:hover{{
    background:rgba(37,99,235,0.15)!important;border-color:#2563EB!important;color:#93C5FD!important;
}}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{{
    background:{A_BLUE}!important;border-color:{A_BLUE}!important;
    color:#FFFFFF!important;
}}

/* ── METRICS ── */
[data-testid="metric-container"]{{
    background:{P_WHITE};border:1px solid {P_BORDER};border-radius:10px;
    padding:18px 20px!important;
    box-shadow:0 1px 2px rgba(0,0,0,0.04),0 4px 12px rgba(0,0,0,0.04);
    transition:box-shadow 0.2s;
}}
[data-testid="metric-container"]:hover{{box-shadow:0 4px 20px rgba(37,99,235,0.1);}}
[data-testid="stMetricValue"]{{
    font-size:22px!important;font-weight:700!important;color:{P_DARK}!important;
    font-family:'DM Mono',monospace!important;letter-spacing:-0.5px!important;
}}
[data-testid="stMetricLabel"]{{
    font-size:11px!important;font-weight:600!important;color:{P_MUTED}!important;
    text-transform:uppercase!important;letter-spacing:0.8px!important;
}}
[data-testid="stMetricDelta"]{{font-size:12px!important;font-family:'DM Mono',monospace!important;}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{{
    background:{P_WHITE}!important;border-bottom:1px solid {P_BORDER}!important;
    gap:0!important;padding:0 24px!important;margin-bottom:0!important;
}}
.stTabs [data-baseweb="tab"]{{
    background:transparent!important;border:none!important;
    border-bottom:2px solid transparent!important;border-radius:0!important;
    padding:13px 18px!important;font-size:12px!important;font-weight:600!important;
    color:{P_MUTED}!important;letter-spacing:0.3px!important;
    text-transform:uppercase!important;margin-bottom:-1px!important;
    transition:color 0.15s!important;
}}
.stTabs [aria-selected="true"]{{color:{A_BLUE}!important;border-bottom:2px solid {A_BLUE}!important;}}
.stTabs [data-baseweb="tab-panel"]{{
    padding-top:0!important;background:transparent!important;
    animation:fadeUp 0.2s ease!important;
}}

@keyframes fadeUp{{
    from{{opacity:0;transform:translateY(8px);}}
    to{{opacity:1;transform:translateY(0);}}
}}

/* ── CHART CARD ── */
.gchart{{
    background:{P_WHITE};border:1px solid {P_BORDER};border-radius:10px;
    padding:18px 20px 12px;margin-bottom:14px;
    box-shadow:0 1px 2px rgba(0,0,0,0.03);
    transition:box-shadow 0.2s;
}}
.gchart:hover{{box-shadow:0 4px 16px rgba(0,0,0,0.07);}}
.gchart-title{{
    font-size:13px;font-weight:600;color:{P_DARK};
    margin-bottom:2px;line-height:1.3;
}}
.gchart-sub{{
    font-size:11px;color:{P_MUTED};margin-bottom:12px;
    padding-bottom:10px;border-bottom:1px solid {P_BORDER};
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{{width:4px;height:4px;}}
::-webkit-scrollbar-track{{background:{P_BG};}}
::-webkit-scrollbar-thumb{{background:{P_BORDER};border-radius:10px;}}

/* ── DOWNLOAD ── */
.stDownloadButton>button{{
    background:{P_WHITE}!important;color:{A_BLUE}!important;
    border:1.5px solid {A_BLUE}!important;border-radius:7px!important;
    font-size:12px!important;font-weight:600!important;padding:7px 18px!important;
    transition:all 0.15s!important;
}}
.stDownloadButton>button:hover{{
    background:{A_BLUE}!important;color:{P_WHITE}!important;
}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# PLOTLY BASE
# ═══════════════════════════════════════
ANIM = dict(duration=400, easing="cubic-in-out")
BASE = dict(
    font=dict(family="DM Sans, sans-serif", size=12, color=P_MED),
    plot_bgcolor=P_WHITE, paper_bgcolor=P_WHITE,
    margin=dict(l=10, r=10, t=30, b=8),
    legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=P_BORDER, borderwidth=1,
                font=dict(size=11, color=P_MED),
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False, zeroline=False, linecolor=P_BORDER,
               tickfont=dict(size=10, color=P_MUTED), tickangle=-35,
               linewidth=1, showline=True),
    yaxis=dict(gridcolor="#F1F5F9", gridwidth=1, zeroline=False,
               linecolor=P_BORDER, tickfont=dict(size=10, color=P_MUTED),
               showline=True, linewidth=1),
    hoverlabel=dict(bgcolor=P_WHITE, bordercolor=P_BORDER,
                    font=dict(size=12, color=P_DARK, family="DM Sans")),
    transition=ANIM,
)

def mkf(h=280, specs=None, rows=1, cols=1, **kw):
    f = make_subplots(rows=rows, cols=cols, specs=specs) if (specs or rows>1) else go.Figure()
    lay = {**BASE, "height": h}; lay.update(kw); f.update_layout(**lay)
    return f

def zl(f, row=None, col=None):
    kw = dict(y=0, line_dash="dash", line_color=P_BORDER, line_width=1.5)
    if row: kw.update(row=row, col=col)
    f.add_hline(**kw)

def bc(s, p=CH["blue"], n=CH["red"]):
    return [n if v<0 else p for v in s.fillna(0)]

def ht(name, clr=CH["blue"], unit="mln $"):
    return (f"<b style='color:{P_DARK};'>{name}</b><br>"
            f"<span style='color:{P_MUTED};font-size:11px;'>%{{x}}</span><br>"
            f"<b style='color:{clr};font-family:DM Mono;font-size:14px;'>%{{y:,.1f}}</b>"
            f"<span style='color:{P_MUTED};font-size:10px;'> {unit}</span><extra></extra>")

def atr(f, x, y, name, clr, alpha=0.08, dash="solid", w=2.2, row=None, col=None):
    r_,g_,b_=int(clr[1:3],16),int(clr[3:5],16),int(clr[5:7],16)
    kw=dict(x=x,y=y,name=name,mode="lines",
            line=dict(color=clr,width=w,dash=dash,shape="spline",smoothing=0.8),
            fill="tozeroy",fillcolor=f"rgba({r_},{g_},{b_},{alpha})",
            hovertemplate=ht(name,clr))
    if row: kw.update(row=row,col=col)
    f.add_trace(go.Scatter(**kw))

def ltr(f, x, y, name, clr, dash="solid", w=2, row=None, col=None, mk=False):
    kw=dict(x=x,y=y,name=name,mode="lines"+("+markers" if mk else ""),
            line=dict(color=clr,width=w,dash=dash,shape="spline",smoothing=0.8),
            hovertemplate=ht(name,clr))
    if mk: kw["marker"]=dict(size=4,color=clr)
    if row: kw.update(row=row,col=col)
    f.add_trace(go.Scatter(**kw))

def btr(f, x, y, name, clr, op=0.85, row=None, col=None):
    kw=dict(x=x,y=y,name=name,
            marker=dict(color=clr,line=dict(color=P_WHITE,width=0.5),opacity=op,cornerradius=3),
            hovertemplate=ht(name,clr))
    if row: kw.update(row=row,col=col)
    f.add_trace(go.Bar(**kw))

def pch(f, key):
    st.plotly_chart(f, use_container_width=True, key=key)

def chart(title, sub=""):
    sub_html = f"<div class='gchart-sub'>{sub}</div>" if sub else "<div style='margin-bottom:14px;'></div>"
    st.markdown(f"<div class='gchart-title'>{title}</div>{sub_html}", unsafe_allow_html=True)

# ═══════════════════════════════════════
# DATA
# ═══════════════════════════════════════
EXCEL = "4-BOP_UZB-_Latin_analiticheskoe-predstavlenie_-4-kv.-2025g..xlsx"

@st.cache_data
def load():
    raw=pd.read_excel(EXCEL,sheet_name="Dataset",header=0,index_col=0)
    df=raw.T.copy(); df.index.name="Chorak"; df.reset_index(inplace=True)
    seen,cols={},[]
    for c in df.columns:
        c=str(c).strip(); seen[c]=seen.get(c,0)+1
        cols.append(f"{c}__2" if seen[c]>1 else c)
    df.columns=cols
    df["Chorak"]=df["Chorak"].str.replace(r"\s*chorak","",regex=True).str.strip()
    df["Yil"]=df["Chorak"].str.extract(r"(\d{4})").astype(int)
    for c in df.columns:
        if c not in("Chorak","Yil") and isinstance(df[c],pd.Series):
            df[c]=pd.to_numeric(df[c],errors="coerce")
    return df

@st.cache_data
def fc(_df, kw):
    for c in _df.columns:
        if kw.lower() in c.lower(): return c
    return None

@st.cache_data
def ann(_df):
    nc=[c for c in _df.columns if c not in("Chorak","Yil") and isinstance(_df[c],pd.Series)]
    y=_df.groupby("Yil")[nc].sum().reset_index()
    y["Chorak"]=y["Yil"].astype(str)
    return y

try:
    df=load()
except FileNotFoundError:
    st.error(f"Fayl topilmadi: **{EXCEL}**"); st.stop()

K={
    "joriy":fc(df,"Joriy operatsiyalar hisobi saldosi"),
    "eks_t":fc(df,"Tovarlar, kredit"),
    "imp_t":fc(df,"Tovarlar, debet"),
    "eks_x":fc(df,"Xizmatlar, kredit"),
    "imp_x":fc(df,"Xizmatlar, debet"),
    "bk":fc(df,"Birlamchi daromadlar, kredit"),
    "bd":fc(df,"Birlamchi daromadlar, debet"),
    "ik":fc(df,"Ikkilamchi daromadlar, kredit"),
    "id":fc(df,"Ikkilamchi daromadlar, debet"),
    "mol":fc(df,"Moliyaviy hisob"),
    "tdi_a":fc(df,"To'g'ridan-to'g'ri investitsiyalar, aktivlar"),
    "tdi_m":fc(df,"To'g'ridan-to'g'ri investitsiyalar, majburiyatlar"),
    "pa":fc(df,"Portfel investitsiyalar, aktivlar"),
    "pm":fc(df,"Portfel investitsiyalar, majburiyatlar"),
    "ba":fc(df,"Boshqa investitsiyalar, aktivlar"),
    "bm":fc(df,"Boshqa investitsiyalar, majburiyatlar"),
    "sof":fc(df,"Sof xatolar"),
    "uum":fc(df,"Umumiy balans"),
    "zax":fc(df,"Zaxira aktivlari"),
}
df["_eks"]=df[K["eks_t"]].fillna(0)+df[K["eks_x"]].fillna(0)
df["_imp"]=df[K["imp_t"]].fillna(0)+df[K["imp_x"]].fillna(0)
df["_net"]=df["_eks"]-df["_imp"]
df_y=ann(df)
df_y["_eks"]=df_y[K["eks_t"]].fillna(0)+df_y[K["eks_x"]].fillna(0)
df_y["_imp"]=df_y[K["imp_t"]].fillna(0)+df_y[K["imp_x"]].fillna(0)
df_y["_net"]=df_y["_eks"]-df_y["_imp"]
ALL_YEARS=sorted(df["Yil"].unique())

# ═══════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    if "lang" not in st.session_state: st.session_state.lang="uz"
    L=T[st.session_state.lang]

    # Logo
    _name={"uz":"O'zbekiston","en":"Uzbekistan","ru":"Узбекистан"}[st.session_state.lang]
    _bank={"uz":"Markaziy bank","en":"Central Bank","ru":"Центральный банк"}[st.session_state.lang]

    st.markdown(f"""
    <div style="padding:20px 16px 16px;border-bottom:1px solid {P_SIDEB};">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
        <span style="font-size:28px;line-height:1;">🇺🇿</span>
        <div>
          <div style="font-size:14px;font-weight:700;color:#F1F5F9;letter-spacing:-0.3px;">{_name}</div>
          <div style="font-size:10px;color:#475569;margin-top:1px;">{_bank}</div>
        </div>
      </div>
      <div style="background:rgba(37,99,235,0.12);border:1px solid rgba(37,99,235,0.2);
                  border-radius:6px;padding:8px 10px;">
        <div style="font-size:9px;color:#60A5FA;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;">
          BOP · IMF BPM6
        </div>
        <div style="font-size:11px;color:#94A3B8;margin-top:2px;">
          {ALL_YEARS[0]}–{ALL_YEARS[-1]} · {len(df)} {L['qtrs']}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Til
    st.markdown(f"""<div style="padding:12px 16px 8px;">
      <div style="font-size:9px;font-weight:700;color:#475569;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px;">{L['lang_lbl']}</div>
    </div>""", unsafe_allow_html=True)
    l1,l2,l3=st.columns(3)
    with l1:
        if st.button("UZ",use_container_width=True,
                     type="primary" if st.session_state.lang=="uz" else "secondary"):
            st.session_state.lang="uz"; st.rerun()
    with l2:
        if st.button("EN",use_container_width=True,
                     type="primary" if st.session_state.lang=="en" else "secondary"):
            st.session_state.lang="en"; st.rerun()
    with l3:
        if st.button("RU",use_container_width=True,
                     type="primary" if st.session_state.lang=="ru" else "secondary"):
            st.session_state.lang="ru"; st.rerun()

    # Har safar tilni qayta yuklash
    L=T[st.session_state.lang]

    # Ma'lumot turi
    st.markdown(f"""<div style="padding:12px 16px 8px;border-top:1px solid {P_SIDEB};margin-top:6px;">
      <div style="font-size:9px;font-weight:700;color:#475569;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px;">{L['dtype_lbl']}</div>
    </div>""", unsafe_allow_html=True)
    mode_opts=[L["quarterly"],L["annual"]]
    mode=st.radio("",mode_opts,horizontal=True,label_visibility="collapsed")

    # Yil oralig'i
    st.markdown(f"""<div style="padding:12px 16px 8px;border-top:1px solid {P_SIDEB};margin-top:2px;">
      <div style="font-size:9px;font-weight:700;color:#475569;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px;">{L['yr_range']}</div>
    </div>""", unsafe_allow_html=True)

    y1,y2=st.columns(2)
    if mode==L["annual"]:
        with y1:
            st.markdown(f"<div style='font-size:10px;color:#475569;font-weight:600;margin-bottom:3px;'>{L['yr_from']}</div>",unsafe_allow_html=True)
            y_from=st.selectbox("",ALL_YEARS,index=0,key="yfa",label_visibility="collapsed")
        with y2:
            st.markdown(f"<div style='font-size:10px;color:#475569;font-weight:600;margin-bottom:3px;'>{L['yr_to']}</div>",unsafe_allow_html=True)
            y_to=st.selectbox("",ALL_YEARS,index=len(ALL_YEARS)-1,key="yta",label_visibility="collapsed")
        if y_from>y_to: y_from,y_to=y_to,y_from
        sel_years=[y for y in ALL_YEARS if y_from<=y<=y_to]
        if not sel_years: sel_years=ALL_YEARS
        focus_year=L["all_"]
    else:
        with y1:
            st.markdown(f"<div style='font-size:10px;color:#475569;font-weight:600;margin-bottom:3px;'>{L['yr_from']}</div>",unsafe_allow_html=True)
            y_from=st.selectbox("",ALL_YEARS,index=max(0,len(ALL_YEARS)-12),key="yfq",label_visibility="collapsed")
        with y2:
            st.markdown(f"<div style='font-size:10px;color:#475569;font-weight:600;margin-bottom:3px;'>{L['yr_to']}</div>",unsafe_allow_html=True)
            y_to=st.selectbox("",ALL_YEARS,index=len(ALL_YEARS)-1,key="ytq",label_visibility="collapsed")
        if y_from>y_to: y_from,y_to=y_to,y_from
        st.markdown(f"<div style='font-size:10px;color:#475569;font-weight:600;margin-top:8px;margin-bottom:3px;'>{L['focus']}</div>",unsafe_allow_html=True)
        focus_year=st.selectbox("",[L["all_"]]+[str(y) for y in ALL_YEARS],key="focq",label_visibility="collapsed")
        sel_years=ALL_YEARS

    # Bo'limlar
    st.markdown(f"""<div style="padding:12px 16px 8px;border-top:1px solid {P_SIDEB};margin-top:4px;">
      <div style="font-size:9px;font-weight:700;color:#475569;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px;">{L['sections']}</div>
    </div>""", unsafe_allow_html=True)
    sh_ca  = st.checkbox(L["p_ca"],  True)
    sh_tr  = st.checkbox(L["p_tr"],  True)
    sh_fi  = st.checkbox(L["p_fi"],  True)
    sh_res = st.checkbox(L["p_re"],  True)
    sh_an  = st.checkbox(L["p_an"],  True)

    # Info
    st.markdown(f"""
    <div style="padding:14px 16px;border-top:1px solid {P_SIDEB};margin-top:6px;">
      <div style="font-size:10px;color:#334155;line-height:1.8;">
        <span style="color:#475569;font-weight:600;">{L['updated']}:</span><br>
        <span style="color:#64748B;">{datetime.date.today().strftime('%d.%m.%Y')}</span>
      </div>
      <div style="font-size:10px;color:#334155;margin-top:6px;line-height:1.6;">{L['source']}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════
# FILTER
# ═══════════════════════════════════════
is_ann=(mode==L["annual"])
if is_ann:
    dff=df_y[df_y["Yil"].isin(sel_years)].copy(); xl="Yil"
    plbl=f"{min(sel_years)}–{max(sel_years)}" if sel_years else "—"
else:
    if focus_year!=L["all_"]:
        dff=df[df["Yil"]==int(focus_year)].copy(); plbl=str(focus_year)
    else:
        dff=df[(df["Yil"]>=y_from)&(df["Yil"]<=y_to)].copy(); plbl=f"{y_from}–{y_to}"
    xl="Chorak"

def g(key):
    c=K.get(key)
    if c and c in dff.columns and isinstance(dff[c],pd.Series): return dff[c].fillna(0)
    return pd.Series(0.0,index=dff.index)
def gx(col):
    return dff[col].fillna(0) if col in dff.columns else pd.Series(0.0,index=dff.index)

xv=dff[xl]; jv=g("joriy"); eks=gx("_eks"); imp=gx("_imp"); net=gx("_net")
last_j=float(jv.iloc[-1]) if len(jv) else 0
prev_j=float(jv.iloc[-2]) if len(jv)>1 else last_j
last_ek=float(eks.iloc[-1]) if len(eks) else 0
last_im=float(imp.iloc[-1]) if len(imp) else 0
net_sum=net.sum()
cov=(eks/imp.replace(0,np.nan)*100).round(1)
clr_j=A_GREEN if last_j>=0 else A_RED
sgn_j="+" if last_j>=0 else ""

def yoy(s):
    return s.pct_change(4 if not is_ann else 1).mul(100).round(1)

# ═══════════════════════════════════════
# HEADER — toza, sodda
# ═══════════════════════════════════════
st.markdown(f"""
<div style="background:{P_WHITE};border-bottom:1px solid {P_BORDER};padding:18px 28px;">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div style="font-size:11px;font-weight:600;color:{P_MUTED};letter-spacing:1.2px;
                  text-transform:uppercase;margin-bottom:4px;">
        {L['country']} · {L['method']}
      </div>
      <div style="font-size:24px;font-weight:700;color:{P_DARK};letter-spacing:-0.5px;">
        {L['title']}
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:32px;">
      <div style="text-align:right;border-right:1px solid {P_BORDER};padding-right:28px;">
        <div style="font-size:10px;font-weight:600;color:{P_MUTED};text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;">{L['k_ca']}</div>
        <div style="font-size:22px;font-weight:700;color:{clr_j};font-family:'DM Mono',monospace;letter-spacing:-0.5px;">
          {sgn_j}{last_j:,.1f} <span style="font-size:12px;color:{P_MUTED};font-weight:400;">{L['mln']}</span>
        </div>
        <div style="font-size:10px;color:{P_MUTED};margin-top:2px;">{plbl} · {L['latest']}</div>
      </div>
      <div style="text-align:right;border-right:1px solid {P_BORDER};padding-right:28px;">
        <div style="font-size:10px;font-weight:600;color:{P_MUTED};text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;">{L['k_ex']}</div>
        <div style="font-size:22px;font-weight:700;color:{A_BLUE};font-family:'DM Mono',monospace;letter-spacing:-0.5px;">
          {last_ek:,.1f} <span style="font-size:12px;color:{P_MUTED};font-weight:400;">{L['mln']}</span>
        </div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:10px;font-weight:600;color:{P_MUTED};text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;">{L['k_im']}</div>
        <div style="font-size:22px;font-weight:700;color:{A_AMBER};font-family:'DM Mono',monospace;letter-spacing:-0.5px;">
          {last_im:,.1f} <span style="font-size:12px;color:{P_MUTED};font-weight:400;">{L['mln']}</span>
        </div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI qatorlari
st.markdown(f"<div style='padding:16px 28px 0;background:{P_BG};'>", unsafe_allow_html=True)
k1,k2,k3,k4,k5,k6=st.columns(6)
net_d=L["surplus"] if net_sum>=0 else L["deficit"]
with k1: st.metric(L["k_ca"],f"{last_j:,.1f}",delta=f"{last_j-prev_j:+,.1f}")
with k2: st.metric(L["k_ex"],f"{eks.sum():,.1f} {L['mln']}")
with k3: st.metric(L["k_im"],f"{imp.sum():,.1f} {L['mln']}")
with k4: st.metric(L["k_tr"],f"{net_sum:,.1f} {L['mln']}",delta=net_d)
with k5: st.metric(L["k_res"],f"{g('zax').sum():,.1f} {L['mln']}")
with k6: st.metric(L["k_fi"],f"{g('mol').sum():,.1f} {L['mln']}")

# ═══════════════════════════════════════
# TABS
# ═══════════════════════════════════════
st.markdown(f"<div style='padding:0 28px;'>",unsafe_allow_html=True)
t1,t2,t3,t4,t5,t6=st.tabs([L["t1"],L["t2"],L["t3"],L["t4"],L["t5"],L["t6"]])

# ── TAB 1 ─────────────────────────────
with t1:
    st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
    r1,r2,r3=st.columns(3)
    with r1:
        chart(L["g_ca"],f"{plbl} · {L['mln']}")
        f1=mkf(200)
        f1.add_trace(go.Scatter(x=xv,y=jv.clip(lower=0),mode="none",fill="tozeroy",fillcolor="rgba(22,163,74,0.07)",showlegend=False))
        f1.add_trace(go.Scatter(x=xv,y=jv.clip(upper=0),mode="none",fill="tozeroy",fillcolor="rgba(220,38,38,0.07)",showlegend=False))
        atr(f1,xv,jv,L["k_ca"],CH["blue"],0.0,w=2)
        if len(jv)>=4: ltr(f1,xv,jv.rolling(4,min_periods=1).mean(),L["rolling"],CH["grey"],"dot",1.5)
        zl(f1); f1.update_layout(showlegend=True,yaxis_title=L["mln"])
        pch(f1,"t1_ca")

    with r2:
        chart(L["g_fi"],f"{plbl} · {L['mln']}")
        mv=g("mol"); f2=mkf(200)
        f2.add_trace(go.Scatter(x=xv,y=mv.clip(lower=0),mode="none",fill="tozeroy",fillcolor="rgba(8,145,178,0.07)",showlegend=False))
        f2.add_trace(go.Scatter(x=xv,y=mv.clip(upper=0),mode="none",fill="tozeroy",fillcolor="rgba(220,38,38,0.07)",showlegend=False))
        atr(f2,xv,mv,L["k_fi"],CH["teal"],0.0,w=2)
        zl(f2); f2.update_layout(showlegend=False,yaxis_title=L["mln"])
        pch(f2,"t1_fi")

    with r3:
        chart(L["g_res"],f"{plbl} · {L['mln']}")
        f3=mkf(200)
        atr(f3,xv,g("zax"),L["k_res"],CH["amber"],0.08,w=2)
        f3.update_layout(showlegend=False,yaxis_title=L["mln"])
        pch(f3,"t1_res")

    r4,r5=st.columns(2)
    with r4:
        chart(L["g_trade"],f"{plbl} · {L['mln']}")
        f4=mkf(240)
        atr(f4,xv,eks,L["k_ex"],CH["blue"],0.08)
        atr(f4,xv,imp,L["k_im"],CH["red"],0.08)
        f4.update_layout(yaxis_title=L["mln"]); pch(f4,"t1_trade")

    with r5:
        chart(L["g_allcomp"],f"{plbl} · {L['mln']}")
        f5=mkf(240)
        ltr(f5,xv,g("joriy"),L["k_ca"],CH["blue"],w=2.2,mk=True)
        ltr(f5,xv,g("mol"),L["k_fi"],CH["teal"],w=2,mk=True)
        ltr(f5,xv,g("sof"),L["c_err"],CH["grey"],"dot",1.5)
        ltr(f5,xv,g("uum"),L["c_ov"],CH["red"],w=2,mk=True)
        zl(f5); f5.update_layout(yaxis_title=L["mln"]); pch(f5,"t1_comp")

    if not is_ann:
        chart(L["g_annual"],f"{plbl} · {L['mln']}")
        ym=(df_y["Yil"]>=(y_from if focus_year==L["all_"] else int(focus_year)))&\
           (df_y["Yil"]<=(y_to if focus_year==L["all_"] else int(focus_year)))
        ydf=df_y[ym]
        def yg(key):
            c=K.get(key)
            if c and c in ydf.columns: return ydf[c].fillna(0)
            return pd.Series(0.0,index=ydf.index)
        f6=mkf(240)
        btr(f6,ydf["Yil"],yg("joriy"),L["k_ca"],CH["blue"])
        btr(f6,ydf["Yil"],yg("mol"),L["k_fi"],CH["teal"])
        btr(f6,ydf["Yil"],yg("uum"),L["c_ov"],CH["red"])
        zl(f6); f6.update_layout(barmode="group",bargap=0.22,yaxis_title=L["mln"])
        pch(f6,"t1_annual")

# ── TAB 2 ─────────────────────────────
with t2:
    if sh_ca or sh_tr:
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        r1,r2=st.columns(2)
        with r1:
            chart(L["g_trade"])
            fa=mkf(260); atr(fa,xv,eks,L["k_ex"],CH["blue"],0.09); atr(fa,xv,imp,L["k_im"],CH["red"],0.09)
            fa.update_layout(yaxis_title=L["mln"]); pch(fa,"ca_ei")
        with r2:
            chart(L["g_net"])
            nv=net; fw=mkf(260)
            fw.add_trace(go.Waterfall(x=xv,y=nv,measure=["relative"]*len(nv),
                connector=dict(line=dict(color=P_BORDER,width=1)),
                increasing=dict(marker_color=CH["green"]),
                decreasing=dict(marker_color=CH["red"]),
                hovertemplate=ht(L["k_tr"],CH["blue"])))
            zl(fw); fw.update_layout(showlegend=False,yaxis_title=L["mln"]); pch(fw,"ca_wf")

        r3,r4=st.columns(2)
        with r3:
            chart(L["g_ex_str"])
            fb=mkf(250)
            btr(fb,xv,g("eks_t"),L["c_exg"],CH["blue"],0.9)
            btr(fb,xv,g("eks_x"),L["c_exs"],CH["lblue"],0.9)
            fb.update_layout(barmode="stack",bargap=0.08,yaxis_title=L["mln"]); pch(fb,"ca_exs")
        with r4:
            chart(L["g_im_str"])
            fc_=mkf(250)
            btr(fc_,xv,g("imp_t"),L["c_img"],CH["red"],0.9)
            btr(fc_,xv,g("imp_x"),L["c_ims"],CH["amber"],0.9)
            fc_.update_layout(barmode="stack",bargap=0.08,yaxis_title=L["mln"]); pch(fc_,"ca_ims")

        r5,r6=st.columns(2)
        with r5:
            chart(L["g_cov"])
            fc2=mkf(240)
            fc2.add_trace(go.Scatter(x=xv,y=cov,name=L["cov_lbl"],
                mode="lines+markers",
                line=dict(color=CH["teal"],width=2,shape="spline",smoothing=0.8),
                marker=dict(size=4,color=[A_GREEN if v>=100 else A_RED for v in cov.fillna(0)],
                            line=dict(color=P_WHITE,width=1)),
                fill="tozeroy",fillcolor="rgba(8,145,178,0.06)",
                hovertemplate=f"<b>{L['cov_lbl']}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"))
            fc2.add_hline(y=100,line_dash="dash",line_color=A_AMBER,line_width=1.8,
                annotation_text=L["threshold"],annotation_position="right",
                annotation_font=dict(size=9,color=A_AMBER))
            fc2.update_layout(showlegend=False,yaxis_title="%"); pch(fc2,"ca_cov")
        with r6:
            chart(L["g_income"])
            fd=mkf(240)
            ltr(fd,xv,g("bk"),L["c_p1"],CH["blue"],"solid",2,mk=True)
            ltr(fd,xv,g("bd"),L["c_p2"],CH["red"],"dash",2)
            ltr(fd,xv,g("ik"),L["c_s1"],CH["teal"],"solid",2,mk=True)
            ltr(fd,xv,g("id"),L["c_s2"],CH["amber"],"dash",2)
            fd.update_layout(yaxis_title=L["mln"]); pch(fd,"ca_inc")

# ── TAB 3 ─────────────────────────────
with t3:
    if sh_fi:
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        chart(L["g_fi"])
        mv2=g("mol"); fe=mkf(240)
        fe.add_trace(go.Scatter(x=xv,y=mv2.clip(lower=0),mode="none",fill="tozeroy",fillcolor="rgba(8,145,178,0.07)",showlegend=False))
        fe.add_trace(go.Scatter(x=xv,y=mv2.clip(upper=0),mode="none",fill="tozeroy",fillcolor="rgba(220,38,38,0.07)",showlegend=False))
        atr(fe,xv,mv2,L["k_fi"],CH["teal"],0.0,w=2)
        zl(fe); fe.update_layout(showlegend=False,yaxis_title=L["mln"]); pch(fe,"fi_tot")

        c1,c2,c3=st.columns(3)
        with c1:
            chart(L["g_fdi"]); ff1=mkf(240)
            btr(ff1,xv,g("tdi_a"),L["assets"],CH["blue"],0.9)
            btr(ff1,xv,g("tdi_m"),L["liab"],CH["teal"],0.9)
            zl(ff1); ff1.update_layout(barmode="group",bargap=0.18,yaxis_title=L["mln"]); pch(ff1,"fi_fdi")
        with c2:
            chart(L["g_port"]); ff2=mkf(240)
            btr(ff2,xv,g("pa"),L["assets"],CH["purple"],0.9)
            btr(ff2,xv,g("pm"),L["liab"],CH["amber"],0.9)
            zl(ff2); ff2.update_layout(barmode="group",bargap=0.18,yaxis_title=L["mln"]); pch(ff2,"fi_port")
        with c3:
            chart(L["g_other"]); ff3=mkf(240)
            ltr(ff3,xv,g("ba"),L["assets"],CH["green"],"solid",2,mk=True)
            ltr(ff3,xv,g("bm"),L["liab"],CH["red"],"dash",2)
            zl(ff3); ff3.update_layout(yaxis_title=L["mln"]); pch(ff3,"fi_oth")

        chart(L["g_netfl"]); fg2=mkf(240)
        atr(fg2,xv,g("tdi_a")-g("tdi_m"),L["net_fdi"],CH["blue"],0.08,w=2)
        atr(fg2,xv,g("pa")-g("pm"),L["net_port"],CH["purple"],0.08,w=2)
        atr(fg2,xv,g("ba")-g("bm"),L["net_oth"],CH["amber"],0.06,"dash",1.8)
        zl(fg2); fg2.update_layout(yaxis_title=L["mln"]); pch(fg2,"fi_net")

        chart(L["g_fistack"]); fs=mkf(240)
        for col,name,clr,fc_ in [
            ("tdi_m",L["tdi_in"],CH["blue"],FILLS[CH["blue"]]),
            ("pm",L["port_in"],CH["teal"],FILLS[CH["teal"]]),
            ("bm",L["oth_in"],CH["green"],FILLS[CH["green"]]),
        ]:
            fs.add_trace(go.Scatter(x=xv,y=g(col),name=name,mode="lines",
                stackgroup="one",line=dict(color=clr,width=1),fillcolor=fc_,
                hovertemplate=ht(name,clr)))
        fs.update_layout(yaxis_title=L["mln"]); pch(fs,"fi_stack")

# ── TAB 4 ─────────────────────────────
with t4:
    if sh_res:
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        chart(L["g_bal"])
        fgg=mkf(300,specs=[[{"secondary_y":True}]])
        uu=g("uum")
        fgg.add_trace(go.Bar(x=xv,y=uu,
            marker=dict(color=bc(uu,CH["blue"],CH["red"]),
                        line=dict(color=P_WHITE,width=0.5),opacity=0.85,cornerradius=3),
            name=L["c_ov"],hovertemplate=ht(L["c_ov"])),secondary_y=False)
        fgg.add_trace(go.Scatter(x=xv,y=g("zax"),mode="lines",name=L["k_res"],
            line=dict(color=CH["amber"],width=2.2,shape="spline",smoothing=0.8),
            hovertemplate=ht(L["k_res"],CH["amber"])),secondary_y=True)
        zl(fgg)
        fgg.update_layout(**{**BASE,"height":300})
        fgg.update_yaxes(title_text=f"{L['c_ov']}, {L['mln']}",gridcolor="#F1F5F9",tickfont=dict(color=P_MUTED,size=10),secondary_y=False)
        fgg.update_yaxes(title_text=f"{L['k_res']}, {L['mln']}",showgrid=False,tickfont=dict(color=P_MUTED,size=10),secondary_y=True)
        pch(fgg,"res_dual")

        rc1,rc2=st.columns([3,2])
        with rc1:
            chart(L["g_err"]); sv=g("sof"); fh=mkf(260)
            fh.add_trace(go.Bar(x=xv,y=sv,
                marker=dict(color=bc(sv,CH["teal"],CH["amber"]),
                            line=dict(color=P_WHITE,width=0.5),opacity=0.88,cornerradius=3),
                hovertemplate=ht(L["c_err"],CH["teal"])))
            zl(fh); fh.update_layout(showlegend=False,yaxis_title=L["mln"]); pch(fh,"res_err")
        with rc2:
            chart(L["g_cum"]); fi=mkf(260)
            atr(fi,xv,g("zax").cumsum(),L["cumul"],CH["amber"],0.08,w=2)
            fi.update_layout(showlegend=False,yaxis_title=L["mln"]); pch(fi,"res_cum")

# ── TAB 5 ─────────────────────────────
with t5:
    if sh_an:
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        chart(L["g_yoy"])
        ye=yoy(eks); yi=yoy(imp); fa1=mkf(260)
        fa1.add_trace(go.Bar(x=xv,y=ye,name=L["k_ex"],
            marker=dict(color=[CH["green"] if v>=0 else CH["red"] for v in ye.fillna(0)],opacity=0.85,cornerradius=3),
            hovertemplate=f"<b>{L['k_ex']}</b><br>%{{x}}<br>%{{y:+.1f}}%<extra></extra>"))
        fa1.add_trace(go.Bar(x=xv,y=yi,name=L["k_im"],
            marker=dict(color=[CH["amber"] if v>=0 else CH["purple"] for v in yi.fillna(0)],opacity=0.7,cornerradius=3),
            hovertemplate=f"<b>{L['k_im']}</b><br>%{{x}}<br>%{{y:+.1f}}%<extra></extra>"))
        zl(fa1); fa1.update_layout(barmode="group",bargap=0.18,yaxis_title="%"); pch(fa1,"an_yoy")

        r1,r2=st.columns(2)
        with r1:
            chart(L["g_scatter"])
            fa2=go.Figure()
            fa2.add_trace(go.Scatter(x=eks,y=jv,mode="markers+text",
                marker=dict(size=9,color=CH["blue"],opacity=0.72,line=dict(color=P_WHITE,width=1.5)),
                text=xv.astype(str),textposition="top right",textfont=dict(size=8,color=P_MUTED),
                hovertemplate=f"<b>%{{text}}</b><br>{L['k_ex']}: %{{x:,.0f}}<br>{L['k_ca']}: %{{y:,.0f}}<extra></extra>",
                name="",showlegend=False))
            if len(eks)>3:
                valid=eks.dropna()
                z=np.polyfit(valid,jv.loc[valid.index],1); p=np.poly1d(z)
                x_line=np.linspace(valid.min(),valid.max(),50)
                fa2.add_trace(go.Scatter(x=x_line,y=p(x_line),mode="lines",
                    line=dict(color=A_RED,width=1.5,dash="dot"),name=L["trend"]))
            fa2.update_layout(**{**BASE,"height":280,
                "xaxis_title":f"{L['k_ex']}, {L['mln']}",
                "yaxis_title":f"{L['k_ca']}, {L['mln']}"})
            pch(fa2,"an_scat")

        with r2:
            chart(L["g_hist"])
            fa3=make_subplots(rows=2,cols=1,row_heights=[0.65,0.35],shared_xaxes=True,vertical_spacing=0.04)
            fa3.add_trace(go.Histogram(x=net,nbinsx=20,
                marker=dict(color=CH["blue"],opacity=0.8,line=dict(color=P_WHITE,width=0.5)),
                name=L["distrib"],hovertemplate=f"%{{x:,.0f}}: %{{y}}<extra></extra>"),row=1,col=1)
            fa3.add_trace(go.Box(x=net,marker=dict(color=P_DARK,size=4),
                line=dict(color=P_DARK,width=1.5),fillcolor="rgba(15,23,42,0.07)",
                boxmean=True,name=L["boxlbl"],hovertemplate=f"%{{x:,.0f}}<extra></extra>"),row=2,col=1)
            fa3.update_layout(**{**BASE,"height":280,"showlegend":False})
            fa3.update_xaxes(showgrid=False); fa3.update_yaxes(gridcolor="#F1F5F9",row=1,col=1)
            pch(fa3,"an_hist")

        if not is_ann and len(df)>4:
            chart(L["g_heatmap"])
            hdf=df[(df["Yil"]>=y_from)&(df["Yil"]<=y_to)].copy()
            hdf["Qn"]=hdf["Chorak"].str.extract(r"-(\w+)$")[0]
            jc=K["joriy"]
            if jc and jc in hdf.columns:
                pivot=hdf.pivot_table(values=jc,index="Yil",columns="Qn",aggfunc="sum")
                fhm=go.Figure(go.Heatmap(
                    z=pivot.values,x=pivot.columns.tolist(),y=pivot.index.tolist(),
                    colorscale=[[0,CH["red"]],[0.5,"#F8F9FC"],[1,CH["blue"]]],zmid=0,
                    text=[[f"{v:,.0f}" for v in row] for row in pivot.values],
                    texttemplate="%{text}",textfont=dict(size=10,color=P_DARK),
                    colorbar=dict(title=L["mln"],thickness=12,tickfont=dict(size=10,color=P_MUTED)),
                    hovertemplate=f"%{{y}} · %{{x}}<br>%{{z:,.0f}} {L['mln']}<extra></extra>"))
                fhm.update_layout(**{**BASE,"height":300}); pch(fhm,"an_hm")

        chart(L["g_funnel"])
        ff=go.Figure(go.Funnel(
            y=[L["k_ca"],L["k_fi"],L["k_res"],L["c_err"]],
            x=[abs(g(k).sum()) for k in("joriy","mol","zax","sof")],
            textinfo="value+percent initial",textfont=dict(size=12,color=P_DARK,family="DM Sans"),
            marker=dict(color=[CH["blue"],CH["teal"],CH["amber"],CH["grey"]],
                        line=dict(color=P_WHITE,width=1.5)),
            connector=dict(line=dict(color=P_BORDER,dash="dot",width=1)),
            hovertemplate=f"<b>%{{y}}</b><br>%{{x:,.0f}} {L['mln']}<extra></extra>"))
        ff.update_layout(**{**BASE,"height":280,"margin":dict(l=160,r=80,t=20,b=10),
            "yaxis":dict(showgrid=False),"xaxis":dict(showgrid=False,title=L["mln"])})
        pch(ff,"an_fun")

# ── TAB 6 ─────────────────────────────
with t6:
    st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
    _tbl_title={"uz":"Ma'lumotlar jadvali","en":"Data table","ru":"Таблица данных"}[st.session_state.lang]
    chart(_tbl_title,f"{plbl} · {L['mln']}")
    table=pd.DataFrame({
        L["c_period"]:xv.values, L["c_ca"]:g("joriy").values,
        L["c_ex"]:eks.values, L["c_im"]:imp.values, L["c_net"]:net.values,
        L["c_fi"]:g("mol").values, L["c_fdia"]:g("tdi_a").values,
        L["c_fdim"]:g("tdi_m").values, L["c_err"]:g("sof").values,
        L["c_ov"]:g("uum").values, L["c_re"]:g("zax").values,
        L["c_ratio"]:cov.values,
    })
    nc=[c for c in table.columns if c not in(L["c_period"],L["c_ratio"])]
    nc2=[L["c_ratio"]]
    def sc(v):
        if isinstance(v,(int,float)):
            if v<0: return f"background:#FEF2F2;color:{A_RED};font-weight:500"
            if v>0: return f"background:#F0FDF4;color:{A_GREEN};font-weight:500"
        return f"color:{P_DARK}"
    def sc2(v):
        if isinstance(v,(int,float)):
            return (f"background:#F0FDF4;color:{A_GREEN};font-weight:500" if v>=100
                    else f"background:#FEF2F2;color:{A_RED};font-weight:500")
        return f"color:{P_DARK}"
    styled=(table.style
        .map(sc,subset=nc).map(sc2,subset=nc2)
        .format({c:"{:,.1f}" for c in nc})
        .format({L["c_ratio"]:"{:.1f}%"})
        .set_properties(**{"font-size":"11px","font-family":"DM Mono,monospace",
                           "border":f"1px solid {P_BORDER}","text-align":"right"})
        .set_table_styles([
            {"selector":"th","props":[
                ("background","#F8F9FC"),("color",A_BLUE),("font-size","11px"),
                ("font-weight","700"),("text-transform","uppercase"),
                ("letter-spacing","0.5px"),("padding","10px 14px"),
                ("border-bottom",f"2px solid {P_BORDER}"),
                ("font-family","DM Sans,sans-serif"),
            ]},
            {"selector":"td","props":[("padding","8px 14px")]},
            {"selector":"tr:hover td","props":[("background","#F8F9FC")]},
        ]))
    st.dataframe(styled,use_container_width=True,height=520)
    d1,d2,_=st.columns([1,1,5])
    with d1:
        csv=table.to_csv(index=False).encode("utf-8")
        st.download_button(f"⬇ {L['dl_csv']}",csv,
            file_name=f"bop_{mode.lower()}.csv",mime="text/csv")
    with d2:
        buf=io.BytesIO()
        with pd.ExcelWriter(buf,engine="openpyxl") as w: table.to_excel(w,index=False,sheet_name="BOP")
        buf.seek(0)
        st.download_button(f"⬇ {L['dl_xl']}",buf.getvalue(),
            file_name=f"bop_{mode.lower()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("</div>",unsafe_allow_html=True)

# ── FOOTER ──
st.markdown(f"""
<div style="background:{P_WHITE};border-top:1px solid {P_BORDER};padding:12px 28px;
     display:flex;justify-content:space-between;align-items:center;margin-top:20px;">
  <span style="font-size:11px;color:{P_MUTED};">{L['footer']}</span>
  <span style="font-size:11px;color:{P_BORDER};font-family:'DM Mono',monospace;">v10.0 · {plbl}</span>
</div>
""",unsafe_allow_html=True)
