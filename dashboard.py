"""
Dashboard Executivo — Gestão de Inventário SBF
Streamlit + Plotly | Design corporativo clean
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ── CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="SBF — Inventário",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── PALETA ──────────────────────────────────────
BG = "#0F1117"
BG_CARD = "#1A1D27"
BG_SURFACE = "#242733"
BORDA = "#2D3040"
TEXTO = "#EAEDF3"
TEXTO2 = "#A0A4B8"
VERDE = "#1B6B3A"
LIMA = "#7CCB5F"
VERDE_MEDIO = "#2B7A4B"
VERMELHO = "#EF4444"
AMARELO = "#F59E0B"
BRANCO = "#FFFFFF"

STATUS_COR = {"No Prazo": "#22C55E", "Atrasado": AMARELO, "Critico": VERMELHO}

# ── CSS ─────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp {{
    background: {BG};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: {TEXTO};
}}

/* Header */
.dash-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 0 20px 0;
    border-bottom: 1px solid {BORDA};
    margin-bottom: 24px;
}}
.dash-header .logo {{
    color: {LIMA};
    font-weight: 700;
    font-size: 1.1rem;
    background: {VERDE};
    padding: 6px 14px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}}
.dash-header .title {{
    font-size: 1.15rem;
    font-weight: 600;
    color: {TEXTO};
}}
.dash-header .badge {{
    margin-left: auto;
    color: {TEXTO2};
    font-size: 0.8rem;
}}

/* KPI */
.kpi {{
    background: {BG_CARD};
    border: 1px solid {BORDA};
    border-radius: 10px;
    padding: 20px;
}}
.kpi .val {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {BRANCO};
    line-height: 1.1;
    margin-bottom: 4px;
}}
.kpi .lbl {{
    font-size: 0.76rem;
    font-weight: 500;
    color: {TEXTO2};
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.kpi .dot {{
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-right: 5px;
    vertical-align: middle;
}}

/* Section */
.sec-title {{
    font-size: 1.0rem;
    font-weight: 600;
    color: {TEXTO};
    margin: 28px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid {BORDA};
}}

/* Cat card */
.cat-card {{
    background: {BG_CARD};
    border: 1px solid {BORDA};
    border-radius: 10px;
    padding: 16px 20px;
}}
.cat-card .name {{
    font-size: 0.95rem;
    font-weight: 600;
    color: {TEXTO};
    margin-bottom: 8px;
}}
.cat-card .stat {{
    font-size: 0.78rem;
    color: {TEXTO2};
    line-height: 1.6;
}}
.cat-card .pct {{
    font-size: 1.5rem;
    font-weight: 700;
    text-align: right;
}}

/* Insight */
.insight {{
    background: {BG_CARD};
    border: 1px solid {BORDA};
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: {TEXTO2};
    margin-bottom: 12px;
}}
.insight strong {{ color: {TEXTO}; }}

/* Executive insight block */
.exec-insight {{
    background: {BG_CARD};
    border: 1px solid {BORDA};
    border-left: 3px solid {LIMA};
    border-radius: 0 8px 8px 0;
    padding: 18px 22px;
    margin: 16px 0 28px 0;
    font-size: 0.92rem;
    line-height: 1.7;
    color: {TEXTO2};
}}
.exec-insight strong {{ color: {TEXTO}; }}
.exec-insight .ei-label {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: {LIMA};
    margin-bottom: 8px;
}}

/* Section subtitle = business question */
.sec-question {{
    font-size: 0.84rem;
    color: #B0B4C8;
    margin: -12px 0 14px 0;
    font-style: italic;
}}

/* Dark table */
.dark-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
    font-family: 'Inter', sans-serif;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid {BORDA};
}}
.dark-table thead th {{
    background: {BG_SURFACE};
    color: {TEXTO2};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    font-size: 0.73rem;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid {BORDA};
}}
.dark-table tbody td {{
    background: {BG_CARD};
    color: {TEXTO};
    padding: 9px 12px;
    border-bottom: 1px solid {BORDA};
}}
.dark-table tbody tr:last-child td {{
    border-bottom: none;
}}
.dark-table tbody tr:hover td {{
    background: {BG_SURFACE};
}}
.dark-table .row-danger td {{
    background: rgba(239, 68, 68, 0.08);
}}
.dark-table .row-warning td {{
    background: rgba(245, 158, 11, 0.06);
}}
.dark-table .text-right {{
    text-align: right;
}}

/* Scrollable table container */
.table-scroll {{
    max-height: 380px;
    overflow-y: auto;
    border-radius: 8px;
    border: 1px solid {BORDA};
}}
.table-scroll .dark-table {{
    border: none;
}}

/* Hide sidebar toggle and other Streamlit chrome */
div[data-testid="stSidebar"] {{ display: none; }}
header[data-testid="stHeader"] {{ background: {BG}; }}
.stDeployButton {{ display: none; }}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY DEFAULTS ─────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXTO2, family="Inter", size=12),
    margin=dict(t=36, b=30, l=50, r=20),
)

def ax(title="", **kw):
    return dict(showgrid=True, gridcolor="#252840", title=title, **kw)


def html_table(df, cols, headers=None, fmt=None, row_class_fn=None, max_height=None):
    """Render a pandas DataFrame as a dark-themed HTML table."""
    if headers is None:
        headers = cols
    if fmt is None:
        fmt = {}

    html = ""
    if max_height:
        html += f'<div class="table-scroll" style="max-height:{max_height}px">'
    html += '<table class="dark-table"><thead><tr>'
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        cls = row_class_fn(row) if row_class_fn else ""
        html += f'<tr class="{cls}">'
        for c in cols:
            val = row[c]
            if c in fmt:
                val = fmt[c](val)
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    if max_height:
        html += "</div>"
    return html


# ── LOAD DATA ───────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("dados-tratados.xlsx")
    if "Valor_Total_Estoque" not in df.columns:
        df["Valor_Total_Estoque"] = df["Estoque_Atual"] * df["Custo_Unitario"]
    df["Cobertura_Estoque_Dias"] = (df["Estoque_Atual"] / df["Venda_Media_Diaria"]).round(1)
    df["Abaixo_Minimo"] = df["Estoque_Atual"] < df["Estoque_Minimo"]
    df_s = df.sort_values("Valor_Total_Estoque", ascending=False)
    df_s["VTE_Acum"] = df_s["Valor_Total_Estoque"].cumsum()
    ids_top20 = df_s[df_s["VTE_Acum"] <= df_s["Valor_Total_Estoque"].sum() * 0.20]["ID_Produto"].tolist()
    df["Top_20_Valor"] = df["ID_Produto"].isin(ids_top20).map({True: "Sim", False: "Não"})
    df["Data_Prevista_Chegada"] = df["Data_Registro"] + pd.to_timedelta(df["Lead_Time_Fornecedor"], unit="D")
    df["Saudavel"] = (df["Estoque_Atual"] >= df["Estoque_Minimo"]) & (df["Status_Entrega"] == "No Prazo")
    return df

df = load_data()


# ── HEADER ──────────────────────────────────────
st.markdown(
    f'<div class="dash-header">'
    f'<span class="logo">SBF</span>'
    f'<span class="title">Dashboard de Inventário</span>'
    f'<span class="badge" title="Data/Hora da última extração da base do ERP">Atualizado em 12/03/2026 às 01:46</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── FILTERS (TOP BAR) ──────────────────────────
fc1, fc2, fc3 = st.columns([4, 4, 3])
with fc1:
    categorias = st.multiselect("Categoria", sorted(df["Categoria"].unique()), default=sorted(df["Categoria"].unique()))
with fc2:
    status_sel = st.multiselect("Status Entrega", sorted(df["Status_Entrega"].unique()), default=sorted(df["Status_Entrega"].unique()))

df_f = df[
    (df["Categoria"].isin(categorias)) &
    (df["Status_Entrega"].isin(status_sel))
]

with fc3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<span style="color:{TEXTO2};font-size:0.82rem;">Exibindo '
        f'<strong style="color:{TEXTO};">{len(df_f)}</strong> de {len(df)} produtos</span>',
        unsafe_allow_html=True,
    )


# ── KPIs ────────────────────────────────────────
ruptura = len(df_f[df_f["Abaixo_Minimo"]])
estoque_zero = len(df_f[df_f["Estoque_Atual"] == 0])
valor_total = df_f["Valor_Total_Estoque"].sum()
saude_pct = df_f["Saudavel"].sum() / max(len(df_f), 1) * 100
cob_media = df_f["Cobertura_Estoque_Dias"].mean()
cob_cor = VERMELHO if cob_media < 5 else (AMARELO if cob_media < 10 else "#22C55E")

def kpi(val, label, dot_color=None, tooltip=""):
    dot = f'<span class="dot" style="background:{dot_color}"></span>' if dot_color else ""
    return f'<div class="kpi" title="{tooltip}"><div class="val">{val}</div><div class="lbl">{dot}{label}</div></div>'

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(kpi(f"R$ {valor_total:,.0f}", "Valor Total em Estoque", tooltip="Soma de (Estoque Atual * Custo Unitário) dos itens filtrados"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi(str(ruptura), "Produtos em Ruptura", VERMELHO, tooltip="Itens onde o Estoque Atual está estritamente abaixo do Estoque Mínimo"), unsafe_allow_html=True)
with k3:
    st.markdown(kpi(str(estoque_zero), "Estoque Zerado", VERMELHO, tooltip="Itens com 0 unidades físicas disponíveis no momento da extração"), unsafe_allow_html=True)
with k4:
    st.markdown(kpi(f"{cob_media:.1f} dias", "Cobertura Média", cob_cor, tooltip="Média de dias que o estoque atual suporta considerando a Venda Média Diária (Top-Down)"), unsafe_allow_html=True)

# ── VALOR POR CATEGORIA + ESTOQUE vs MÍNIMO ────
st.markdown('<div class="sec-title">Distribuição de Capital por Categoria</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-question">Resumir o Valor Total em Estoque e a Venda Média por Categoria.</div>', unsafe_allow_html=True)

tabela_cat = df_f.groupby("Categoria").agg(
    Qtd_Produtos=("ID_Produto", "count"),
    Estoque_Total=("Estoque_Atual", "sum"),
    Custo_Medio=("Custo_Unitario", "mean"),
    Valor_Total=("Valor_Total_Estoque", "sum"),
    Venda_Media=("Venda_Media_Diaria", "mean"),
)
tabela_cat["Participação (%)"] = tabela_cat["Valor_Total"] / tabela_cat["Valor_Total"].sum() * 100

cat_estoque = df_f.groupby("Categoria").agg(
    Estoque_Atual=("Estoque_Atual", "sum"),
    Estoque_Minimo=("Estoque_Minimo", "sum"),
)

c2a, c2b = st.columns([1.3, 0.7])
with c2a:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tabela_cat.index, y=tabela_cat["Valor_Total"],
        name="Valor em Estoque (R$)", marker_color=LIMA,
        text=[f"R$ {v/1000:,.0f}k" for v in tabela_cat["Valor_Total"]],
        textposition="auto", textfont=dict(color=BRANCO, size=11), yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=tabela_cat.index, y=tabela_cat["Venda_Media"],
        name="Venda Média (Giro)", mode="lines+markers",
        line=dict(color=AMARELO, width=2),
        marker=dict(size=8, color=AMARELO), yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Venda Média: %{y:.1f}<extra></extra>"
    ))
    max_valor = tabela_cat["Valor_Total"].max()
    max_venda = tabela_cat["Venda_Media"].max()
    
    fig.update_layout(
        title=dict(text="Valor em Estoque vs Venda Média", font=dict(size=14, color=TEXTO2)),
        **PL, height=420,
        yaxis=dict(title="Valor Total (R$)", showgrid=True, gridcolor="#252840", range=[0, max_valor * 1.15]),
        yaxis2=dict(
            title=dict(text="Venda Média Diária", font=dict(color=AMARELO)), 
            overlaying="y", side="right", showgrid=False, tickfont=dict(color=AMARELO),
            range=[0, max_venda * 1.45]
        ),
        legend=dict(orientation="h", y=1.05, x=0, font=dict(size=11, color=TEXTO2))
    )
    st.plotly_chart(fig, use_container_width=True)

with c2b:
    st.markdown(html_table(
        tabela_cat.reset_index(),
        cols=["Categoria", "Valor_Total", "Venda_Media"],
        headers=["Categoria", "Valor Total (R$)", "Venda Média"],
        fmt={"Valor_Total": lambda v: f"R$ {v:,.0f}", "Venda_Media": lambda v: f"{v:.1f}"},
        max_height=380,
    ), unsafe_allow_html=True)

# Insight executivo — Capital por Categoria
cat_maior = tabela_cat["Valor_Total"].idxmax()
cat_maior_pct = tabela_cat.loc[cat_maior, "Participação (%)"]
cat_maior_venda = tabela_cat.loc[cat_maior, "Venda_Media"]
cat_menor_venda = tabela_cat["Venda_Media"].idxmin()
cat_deficit = cat_estoque[cat_estoque["Estoque_Atual"] < cat_estoque["Estoque_Minimo"]]

insight_capital = (
    f'<div class="exec-insight"><div class="ei-label">Resumo do Insight</div>'
    f'A categoria <strong>{cat_maior}</strong> concentra <strong>{cat_maior_pct:.0f}%</strong> '
    f'do capital investido em estoque (R$ {tabela_cat.loc[cat_maior, "Valor_Total"]:,.0f}). '
)
if len(cat_deficit) > 0:
    cats_list = cat_deficit.index.tolist()
    cats_str = ", ".join(cats_list)
    prefixo = "As categorias" if len(cats_list) > 1 else "A categoria"
    verbo = "apresentam" if len(cats_list) > 1 else "apresenta"
    insight_capital += (
        f'{prefixo} <strong>{cats_str}</strong> {verbo} estoque total '
        f'abaixo do mínimo necessário, indicando risco de ruptura agregado. '
    )
insight_capital += (
    f'A categoria com menor giro médio é <strong>{cat_menor_venda}</strong> '
    f'({tabela_cat.loc[cat_menor_venda, "Venda_Media"]:.1f} un/dia), '
    f'sugerindo possível sobreestoque relativo.</div>'
)
st.markdown(insight_capital, unsafe_allow_html=True)


# ── RISCO DE RUPTURA ────────────────────────────
st.markdown('<div class="sec-title">Risco de Ruptura</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-question">Quais produtos apresentam maior risco de ruptura no curto prazo?</div>', unsafe_allow_html=True)

c3a, c3b = st.columns([1.2, 0.8])

with c3a:
    top10_base = df_f.sort_values(["Cobertura_Estoque_Dias", "Venda_Media_Diaria"], ascending=[True, False]).head(10)
    
    fig3 = go.Figure(go.Bar(
        x=top10_base["Nome_Produto"], y=top10_base["Cobertura_Estoque_Dias"],
        marker_color=[VERMELHO if c < 2 else AMARELO for c in top10_base["Cobertura_Estoque_Dias"]],
        text=[f"{v:.1f}d" for v in top10_base["Cobertura_Estoque_Dias"]],
        textposition="outside", textfont=dict(color=TEXTO, size=11),
    ))
    fig3.add_hline(y=2, line_color=VERMELHO, line_dash="dot", line_width=1.5, annotation_text="Corte Crítico (2d)", annotation_font_color=VERMELHO)
    fig3.update_layout(title=dict(text="Top 10 Produtos em Risco", font=dict(size=14, color=TEXTO2)),
                       **PL, xaxis=dict(title="", showgrid=False, tickangle=-45), yaxis=ax("Cobertura (dias)"),
                       height=420)
    fig3.update_layout(margin=dict(l=50, r=40, t=36, b=100))
    st.plotly_chart(fig3, use_container_width=True)

with c3b:
    # Focando os indicadores especificamente no Top 10 exibido
    criticos = len(top10_base[(top10_base["Cobertura_Estoque_Dias"] < 2) & (top10_base["Venda_Media_Diaria"] > 0)])
    atencao = len(top10_base[(top10_base["Cobertura_Estoque_Dias"] >= 2) & (top10_base["Cobertura_Estoque_Dias"] < 5)])

    st.markdown(
        f'<div class="insight"><span class="dot" style="background:{VERMELHO}"></span> '
        f'<strong>{criticos}</strong> dos 10 itens em zona crítica — cobertura < 2 dias</div>'
        f'<div class="insight"><span class="dot" style="background:{AMARELO}"></span> '
        f'<strong>{atencao}</strong> dos 10 itens em atenção — cobertura entre 2 e 5 dias</div>',
        unsafe_allow_html=True,
    )

    # Top 10 most critical — dark themed table
    top10 = top10_base.copy()[
        ["Nome_Produto", "Categoria", "Estoque_Atual", "Estoque_Minimo",
         "Venda_Media_Diaria", "Cobertura_Estoque_Dias", "Status_Entrega", "Data_Prevista_Chegada"]
    ].reset_index(drop=True)

    def risk_row_class(row):
        # Vermelho: Risco real de falta (Atrasado ou Crítico)
        if row["Status_Entrega"] in ["Atrasado", "Critico"]:
            return "row-danger"
        # Amarelo: Estoque baixo, mas reposição está No Prazo (Monitorar)
        elif row["Status_Entrega"] == "No Prazo":
            return "row-warning"
        return ""

    st.markdown(html_table(
        top10,
        cols=["Nome_Produto", "Estoque_Atual", "Venda_Media_Diaria", "Cobertura_Estoque_Dias", "Status_Entrega", "Data_Prevista_Chegada"],
        headers=["Produto", "Atual", "Venda/dia", "Cobert. (d)", "Situação Reposição", "Prev. Chegada"],
        fmt={
            "Cobertura_Estoque_Dias": lambda v: f"{v:.1f}", 
            "Venda_Media_Diaria": lambda v: f"{v:.0f}",
            "Data_Prevista_Chegada": lambda x: x.strftime("%d/%m") if pd.notna(x) else "—"
        },
        row_class_fn=risk_row_class,
        max_height=360,
    ), unsafe_allow_html=True)

# Insight executivo — Risco de Ruptura
if len(top10) > 0:
    pior = top10.iloc[0]
    pior_cob = pior["Cobertura_Estoque_Dias"]
    pior_nome = pior["Nome_Produto"]
    # Cálculo do custo da demanda perdida por dia (Venda Média x Custo)
    venda_risco_diario = (top10_base["Venda_Media_Diaria"] * top10_base["Custo_Unitario"]).sum()
    cats_risco = top10["Categoria"].value_counts()
    cat_mais_risco = cats_risco.index[0] if not cats_risco.empty else "N/A"

    st.markdown(
        f'<div class="exec-insight"><div class="ei-label">Prioridade de Ação — Top 10</div>'
        f'Focando nos 10 itens de maior risco, identificamos que <strong>{criticos}</strong> operam com cobertura crítica (&lt; 2 dias), '
        f'exigindo intervenção imediata para evitar ruptura prolongada. '
        f'O item mais sensível é <strong>{pior_nome}</strong> ({pior_cob:.1f}d). '
        f'O <strong>impacto diário (custo)</strong> por falta de estoque desses 10 itens soma <strong>R$ {venda_risco_diario:,.0f}</strong>. '
        f'A categoria <strong>{cat_mais_risco}</strong> concentra a maior parte dessa urgência operacional.</div>',
        unsafe_allow_html=True,
    )


# ── PARETO ──────────────────────────────────────
st.markdown('<div class="sec-title">Concentração de Capital — Pareto</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-question">Quais poucos produtos concentram a maior parte do capital investido?</div>', unsafe_allow_html=True)

c4a, c4b = st.columns([1.4, 0.6])

with c4a:
    df_p = df_f[["Nome_Produto", "Valor_Total_Estoque"]].copy()
    df_p = df_p.sort_values("Valor_Total_Estoque", ascending=False).reset_index(drop=True)
    total_val = df_p["Valor_Total_Estoque"].sum()
    df_p["Acum"] = (df_p["Valor_Total_Estoque"].cumsum() / total_val * 100).round(1)

    curva_a = df_p[df_p["Acum"] <= 20].copy()
    if len(curva_a) == 0 and len(df_p) > 0:
        curva_a = df_p.head(1)
    
    fig4 = go.Figure(go.Bar(
        y=curva_a["Nome_Produto"],
        x=curva_a["Valor_Total_Estoque"],
        orientation="h",
        marker_color=LIMA,
        text=[f"R$ {v:,.0f}" for v in curva_a["Valor_Total_Estoque"]],
        textposition="auto", textfont=dict(color=BRANCO, size=11)
    ))
    fig4.update_layout(
        title=dict(text=f"Produtos que compõem os 20% mais caros", font=dict(size=14, color=TEXTO2)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXTO2, family="Inter", size=12),
        yaxis=dict(title="", autorange="reversed", showgrid=False), xaxis=ax("Valor (R$)"),
        height=420, margin=dict(t=36, b=20, l=150, r=20)
    )
    st.plotly_chart(fig4, use_container_width=True)

with c4b:
    v20 = curva_a["Valor_Total_Estoque"].sum()
    pct_skus = len(curva_a) / len(df_p) * 100
    st.markdown(
        f'<div class="insight" style="margin-top:0">'
        f'<strong style="font-size:1.5rem;color:{LIMA}">{len(curva_a)}</strong> '
        f'<span>produtos (só {pct_skus:.1f}% do portfólio) sozinhos imobilizam <strong>20%</strong> de todo o capital investido</span><br><br>'
        f'<span style="color:{TEXTO};font-weight:600">R$ {v20:,.0f}</span> '
        f'de R$ {total_val:,.0f}</div>',
        unsafe_allow_html=True,
    )

    tp = curva_a[["Nome_Produto", "Valor_Total_Estoque", "Acum"]].reset_index(drop=True)
    st.markdown(html_table(
        tp,
        cols=["Nome_Produto", "Valor_Total_Estoque"],
        headers=["Produto (Curva A Restrita)", "Valor (R$)"],
        fmt={"Valor_Total_Estoque": lambda v: f"R$ {v:,.0f}"},
        max_height=300,
    ), unsafe_allow_html=True)

# Insight executivo — Concentração Curva A (Top 20% budget)
top1 = df_p.iloc[0]
st.markdown(
    f'<div class="exec-insight"><div class="ei-label">Resumo do Insight Corporativo</div>'
    f'Focando na hiper-concentração de capital, identificamos que a "Ponta do Iceberg" compreende apenas <strong>{len(curva_a)} produto(s)</strong> '
    f'({pct_skus:.1f}% do portfólio), mas que sozinhos retêm pesados <strong>20% de todo o caixa estocado</strong> (R$ {v20:,.0f}). '
    f'O item líder é <strong>{top1["Nome_Produto"]}</strong>.</div>',
    unsafe_allow_html=True,
)


# ── PREVISÃO DE CHEGADA ─────────────────────────
st.markdown('<div class="sec-title">Previsão de Reposição e Risco de Abastecimento</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-question">Quantos produtos têm previsão de chegada após 15/02/2026, indicando risco de atraso?</div>', unsafe_allow_html=True)

chegada = df_f[df_f["Data_Prevista_Chegada"] > pd.Timestamp("2026-02-15")].sort_values("Data_Prevista_Chegada")

c5a, c5b = st.columns(2)

with c5a:
    total_rastr = len(df_f[df_f["Data_Prevista_Chegada"].notna()])
    df_rastr = df_f[df_f["Data_Prevista_Chegada"].notna()].copy()
    ref_date = pd.Timestamp("2026-02-15")
    df_rastr["Periodo_Chegada"] = df_rastr["Data_Prevista_Chegada"].apply(
        lambda x: "Pós 15/02 (Risco Atraso)" if x > ref_date else "Antes 15/02 (Seguro)"
    )
    
    st.markdown(
        f'<div class="insight">'
        f'<strong>{len(chegada)}</strong> de {total_rastr} produtos rastreáveis chegarão apenas '
        f'<strong style="color:{VERMELHO}">após o deadline de 15/02</strong> '
        f'({len(chegada)/max(total_rastr,1)*100:.0f}%)</div>',
        unsafe_allow_html=True,
    )

    if total_rastr > 0:
        resumo_prazo = df_rastr.groupby("Periodo_Chegada").agg(
            Valor_Total_Estoque=("Valor_Total_Estoque", "sum"), 
            ID_Produto=("ID_Produto", "count")
        ).reset_index()
        
        fig5 = go.Figure(go.Pie(
            labels=resumo_prazo["Periodo_Chegada"], 
            values=resumo_prazo["ID_Produto"],
            hole=0.6,
            marker=dict(colors=[VERMELHO if "Pós" in p else "#4E9A6D" for p in resumo_prazo["Periodo_Chegada"]]),
            textinfo="value+label",
            textposition="outside",
            hovertemplate="<b>%{label}</b><br>%{value} produtos<extra></extra>"
        ))
        
        fig5.update_layout(
            title=dict(text="Produtos por Previsão de Chegada", font=dict(size=14, color=TEXTO2)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXTO2, family="Inter", size=12),
            height=380, margin=dict(t=40, l=20, b=20, r=20),
            showlegend=False
        )
        
        total_p_row = resumo_prazo[resumo_prazo["Periodo_Chegada"].str.contains("Pós")]
        total_p = total_p_row["ID_Produto"].sum() if len(total_p_row) > 0 else 0
        
        if total_p > 0:
            fig5.add_annotation(text=f"Risco de<br>Atraso<br><b>{total_p} itens</b>", x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=VERMELHO))
            
        st.plotly_chart(fig5, use_container_width=True)

with c5b:
    # Focando o Lead Time apenas nos itens que estão em fluxo de reposição
    lt_cat = df_rastr.groupby("Categoria").agg(
        Lead_Time_Medio=("Lead_Time_Fornecedor", "mean"),
        No_Prazo=("Status_Entrega", lambda x: (x == "No Prazo").sum()),
        Total=("ID_Produto", "count"),
    ).round(1)
    lt_cat["Taxa No Prazo (%)"] = (lt_cat["No_Prazo"] / lt_cat["Total"] * 100).round(0)

    fig6 = go.Figure(go.Bar(
        x=lt_cat.index, y=lt_cat["Lead_Time_Medio"],
        marker_color=["#22C55E" if v <= 7 else (AMARELO if v <= 10 else VERMELHO) for v in lt_cat["Lead_Time_Medio"]],
        text=[f"{v:.0f}d" for v in lt_cat["Lead_Time_Medio"]],
        textposition="auto", textfont=dict(color=BRANCO, size=12),
    ))
    fig6.update_layout(title=dict(text="Lead Time Médio (Itens em Reposição)", font=dict(size=14, color=TEXTO2)),
                       **PL, yaxis=ax("Dias"), xaxis=dict(title=""), height=280)
    st.plotly_chart(fig6, use_container_width=True)

    if len(chegada) > 0:
        cd = chegada[["Nome_Produto", "Categoria", "Lead_Time_Fornecedor",
                       "Data_Prevista_Chegada", "Status_Entrega"]].reset_index(drop=True)

        def arrival_row_class(row):
            if row["Status_Entrega"] == "Critico":
                return "row-danger"
            elif row["Status_Entrega"] == "Atrasado":
                return "row-warning"
            return ""

        st.markdown(html_table(
            cd,
            cols=["Nome_Produto", "Categoria", "Lead_Time_Fornecedor", "Data_Prevista_Chegada", "Status_Entrega"],
            headers=["Produto", "Categoria", "Lead Time", "Chegada", "Status"],
            fmt={
                "Data_Prevista_Chegada": lambda x: x.strftime("%d/%m/%Y") if pd.notna(x) else "—",
                "Lead_Time_Fornecedor": lambda v: f"{v}d",
            },
            row_class_fn=arrival_row_class,
            max_height=200,
        ), unsafe_allow_html=True)

# Insight executivo — Previsão de Chegada
atrasados_log = len(chegada[chegada["Status_Entrega"].isin(["Atrasado", "Critico"])])
valor_risco_chegada = chegada["Valor_Total_Estoque"].sum()
lt_max_cat = lt_cat["Lead_Time_Medio"].idxmax() if not lt_cat.empty else "N/A"
lt_max_val = lt_cat.loc[lt_max_cat, "Lead_Time_Medio"] if not lt_cat.empty else 0

st.markdown(
    f'<div class="exec-insight"><div class="ei-label">Análise de Risco de Abastecimento</div>'
    f'Identificamos <strong>{len(chegada)} produtos</strong> com chegada prevista após o deadline de 15/02, '
    f'dos quais <strong>{atrasados_log}</strong> já apresentam atraso logístico confirmado. '
    f'O valor total em estoque desses itens sob risco é de <strong>R$ {valor_risco_chegada:,.0f}</strong>. '
    f'A categoria <strong>{lt_max_cat}</strong> demanda maior atenção devido ao Lead Time elevado '
    f'(média de <strong>{lt_max_val:.0f} dias</strong>), o que dificulta manobras rápidas de reposição.</div>',
    unsafe_allow_html=True,
)


# ── FOOTER ──────────────────────────────────────
st.markdown(
    f'<div style="text-align:center;color:{TEXTO2};font-size:0.75rem;padding:24px 0 12px 0;'
    f'border-top:1px solid {BORDA};margin-top:32px;">'
    f'SBF Inventário · Python · Pandas · Streamlit · Plotly · '
    f'Atualizado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}</div>',
    unsafe_allow_html=True,
)
