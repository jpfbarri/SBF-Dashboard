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
TEXTO2 = "#8B8FA3"
VERDE = "#005F1F"
LIMA = "#9EFE06"
VERDE_MEDIO = "#2D8B46"
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
    font-size: 0.7rem;
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
    font-size: 0.95rem;
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
    padding: 12px 16px;
    font-size: 0.82rem;
    color: {TEXTO2};
    margin-bottom: 8px;
}}
.insight strong {{ color: {TEXTO}; }}

/* Executive insight block */
.exec-insight {{
    background: {BG_CARD};
    border: 1px solid {BORDA};
    border-left: 3px solid {LIMA};
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0 24px 0;
    font-size: 0.82rem;
    line-height: 1.6;
    color: {TEXTO2};
}}
.exec-insight strong {{ color: {TEXTO}; }}
.exec-insight .ei-label {{
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: {LIMA};
    margin-bottom: 6px;
}}

/* Section subtitle = business question */
.sec-question {{
    font-size: 0.78rem;
    color: {TEXTO2};
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
    font-size: 0.68rem;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid {BORDA};
}}
.dark-table tbody td {{
    background: {BG_CARD};
    color: {TEXTO};
    padding: 8px 12px;
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
    return dict(showgrid=True, gridcolor="#1E2130", title=title, **kw)


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
    f'<span class="badge">Atualizado em {datetime.now().strftime("%d/%m/%Y %H:%M")}</span>'
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

def kpi(val, label, dot_color=None):
    dot = f'<span class="dot" style="background:{dot_color}"></span>' if dot_color else ""
    return f'<div class="kpi"><div class="val">{val}</div><div class="lbl">{dot}{label}</div></div>'

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(kpi(f"R$ {valor_total:,.0f}", "Valor Total em Estoque"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi(f"{saude_pct:.0f}%", "Índice de Saúde", "#22C55E" if saude_pct >= 60 else AMARELO), unsafe_allow_html=True)
with k3:
    st.markdown(kpi(str(ruptura), "Produtos em Ruptura", VERMELHO), unsafe_allow_html=True)
with k4:
    st.markdown(kpi(str(estoque_zero), "Estoque Zerado", VERMELHO), unsafe_allow_html=True)
with k5:
    st.markdown(kpi(f"{cob_media:.1f} dias", "Cobertura Média", cob_cor), unsafe_allow_html=True)


# ── SAÚDE POR CATEGORIA ────────────────────────
st.markdown('<div class="sec-title">Saúde por Categoria</div>', unsafe_allow_html=True)

cat_health = df_f.groupby("Categoria").agg(
    Total=("ID_Produto", "count"),
    Saudaveis=("Saudavel", "sum"),
    Em_Ruptura=("Abaixo_Minimo", "sum"),
    Estoque_Zero=("Estoque_Atual", lambda x: (x == 0).sum()),
).round(0)
cat_health["Pct"] = (cat_health["Saudaveis"] / cat_health["Total"] * 100).round(0)

cc1, cc2, cc3 = st.columns(3)
for col_st, (cat, row) in zip([cc1, cc2, cc3], cat_health.iterrows()):
    pct = row["Pct"]
    cor = "#22C55E" if pct >= 70 else (AMARELO if pct >= 40 else VERMELHO)
    with col_st:
        st.markdown(
            f'<div class="cat-card">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            f'<div>'
            f'<div class="name">{cat}</div>'
            f'<div class="stat">{int(row["Total"])} produtos<br>'
            f'{int(row["Em_Ruptura"])} em ruptura · {int(row["Estoque_Zero"])} sem estoque</div>'
            f'</div>'
            f'<div class="pct" style="color:{cor}">{pct:.0f}%</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )


# ── VALOR POR CATEGORIA + ESTOQUE vs MÍNIMO ────
st.markdown('<div class="sec-title">Distribuição de Capital por Categoria</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-question">Quais categorias concentram o maior capital investido e como ele se compara com a demanda?</div>', unsafe_allow_html=True)

tabela_cat = df_f.groupby("Categoria").agg(
    Qtd_Produtos=("ID_Produto", "count"),
    Estoque_Total=("Estoque_Atual", "sum"),
    Custo_Medio=("Custo_Unitario", "mean"),
    Valor_Total=("Valor_Total_Estoque", "sum"),
    Venda_Media=("Venda_Media_Diaria", "mean"),
).round(2)
tabela_cat["Participação (%)"] = (tabela_cat["Valor_Total"] / tabela_cat["Valor_Total"].sum() * 100).round(1)

cat_estoque = df_f.groupby("Categoria").agg(
    Estoque_Atual=("Estoque_Atual", "sum"),
    Estoque_Minimo=("Estoque_Minimo", "sum"),
)

c2a, c2b = st.columns(2)
with c2a:
    fig = go.Figure(go.Bar(
        x=tabela_cat.index, y=tabela_cat["Valor_Total"],
        marker_color=[VERDE, LIMA, VERDE_MEDIO][:len(tabela_cat)],
        text=[f"R$ {v:,.0f}" for v in tabela_cat["Valor_Total"]],
        textposition="auto", textfont=dict(color=BRANCO, size=11),
    ))
    fig.update_layout(title=dict(text="Valor Total em Estoque", font=dict(size=14, color=TEXTO2)),
                      **PL, yaxis=ax("R$"), xaxis=dict(title=""), height=420)
    st.plotly_chart(fig, use_container_width=True)

with c2b:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=cat_estoque.index, y=cat_estoque["Estoque_Atual"],
                          name="Atual", marker_color=LIMA,
                          text=[f"{v:,.0f}" for v in cat_estoque["Estoque_Atual"]],
                          textposition="auto", textfont=dict(color=BRANCO, size=11)))
    fig2.add_trace(go.Bar(x=cat_estoque.index, y=cat_estoque["Estoque_Minimo"],
                          name="Mínimo", marker_color=VERMELHO, opacity=0.6,
                          text=[f"{v:,.0f}" for v in cat_estoque["Estoque_Minimo"]],
                          textposition="auto", textfont=dict(color=BRANCO, size=11)))
    fig2.update_layout(title=dict(text="Estoque Atual vs Mínimo", font=dict(size=14, color=TEXTO2)),
                       **PL, yaxis=ax("Unidades"), xaxis=dict(title=""), barmode="group", height=420,
                       legend=dict(orientation="h", y=1.05, x=0, font=dict(size=11, color=TEXTO2)))
    st.plotly_chart(fig2, use_container_width=True)

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
    cats_deficit = ", ".join(cat_deficit.index.tolist())
    insight_capital += (
        f'As categorias <strong>{cats_deficit}</strong> apresentam estoque total '
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
    df_sc = df_f[df_f["Venda_Media_Diaria"] > 0].copy()
    df_sc["Sz"] = df_sc["Valor_Total_Estoque"].clip(lower=100)

    fig3 = go.Figure()
    fig3.add_vrect(x0=0, x1=2, fillcolor=VERMELHO, opacity=0.06, layer="below", line_width=0)
    fig3.add_vrect(x0=2, x1=5, fillcolor=AMARELO, opacity=0.04, layer="below", line_width=0)

    for sv, cor in STATUS_COR.items():
        sub = df_sc[df_sc["Status_Entrega"] == sv]
        if len(sub) == 0:
            continue
        fig3.add_trace(go.Scatter(
            x=sub["Cobertura_Estoque_Dias"], y=sub["Venda_Media_Diaria"], mode="markers",
            marker=dict(size=sub["Sz"].apply(lambda v: max(7, min(26, v / 600))),
                        color=cor, line=dict(width=1, color=BG_CARD), opacity=0.8),
            name=sv,
            text=[f"<b>{r['Nome_Produto']}</b><br>Cobertura: {r['Cobertura_Estoque_Dias']:.1f}d<br>"
                  f"Venda/dia: {r['Venda_Media_Diaria']:.0f}<br>Estoque: {r['Estoque_Atual']} (mín: {r['Estoque_Minimo']})"
                  for _, r in sub.iterrows()],
            hovertemplate="%{text}<extra></extra>",
        ))

    fig3.add_vline(x=2, line_color=VERMELHO, line_dash="dot", line_width=1)
    fig3.add_vline(x=5, line_color=AMARELO, line_dash="dot", line_width=1)
    fig3.update_layout(title=dict(text="Cobertura vs Demanda", font=dict(size=14, color=TEXTO2)),
                       **PL, xaxis=ax("Cobertura (dias)"), yaxis=ax("Venda Média Diária"),
                       height=420, legend=dict(orientation="h", y=1.05, x=0, font=dict(size=11, color=TEXTO2)))
    st.plotly_chart(fig3, use_container_width=True)

with c3b:
    criticos = len(df_f[(df_f["Cobertura_Estoque_Dias"] < 2) & (df_f["Venda_Media_Diaria"] > 0)])
    atencao = len(df_f[(df_f["Cobertura_Estoque_Dias"] >= 2) & (df_f["Cobertura_Estoque_Dias"] < 5)])

    st.markdown(
        f'<div class="insight"><span class="dot" style="background:{VERMELHO}"></span> '
        f'<strong>{criticos}</strong> produtos em zona crítica — cobertura inferior a 2 dias</div>'
        f'<div class="insight"><span class="dot" style="background:{AMARELO}"></span> '
        f'<strong>{atencao}</strong> produtos em atenção — cobertura entre 2 e 5 dias</div>',
        unsafe_allow_html=True,
    )

    # Top 10 most critical — dark themed table
    top10 = df_f.nsmallest(10, "Cobertura_Estoque_Dias")[
        ["Nome_Produto", "Categoria", "Estoque_Atual", "Estoque_Minimo",
         "Venda_Media_Diaria", "Cobertura_Estoque_Dias", "Status_Entrega"]
    ].reset_index(drop=True)

    def risk_row_class(row):
        if row["Cobertura_Estoque_Dias"] < 2:
            return "row-danger"
        elif row["Cobertura_Estoque_Dias"] < 5:
            return "row-warning"
        return ""

    st.markdown(html_table(
        top10,
        cols=["Nome_Produto", "Estoque_Atual", "Estoque_Minimo", "Venda_Media_Diaria", "Cobertura_Estoque_Dias", "Status_Entrega"],
        headers=["Produto", "Atual", "Mín.", "Venda/dia", "Cobert. (d)", "Status"],
        fmt={"Cobertura_Estoque_Dias": lambda v: f"{v:.1f}", "Venda_Media_Diaria": lambda v: f"{v:.0f}"},
        row_class_fn=risk_row_class,
        max_height=360,
    ), unsafe_allow_html=True)

# Insight executivo — Risco de Ruptura
if len(top10) > 0:
    pior = top10.iloc[0]
    pior_cob = pior["Cobertura_Estoque_Dias"]
    pior_nome = pior["Nome_Produto"]
    valor_risco = df_f[df_f["Cobertura_Estoque_Dias"] < 5]["Valor_Total_Estoque"].sum()
    pct_risco = criticos / max(len(df_f), 1) * 100
    cats_risco = top10["Categoria"].value_counts()
    cat_mais_risco = cats_risco.index[0]

    st.markdown(
        f'<div class="exec-insight"><div class="ei-label">Resumo do Insight</div>'
        f'<strong>{criticos}</strong> produtos ({pct_risco:.0f}% do total) operam com cobertura inferior a 2 dias, '
        f'representando risco iminente de ruptura e perda de vendas. '
        f'O item mais crítico é <strong>{pior_nome}</strong> com apenas <strong>{pior_cob:.1f} dia(s)</strong> de cobertura. '
        f'A categoria <strong>{cat_mais_risco}</strong> concentra a maioria dos itens em zona de risco. '
        f'O valor total em estoque sob risco (cobertura &lt; 5 dias) soma <strong>R$ {valor_risco:,.0f}</strong>.</div>',
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

    n_show = min(20, len(df_p))
    ds = df_p.head(n_show)
    idx_80 = df_p[df_p["Acum"] >= 80].index[0] if len(df_p[df_p["Acum"] >= 80]) > 0 else len(df_p) - 1
    n_80 = idx_80 + 1

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=ds["Nome_Produto"], y=ds["Valor_Total_Estoque"],
        marker_color=[LIMA if i <= idx_80 else "#3A3D4A" for i in range(n_show)],
        text=[f"R$ {v:,.0f}" for v in ds["Valor_Total_Estoque"]],
        textposition="auto", textfont=dict(color=BRANCO, size=9),
        name="Valor", yaxis="y",
    ))
    fig4.add_trace(go.Scatter(
        x=ds["Nome_Produto"], y=ds["Acum"],
        mode="lines+markers", line=dict(color=AMARELO, width=2),
        marker=dict(size=4, color=AMARELO), name="% Acumulado", yaxis="y2",
    ))
    fig4.add_hline(y=80, line_color=VERMELHO, line_dash="dash", line_width=1,
                   annotation_text="80%", annotation_font_color=VERMELHO,
                   annotation_font_size=10, annotation_position="right", yref="y2")
    fig4.update_layout(
        title=dict(text=f"Top {n_show} Produtos por Valor", font=dict(size=14, color=TEXTO2)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXTO2, family="Inter", size=12),
        yaxis=dict(title="Valor (R$)", showgrid=True, gridcolor="#1E2130"),
        yaxis2=dict(title=dict(text="% Acumulado", font=dict(color=AMARELO)),
                    overlaying="y", side="right", showgrid=False, range=[0, 105],
                    ticksuffix="%", tickfont=dict(color=AMARELO)),
        xaxis=dict(title="", tickangle=30), height=420,
        margin=dict(t=36, b=100, l=50, r=50), bargap=0.3,
        legend=dict(orientation="h", y=1.05, x=0, font=dict(size=11, color=TEXTO2)),
    )
    st.plotly_chart(fig4, use_container_width=True)

with c4b:
    v80 = df_p.head(n_80)["Valor_Total_Estoque"].sum()
    pct_skus = n_80 / len(df_p) * 100
    st.markdown(
        f'<div class="insight" style="margin-top:0">'
        f'<strong style="font-size:1.5rem;color:{TEXTO}">{n_80}</strong> '
        f'<span>produtos ({pct_skus:.0f}% dos SKUs) concentram <strong>80%</strong> do valor total</span><br><br>'
        f'<span style="color:{TEXTO};font-weight:600">R$ {v80:,.0f}</span> '
        f'de R$ {total_val:,.0f}</div>',
        unsafe_allow_html=True,
    )

    tp = df_p.head(n_80)[["Nome_Produto", "Valor_Total_Estoque", "Acum"]].reset_index(drop=True)
    st.markdown(html_table(
        tp,
        cols=["Nome_Produto", "Valor_Total_Estoque", "Acum"],
        headers=["Produto", "Valor (R$)", "Acum (%)"],
        fmt={
            "Valor_Total_Estoque": lambda v: f"R$ {v:,.0f}",
            "Acum": lambda v: f"{v:.1f}%",
        },
        max_height=300,
    ), unsafe_allow_html=True)

# Insight executivo — Pareto
top1 = df_p.iloc[0]
st.markdown(
    f'<div class="exec-insight"><div class="ei-label">Resumo do Insight</div>'
    f'Apenas <strong>{n_80} produtos</strong> ({pct_skus:.0f}% dos SKUs) concentram '
    f'<strong>80% do capital</strong> investido em estoque (R$ {v80:,.0f} de R$ {total_val:,.0f}). '
    f'O item de maior valor é <strong>{top1["Nome_Produto"]}</strong> (R$ {top1["Valor_Total_Estoque"]:,.0f}). '
    f'Esses itens exigem monitoramento prioritário, revisão frequente do estoque de segurança '
    f'e negociação de condições preferenciais com fornecedores.</div>',
    unsafe_allow_html=True,
)


# ── PREVISÃO DE CHEGADA ─────────────────────────
st.markdown('<div class="sec-title">Previsão de Reposição e Risco de Abastecimento</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-question">Quantos produtos têm previsão de chegada após 15/02/2026, indicando risco de atraso?</div>', unsafe_allow_html=True)

chegada = df_f[df_f["Data_Prevista_Chegada"] > pd.Timestamp("2026-02-15")].sort_values("Data_Prevista_Chegada")

c5a, c5b = st.columns(2)

with c5a:
    total_rastr = len(df_f[df_f["Data_Prevista_Chegada"].notna()])
    st.markdown(
        f'<div class="insight">'
        f'<strong>{len(chegada)}</strong> produtos com chegada após 15/02/2026 '
        f'({len(chegada)}/{total_rastr} rastreáveis — '
        f'<strong>{len(chegada)/max(total_rastr,1)*100:.0f}%</strong>)</div>',
        unsafe_allow_html=True,
    )

    if len(chegada) > 0:
        fig5 = go.Figure()
        for sv, cor in STATUS_COR.items():
            sub = chegada[chegada["Status_Entrega"] == sv]
            if len(sub) == 0:
                continue
            fig5.add_trace(go.Scatter(
                x=sub["Data_Prevista_Chegada"], y=sub["Nome_Produto"], mode="markers",
                marker=dict(size=10, color=cor, line=dict(width=1, color=BG_CARD)),
                name=sv,
                text=[f"<b>{r['Nome_Produto']}</b><br>{r['Data_Prevista_Chegada'].strftime('%d/%m/%Y')}<br>"
                      f"Lead Time: {r['Lead_Time_Fornecedor']}d · {r['Status_Entrega']}"
                      for _, r in sub.iterrows()],
                hovertemplate="%{text}<extra></extra>",
            ))

        ref = datetime(2026, 2, 15)
        fig5.add_shape(type="line", x0=ref, x1=ref, y0=0, y1=1, yref="paper",
                       line=dict(color=VERMELHO, dash="dash", width=1))
        fig5.add_annotation(x=ref, y=1.05, yref="paper", text="15/02/2026",
                            showarrow=False, font=dict(color=VERMELHO, size=10))
        fig5.update_layout(
            title=dict(text="Timeline de Chegada", font=dict(size=14, color=TEXTO2)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXTO2, family="Inter", size=12),
            xaxis=ax("Data Prevista"), yaxis=dict(title="", autorange="reversed"),
            height=420, margin=dict(t=36, l=160, b=30, r=20),
            legend=dict(orientation="h", y=1.05, x=0, font=dict(size=11, color=TEXTO2)),
        )
        st.plotly_chart(fig5, use_container_width=True)

with c5b:
    lt_cat = df_f.groupby("Categoria").agg(
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
    fig6.update_layout(title=dict(text="Lead Time Médio por Categoria", font=dict(size=14, color=TEXTO2)),
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
criticos_log = len(chegada[chegada["Status_Entrega"] == "Critico"])
lt_max_cat = lt_cat["Lead_Time_Medio"].idxmax()
lt_max_val = lt_cat.loc[lt_max_cat, "Lead_Time_Medio"]
taxa_prazo_geral = df_f[df_f["Status_Entrega"] == "No Prazo"].shape[0] / max(len(df_f), 1) * 100

st.markdown(
    f'<div class="exec-insight"><div class="ei-label">Resumo do Insight</div>'
    f'Dos <strong>{len(chegada)}</strong> produtos com chegada prevista após 15/02/2026, '
    f'<strong>{atrasados_log}</strong> apresentam status de atraso '
    f'(sendo {criticos_log} em situação crítica). '
    f'A categoria <strong>{lt_max_cat}</strong> possui o maior lead time médio '
    f'(<strong>{lt_max_val:.0f} dias</strong>), o que eleva o risco de desabastecimento. '
    f'A taxa geral de entregas no prazo é de <strong>{taxa_prazo_geral:.0f}%</strong> — '
    + (f'abaixo do ideal para operação estável.' if taxa_prazo_geral < 70 else f'dentro de padrão aceitável, mas requer monitoramento contínuo.')
    + '</div>',
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
