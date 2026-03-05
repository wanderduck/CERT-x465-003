"""Pokemon Base Stats Explorer — Plotly Dash dashboard."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DATA_PATH = Path(__file__).resolve().parent / ".." / "data" / "pokemon_dataset_MASTER.csv"
df = pd.read_csv(DATA_PATH)

# ---------------------------------------------------------------------------
# Compute GMM cluster assignments (reproduces notebook Section 7)
# ---------------------------------------------------------------------------
ZSCORE_COLS = ['HP_zscore', 'Attack_zscore', 'Defense_zscore',
               'Speed_zscore', 'Special_Attack_zscore', 'Special_Defense_zscore']
_EXTRA_COLS = ['BMI', 'Physical/Special', 'Offensive/Defensive']

_cluster_df = df.dropna(subset=ZSCORE_COLS + _EXTRA_COLS + ['Type 1']).copy()
_scaler = StandardScaler()
_scaled = _scaler.fit_transform(_cluster_df[_EXTRA_COLS])
for _i, _col in enumerate(_EXTRA_COLS):
    _cluster_df[f'{_col}_scaled'] = _scaled[:, _i]
_t1_dummies = pd.get_dummies(_cluster_df['Type 1'], prefix='T1').astype(float)
_cluster_df = pd.concat([_cluster_df, _t1_dummies], axis=1)
_FEAT_COLS = (ZSCORE_COLS + [f'{c}_scaled' for c in _EXTRA_COLS]
              + [c for c in _t1_dummies.columns])
_X = _cluster_df[_FEAT_COLS].values
_gmm = GaussianMixture(n_components=14, covariance_type='diag',
                        random_state=42, n_init=5, max_iter=300)
_gmm.fit(_X)
_cluster_df['_cluster_id'] = _gmm.predict(_X)

CLUSTER_NAMES = {
    0: 'Fairy Fortress Elite', 1: 'Dragon Powerhouses', 2: 'Extreme Wall Outlier',
    3: 'Ghost Generalists', 4: 'Electric Speedsters', 5: 'Blue-Collar Brawlers',
    6: 'Armored Heavyweights', 7: 'Low-Stat Midtiers', 8: 'Pixie Wardens',
    9: 'Rooted Slowpokes', 10: 'Toxic Heavies', 11: 'Shadow Strikers',
    12: 'Psychic Cannons', 13: 'Fragile Normals',
}
_cluster_df['Cluster Role'] = _cluster_df['_cluster_id'].map(CLUSTER_NAMES)
# Merge cluster role back into main df
df = df.merge(_cluster_df[['Cluster Role']],
              left_index=True, right_index=True, how='left')
df['Cluster Role'] = df['Cluster Role'].fillna('Unassigned')

CLUSTER_ORDER = sorted(CLUSTER_NAMES.values())

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
STAT_COLS = ["HP", "Attack", "Defense", "Speed", "Special Attack", "Special Defense"]
ROLE_ORDER = [
    "Physical Sweeper", "Special Sweeper", "Mixed Attacker",
    "Balanced", "Tank", "Physical Wall", "Special Wall",
]

TYPE_COLORS = {
    "Normal": "#A8A77A", "Fire": "#EE8130", "Water": "#6390F0",
    "Electric": "#F7D02C", "Grass": "#7AC74C", "Ice": "#96D9D6",
    "Fighting": "#C22E28", "Poison": "#A33EA1", "Ground": "#E2BF65",
    "Flying": "#A98FF3", "Psychic": "#F95587", "Bug": "#A6B91A",
    "Rock": "#B6A136", "Ghost": "#735797", "Dragon": "#6F35FC",
    "Dark": "#705746", "Steel": "#B7B7CE", "Fairy": "#D685AD",
}

ROLE_COLORS = [
    "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3",
    "#A6D854", "#FFD92F", "#E5C494",
]
ROLE_COLOR_MAP = dict(zip(ROLE_ORDER, ROLE_COLORS))

def _hex_scale(hex_color, factor):
    """factor < 1 = darken, factor > 1 = lighten toward white."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if factor > 1:
        f = factor - 1
        r, g, b = int(r + (255 - r) * f), int(g + (255 - g) * f), int(b + (255 - b) * f)
    else:
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
    return '#{:02x}{:02x}{:02x}'.format(min(r, 255), min(g, 255), min(b, 255))

TYPE_COLORS_LIGHT = {t: _hex_scale(c, 1.45) for t, c in TYPE_COLORS.items()}
TYPE_COLORS_DARK = {t: _hex_scale(c, 0.60) for t, c in TYPE_COLORS.items()}

ALL_TYPES = sorted(TYPE_COLORS.keys())
ALL_GENS = sorted(df["Generation"].dropna().unique())

TEMPLATE = "plotly_dark"

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
PAGE_BG = "#1a1a2e"
TEXT_COLOR = "#e8e8f0"
ACCENT_BLUE = "#6390F0"
ACCENT_GLOW = "0 0 12px rgba(99, 144, 240, 0.3)"

CARD_STYLE = {
    "backgroundColor": "#252540",
    "border": "1px solid #3a3a5c",
    "borderTop": f"3px solid {ACCENT_BLUE}",
    "borderRadius": "10px",
    "padding": "18px 14px",
    "textAlign": "center",
    "flex": "1",
    "minWidth": "140px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.4)",
}
CARD_TITLE = {
    "fontSize": "0.75rem",
    "color": "#8888aa",
    "marginBottom": "6px",
    "textTransform": "uppercase",
    "letterSpacing": "1.2px",
    "fontWeight": "600",
}
CARD_VALUE = {
    "fontSize": "1.8rem",
    "fontWeight": "bold",
    "color": TEXT_COLOR,
    "lineHeight": "1.2",
}
DROPDOWN_STYLE = {"color": "#000", "borderRadius": "6px"}

FILTER_CONTAINER_STYLE = {
    "backgroundColor": "#20203a",
    "border": "1px solid #3a3a5c",
    "borderRadius": "12px",
    "padding": "20px 24px",
    "marginBottom": "20px",
}
FILTER_HEADER_STYLE = {
    "fontSize": "0.85rem",
    "color": "#8888aa",
    "textTransform": "uppercase",
    "letterSpacing": "1.5px",
    "fontWeight": "700",
    "marginBottom": "14px",
    "paddingBottom": "8px",
    "borderBottom": "1px solid #3a3a5c",
}
FILTER_LABEL_STYLE = {
    "fontSize": "0.95rem",
    "fontWeight": "bold",
    "color": "#c0c0d8",
    "marginBottom": "4px",
}

TAB_STYLE = {
    "backgroundColor": "#20203a",
    "color": "#8888aa",
    "border": "none",
    "borderBottom": "3px solid transparent",
    "padding": "14px 24px",
    "fontSize": "1rem",
    "fontWeight": "600",
    "cursor": "pointer",
}
TAB_SELECTED_STYLE = {
    "backgroundColor": "#252540",
    "color": "#ffffff",
    "border": "none",
    "borderBottom": f"3px solid {ACCENT_BLUE}",
    "boxShadow": ACCENT_GLOW,
    "padding": "14px 24px",
    "fontSize": "1rem",
    "fontWeight": "700",
    "cursor": "pointer",
}

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Dash(__name__)
app.title = "Pokemon Base Stats Explorer"
app.config.suppress_callback_exceptions = True

# Inject CSS to fix slider tooltip text color (black on white)
app.index_string = '''<!DOCTYPE html>
<html>
<head>
{%metas%}{%favicon%}{%css%}
<title>{%title%}</title>
<style>
.rc-slider-tooltip-inner {
    color: #000 !important;
    background-color: #fff !important;
    font-weight: bold;
}
</style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>'''

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
app.layout = html.Div(
    style={"backgroundColor": PAGE_BG, "color": TEXT_COLOR,
           "minHeight": "100vh", "padding": "20px", "fontFamily": "sans-serif"},
    children=[
        # ── Title ────────────────────────────────────────────────────────
        html.Div(style={"textAlign": "center", "marginBottom": "24px"}, children=[
            html.H1("Pokemon Base Stats Explorer",
                     style={"marginBottom": "4px", "fontSize": "2.2rem",
                            "fontWeight": "800", "color": ACCENT_BLUE,
                            "background": f"linear-gradient(135deg, {ACCENT_BLUE}, #a0c4ff, #ffffff)",
                            "WebkitBackgroundClip": "text",
                            "WebkitTextFillColor": "transparent"}),
            html.Div(style={"width": "80px", "height": "3px", "margin": "0 auto 8px auto",
                            "background": f"linear-gradient(90deg, {ACCENT_BLUE}, transparent)",
                            "borderRadius": "2px"}),
            html.P("Interactive EDA of 1,231 Pokemon across 9 generations",
                   style={"color": "#8888aa", "fontSize": "1rem", "margin": "0",
                          "letterSpacing": "0.5px"}),
        ]),

        # ── Global filters ────────────────────────────────────────────────
        html.Div(style=FILTER_CONTAINER_STYLE, children=[
            html.Div("Filters", style=FILTER_HEADER_STYLE),
            html.Div(
                style={"display": "flex", "gap": "20px", "flexWrap": "wrap",
                       "alignItems": "flex-end"},
                children=[
                    html.Div([
                        html.Label("Generation", style=FILTER_LABEL_STYLE),
                        dcc.Dropdown(
                            id="gen-filter",
                            options=[{"label": str(g), "value": g} for g in ALL_GENS],
                            multi=True,
                            placeholder="All generations",
                            style=DROPDOWN_STYLE,
                        ),
                    ], style={"flex": "1", "minWidth": "180px"}),

                    html.Div([
                        html.Label("Type 1", style=FILTER_LABEL_STYLE),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[{"label": t, "value": t} for t in ALL_TYPES],
                            multi=True,
                            placeholder="All types",
                            style=DROPDOWN_STYLE,
                        ),
                    ], style={"flex": "1", "minWidth": "180px"}),

                    html.Div([
                        html.Label("Type 2", style=FILTER_LABEL_STYLE),
                        dcc.Dropdown(
                            id="type2-filter",
                            options=[{"label": t, "value": t} for t in ALL_TYPES],
                            multi=True,
                            placeholder="All types",
                            style=DROPDOWN_STYLE,
                        ),
                    ], style={"flex": "1", "minWidth": "180px"}),

                    html.Div([
                        html.Label("Role", style=FILTER_LABEL_STYLE),
                        dcc.Dropdown(
                            id="role-filter",
                            options=(
                                [{"label": f"[Rule] {r}", "value": f"rule:{r}"} for r in ROLE_ORDER]
                                + [{"label": f"[Cluster] {c}", "value": f"cluster:{c}"} for c in CLUSTER_ORDER]
                            ),
                            multi=True,
                            placeholder="All roles",
                            style=DROPDOWN_STYLE,
                        ),
                    ], style={"flex": "1.5", "minWidth": "240px"}),

                    html.Div([
                        html.Label("Legendary", style=FILTER_LABEL_STYLE),
                        dcc.RadioItems(
                            id="legendary-filter",
                            options=[
                                {"label": "All", "value": "All"},
                                {"label": "Legendary", "value": "Legendary"},
                                {"label": "Non-Legendary", "value": "Non-Legendary"},
                            ],
                            value="All",
                            inline=True,
                            style={"display": "flex", "gap": "12px"},
                        ),
                    ], style={"minWidth": "260px"}),
                ],
            ),
        ]),

        # ── KPI cards ─────────────────────────────────────────────────────
        html.Div(
            id="kpi-row",
            style={"display": "flex", "gap": "12px", "flexWrap": "wrap",
                   "marginBottom": "24px"},
            children=[
                html.Div([html.Div("Count", style=CARD_TITLE),
                           html.Div(id="kpi-count", style=CARD_VALUE)],
                          style=CARD_STYLE),
                html.Div([html.Div("Avg Stat Total", style=CARD_TITLE),
                           html.Div(id="kpi-bst", style=CARD_VALUE)],
                          style=CARD_STYLE),
                html.Div([html.Div("Avg Speed", style=CARD_TITLE),
                           html.Div(id="kpi-speed", style=CARD_VALUE)],
                          style=CARD_STYLE),
                html.Div([html.Div("Avg BMI", style=CARD_TITLE),
                           html.Div(id="kpi-bmi", style=CARD_VALUE)],
                          style=CARD_STYLE),
                html.Div([html.Div("Dominant Role", style=CARD_TITLE),
                           html.Div(id="kpi-role", style=CARD_VALUE)],
                          style=CARD_STYLE),
                html.Div([html.Div("Legendary %", style=CARD_TITLE),
                           html.Div(id="kpi-legend-pct", style=CARD_VALUE)],
                          style=CARD_STYLE),
                html.Div([html.Div("Avg Specialization", style=CARD_TITLE),
                           html.Div(id="kpi-spec", style=CARD_VALUE)],
                          style=CARD_STYLE),
            ],
        ),

        # ── Tabs ──────────────────────────────────────────────────────────
        dcc.Tabs(
            id="tabs",
            value="tab-overview",
            colors={"border": "#3a3a5c", "primary": ACCENT_BLUE, "background": "#20203a"},
            children=[
                dcc.Tab(label="Overview", value="tab-overview",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="Type Identity", value="tab-type",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="Power & Specialization", value="tab-power",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="Generational Trends", value="tab-gen",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="Evolution & Roles", value="tab-evo",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="Pokemon Creator", value="tab-creator",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            ],
        ),

        # Tab content container
        html.Div(id="tab-content", style={"marginTop": "20px", "padding": "0 8px"}),
    ],
)

# ---------------------------------------------------------------------------
# Helper: empty placeholder figure
# ---------------------------------------------------------------------------
def _empty_fig(title: str = "") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        template=TEMPLATE, title=title or "Coming soon",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        annotations=[dict(text="Placeholder", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False,
                          font=dict(size=18, color="#888"))],
    )
    return fig


# ---------------------------------------------------------------------------
# Pokemon Creator: role classifier + form + charts
# ---------------------------------------------------------------------------
_SLIDER_MAP = [
    ("HP",              "creator-hp"),
    ("Attack",          "creator-attack"),
    ("Defense",         "creator-defense"),
    ("Speed",           "creator-speed"),
    ("Special Attack",  "creator-spatk"),
    ("Special Defense", "creator-spdef"),
]
_SLIDER_MARKS = {v: {"label": str(v), "style": {"color": "#ccc"}}
                 for v in [1, 50, 100, 150, 200, 255]}

_FORM_LABEL = {"color": "#ddd", "fontWeight": "bold", "marginBottom": "2px",
               "marginTop": "12px", "fontSize": "14px"}


def _classify_role(hp, atk, dfn, spd, spatk, spdef):
    """Classify into one of 7 combat roles."""
    if atk > spatk and atk > dfn and atk > spdef and (dfn == 0 or atk / max(dfn, 1) > 1.2):
        return "Physical Sweeper"
    if spatk > atk and spatk > dfn and spatk > spdef and (spdef == 0 or spatk / max(spdef, 1) > 1.2):
        return "Special Sweeper"
    if dfn > atk and dfn > spatk:
        return "Physical Wall"
    if spdef > atk and spdef > spatk:
        return "Special Wall"
    if atk + spatk > hp + dfn + spdef:
        return "Mixed Attacker"
    if hp >= atk and hp >= spatk and hp + dfn + spdef > atk + spatk:
        return "Tank"
    return "Balanced"


def _creator_form():
    """Left-column form for the Pokemon Creator tab."""
    sliders = []
    for label, sid in _SLIDER_MAP:
        sliders.append(html.Div(label, style=_FORM_LABEL))
        sliders.append(dcc.Slider(
            id=sid, min=1, max=255, step=1, value=80,
            marks=_SLIDER_MARKS,
            tooltip={"placement": "bottom", "always_visible": True},
        ))

    return html.Div([
        html.H4("Create Your Pokemon",
                 style={"color": "#fff", "marginBottom": "16px"}),
        html.Div("Name", style=_FORM_LABEL),
        dcc.Input(id="creator-name", type="text",
                  placeholder="Pokemon Name", value="MyPokemon",
                  style={"width": "100%", "padding": "6px", "borderRadius": "4px",
                         "border": "1px solid #555", "backgroundColor": "#1a1a2e",
                         "color": "#fff"}),
        html.Div("Type 1", style=_FORM_LABEL),
        dcc.Dropdown(id="creator-type", options=ALL_TYPES, value="Fire",
                     style={"color": "#000"}),
        html.Div("Type 2", style=_FORM_LABEL),
        dcc.Dropdown(id="creator-type2",
                     options=[{"label": "None", "value": "None"}]
                             + [{"label": t, "value": t} for t in ALL_TYPES],
                     value="None", style={"color": "#000"}),
        *sliders,
        html.Div(style={"display": "flex", "gap": "12px", "marginTop": "12px"}, children=[
            html.Div([
                html.Div("Height (m)", style=_FORM_LABEL),
                dcc.Input(id="creator-height", type="number",
                          value=1.0, min=0.1, max=100, step=0.1,
                          style={"width": "100%", "padding": "6px", "borderRadius": "4px",
                                 "border": "1px solid #555", "backgroundColor": "#1a1a2e",
                                 "color": "#fff"}),
            ], style={"flex": "1"}),
            html.Div([
                html.Div("Weight (kg)", style=_FORM_LABEL),
                dcc.Input(id="creator-weight", type="number",
                          value=50.0, min=0.1, max=9999, step=0.1,
                          style={"width": "100%", "padding": "6px", "borderRadius": "4px",
                                 "border": "1px solid #555", "backgroundColor": "#1a1a2e",
                                 "color": "#fff"}),
            ], style={"flex": "1"}),
        ]),
        html.Div("Legendary?", style={**_FORM_LABEL, "marginTop": "18px"}),
        dcc.RadioItems(id="creator-legendary",
                       options=["Yes", "No"], value="No", inline=True,
                       labelStyle={"color": "#ccc", "marginRight": "16px"}),
        html.Button("Reset All", id="creator-reset",
                    style={"marginTop": "20px", "width": "100%", "padding": "10px",
                           "backgroundColor": "#6390F0", "color": "#fff",
                           "border": "none", "borderRadius": "6px",
                           "fontSize": "0.95rem", "fontWeight": "bold",
                           "cursor": "pointer"}),
        html.Hr(style={"borderColor": "#444", "marginTop": "16px"}),
        html.Div(id="creator-summary",
                 style={"color": "#ccc", "fontSize": "14px", "marginTop": "8px"}),
    ], style={"backgroundColor": "#252540", "padding": "20px",
              "borderRadius": "10px", "border": "1px solid #3a3a5c"})


def _build_creator_charts(name, type1, type2, hp, atk, dfn, spd, spatk, spdef,
                          height_m, weight_kg, dataset_df):
    """Build the 4 comparison charts for a custom Pokemon."""
    stats = [hp, atk, dfn, spd, spatk, spdef]
    stat_total = sum(stats)
    custom_bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0
    stat_labels = STAT_COLS
    has_type2 = type2 and type2 != "None"

    # ── Radar overlay (2c style: Type 2 dark behind, Type 1 light on top) ──
    radar = go.Figure()

    # Type 2 FIRST (behind): dark shade, 0.72 opacity, thick white border
    if has_type2:
        t2_mask = dataset_df["Type 2"] == type2
        t2_means = dataset_df.loc[t2_mask, STAT_COLS].mean().tolist() if t2_mask.any() else [80]*6
        radar.add_trace(go.Scatterpolar(
            r=t2_means + [t2_means[0]], theta=stat_labels + [stat_labels[0]],
            fill="toself", fillcolor=TYPE_COLORS_DARK.get(type2, "#444"),
            opacity=0.72, line=dict(color="white", width=3),
            name=f"{type2} Avg (Type 2)",
        ))

    # Type 1 SECOND (on top): light shade, 0.45 opacity, thick black border
    t1_mask = dataset_df["Type 1"] == type1
    t1_means = dataset_df.loc[t1_mask, STAT_COLS].mean().tolist() if t1_mask.any() else [80]*6
    radar.add_trace(go.Scatterpolar(
        r=t1_means + [t1_means[0]], theta=stat_labels + [stat_labels[0]],
        fill="toself", fillcolor=TYPE_COLORS_LIGHT.get(type1, "#aaa"),
        opacity=0.45, line=dict(color="black", width=3),
        name=f"{type1} Avg (Type 1)",
    ))

    # Custom Pokemon on top of both: red line, white fill
    radar.add_trace(go.Scatterpolar(
        r=stats + [stats[0]], theta=stat_labels + [stat_labels[0]],
        fill="toself", fillcolor="rgba(255,77,77,0.12)",
        line=dict(color="#ff4d4d", width=3), name=name,
    ))

    title_suffix = f" / {type2}" if has_type2 else ""
    radar.update_layout(
        title=f"{name} vs. {type1}{title_suffix}-type Averages",
        template=TEMPLATE, height=450,
        polar=dict(radialaxis=dict(visible=True, range=[0, 260], color="#aaa"),
                   bgcolor="rgba(0,0,0,0)"),
        legend=dict(font=dict(color="#ccc")), margin=dict(t=60, b=30),
    )

    # ── BST Histogram with marker ────────────────────────────────────
    hist = go.Figure()
    hist.add_trace(go.Histogram(
        x=dataset_df["Stat Total"], nbinsx=50,
        marker_color="#636EFA", opacity=0.75, name="All Pokemon",
    ))
    hist.add_vline(x=stat_total, line_width=3, line_color="red")
    hist.add_annotation(
        x=stat_total, y=1, yref="paper",
        text=f"{name}<br>BST {stat_total}",
        showarrow=True, arrowhead=2, arrowcolor="red",
        font=dict(color="#fff", size=13),
        bgcolor="rgba(0,0,0,0.6)", bordercolor="red",
    )
    hist.update_layout(
        title=f"Where {name} Falls (BST = {stat_total})",
        xaxis_title="Base Stat Total", yaxis_title="Count",
        template=TEMPLATE, height=450, margin=dict(t=60, b=40),
    )

    # ── Speed vs Bulk scatter ────────────────────────────────────────
    bulk = dataset_df["HP"] + dataset_df["Defense"] + dataset_df["Special Defense"]
    scatter = go.Figure()
    for t in sorted(dataset_df["Type 1"].unique()):
        mask = dataset_df["Type 1"] == t
        scatter.add_trace(go.Scatter(
            x=dataset_df.loc[mask, "Speed"], y=bulk[mask],
            mode="markers", marker=dict(size=5, color=TYPE_COLORS.get(t, "#888"), opacity=0.5),
            name=t, legendgroup=t,
        ))
    custom_bulk = hp + dfn + spdef
    scatter.add_trace(go.Scatter(
        x=[spd], y=[custom_bulk], mode="markers+text",
        marker=dict(size=20, color="red", symbol="star",
                    line=dict(color="white", width=2)),
        text=[name], textposition="top center",
        textfont=dict(color="#fff", size=13), name=name,
    ))
    scatter.update_layout(
        title=f"{name} in Speed-Bulk Space",
        xaxis_title="Speed", yaxis_title="Bulk (HP + Def + SpDef)",
        template=TEMPLATE, height=450, margin=dict(t=60, b=40),
        legend=dict(font=dict(size=10)),
    )

    # ── BMI comparison histogram ─────────────────────────────────────
    bmi_fig = go.Figure()
    bmi_data = dataset_df["BMI"].dropna()
    # Clip extreme outliers for readability (like Cosmoem at ~100k)
    bmi_clipped = bmi_data[bmi_data < 200]
    bmi_fig.add_trace(go.Histogram(
        x=bmi_clipped, nbinsx=50,
        marker_color="#7AC74C", opacity=0.75, name="All Pokemon (BMI < 200)",
    ))
    bmi_fig.add_vline(x=custom_bmi, line_width=3, line_color="red")
    bmi_fig.add_annotation(
        x=custom_bmi, y=1, yref="paper",
        text=f"{name}<br>BMI {custom_bmi:.1f}",
        showarrow=True, arrowhead=2, arrowcolor="red",
        font=dict(color="#fff", size=13),
        bgcolor="rgba(0,0,0,0.6)", bordercolor="red",
    )
    bmi_fig.update_layout(
        title=f"{name} BMI Comparison ({height_m}m, {weight_kg}kg → BMI {custom_bmi:.1f})",
        xaxis_title="BMI", yaxis_title="Count",
        template=TEMPLATE, height=450, margin=dict(t=60, b=40),
    )

    # Row 1: Radar + BST histogram side by side
    # Row 2: BMI comparison + Speed-Bulk scatter
    return html.Div([
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=radar, style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(figure=hist, style={"flex": "1", "minWidth": "400px"}),
        ]),
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=bmi_fig, style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(figure=scatter, style={"flex": "1", "minWidth": "400px"}),
        ]),
    ])


def _build_creator_tab():
    """Full Pokemon Creator tab layout."""
    return html.Div([
        html.Div(_creator_form(),
                 style={"width": "28%", "display": "inline-block",
                        "verticalAlign": "top", "padding": "12px"}),
        html.Div(id="creator-charts",
                 style={"width": "70%", "display": "inline-block",
                        "verticalAlign": "top", "padding": "12px"}),
    ])


# ── Creator callback ────────────────────────────────────────────────────
@app.callback(
    [Output("creator-charts", "children"),
     Output("creator-summary", "children")],
    [Input("creator-name", "value"),
     Input("creator-type", "value"),
     Input("creator-type2", "value"),
     Input("creator-hp", "value"),
     Input("creator-attack", "value"),
     Input("creator-defense", "value"),
     Input("creator-speed", "value"),
     Input("creator-spatk", "value"),
     Input("creator-spdef", "value"),
     Input("creator-height", "value"),
     Input("creator-weight", "value"),
     Input("creator-legendary", "value")],
)
def update_creator(name, type1, type2, hp, atk, dfn, spd, spatk, spdef,
                   height_m, weight_kg, legendary):
    name     = name     or "MyPokemon"
    type1    = type1    or "Fire"
    type2    = type2    or "None"
    hp       = hp       or 80
    atk      = atk      or 80
    dfn      = dfn      or 80
    spd      = spd      or 80
    spatk    = spatk    or 80
    spdef    = spdef    or 80
    height_m = height_m or 1.0
    weight_kg = weight_kg or 50.0

    stat_total = hp + atk + dfn + spd + spatk + spdef
    stat_std = float(np.std([hp, atk, dfn, spd, spatk, spdef], ddof=0))
    role = _classify_role(hp, atk, dfn, spd, spatk, spdef)
    bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0

    charts = _build_creator_charts(name, type1, type2, hp, atk, dfn, spd, spatk, spdef,
                                   height_m, weight_kg, df)

    summary = html.Div([
        html.Span("Stat Total: ", style={"color": "#aaa"}),
        html.Span(f"{stat_total}", style={"color": "#fff", "fontWeight": "bold", "fontSize": "18px"}),
        html.Br(),
        html.Span("Std Dev: ", style={"color": "#aaa"}),
        html.Span(f"{stat_std:.1f}", style={"color": "#fff", "fontWeight": "bold"}),
        html.Br(),
        html.Span("BMI: ", style={"color": "#aaa"}),
        html.Span(f"{bmi:.1f}", style={"color": "#fff", "fontWeight": "bold"}),
        html.Br(),
        html.Span("Role: ", style={"color": "#aaa"}),
        html.Span(role, style={"color": "#ffcc00", "fontWeight": "bold"}),
        html.Br(),
        html.Span("Legendary: ", style={"color": "#aaa"}),
        html.Span(legendary or "No", style={"color": "#fff", "fontWeight": "bold"}),
    ])
    return charts, summary


# ── Reset button callback ────────────────────────────────────────────────
@app.callback(
    [Output("creator-name", "value"),
     Output("creator-type", "value"),
     Output("creator-type2", "value"),
     Output("creator-hp", "value"),
     Output("creator-attack", "value"),
     Output("creator-defense", "value"),
     Output("creator-speed", "value"),
     Output("creator-spatk", "value"),
     Output("creator-spdef", "value"),
     Output("creator-height", "value"),
     Output("creator-weight", "value"),
     Output("creator-legendary", "value")],
    [Input("creator-reset", "n_clicks")],
    prevent_initial_call=True,
)
def reset_creator(_n):
    return "MyPokemon", "Fire", "None", 80, 80, 80, 80, 80, 80, 1.0, 50.0, "No"


# ---------------------------------------------------------------------------
# Main callback: filters -> KPIs + tab content
# ---------------------------------------------------------------------------
@app.callback(
    [
        Output("kpi-count", "children"),
        Output("kpi-bst", "children"),
        Output("kpi-speed", "children"),
        Output("kpi-bmi", "children"),
        Output("kpi-role", "children"),
        Output("kpi-legend-pct", "children"),
        Output("kpi-spec", "children"),
        Output("tab-content", "children"),
    ],
    [
        Input("gen-filter", "value"),
        Input("type-filter", "value"),
        Input("type2-filter", "value"),
        Input("role-filter", "value"),
        Input("legendary-filter", "value"),
        Input("tabs", "value"),
    ],
)
def update_dashboard(gens, types, types2, roles, legendary, active_tab):
    # ── Filter ────────────────────────────────────────────────────────
    filtered = df.copy()
    if gens:
        filtered = filtered[filtered["Generation"].isin(gens)]
    if types:
        filtered = filtered[filtered["Type 1"].isin(types)]
    if types2:
        filtered = filtered[filtered["Type 2"].isin(types2)]
    if roles:
        rule_roles = [r.split(":", 1)[1] for r in roles if r.startswith("rule:")]
        cluster_roles = [r.split(":", 1)[1] for r in roles if r.startswith("cluster:")]
        mask = pd.Series(False, index=filtered.index)
        if rule_roles:
            mask |= filtered["Role"].isin(rule_roles)
        if cluster_roles:
            mask |= filtered["Cluster Role"].isin(cluster_roles)
        filtered = filtered[mask]
    if legendary == "Legendary":
        filtered = filtered[filtered["Legendary"] == True]  # noqa: E712
    elif legendary == "Non-Legendary":
        filtered = filtered[filtered["Legendary"] == False]  # noqa: E712

    n = len(filtered)

    # ── KPIs ──────────────────────────────────────────────────────────
    kpi_count = f"{n:,}"
    kpi_bst = f"{filtered['Stat Total'].mean():.0f}" if n else "—"
    kpi_speed = f"{filtered['Speed'].mean():.0f}" if n else "—"
    kpi_bmi = f"{filtered['BMI'].mean():.1f}" if n else "—"
    kpi_role = filtered["Role"].mode().iloc[0] if n else "—"
    kpi_legend_pct = (
        f"{filtered['Legendary'].sum() / n * 100:.1f}%" if n else "—"
    )
    kpi_spec = f"{filtered['Stat Std Dev'].mean():.1f}" if n else "—"

    # ── Build tab content ─────────────────────────────────────────────
    if active_tab == "tab-overview":
        content = _build_overview(filtered)
    elif active_tab == "tab-type":
        content = _build_type_identity(filtered)
    elif active_tab == "tab-power":
        content = _build_power(filtered)
    elif active_tab == "tab-gen":
        content = _build_gen_trends(filtered)
    elif active_tab == "tab-evo":
        content = _build_evo_roles(filtered)
    elif active_tab == "tab-creator":
        content = _build_creator_tab()
    else:
        content = html.Div("Select a tab.")

    return kpi_count, kpi_bst, kpi_speed, kpi_bmi, kpi_role, kpi_legend_pct, kpi_spec, content


# ---------------------------------------------------------------------------
# Tab builders
# ---------------------------------------------------------------------------

def _build_overview(filt: pd.DataFrame) -> html.Div:
    """Overview tab — 3 charts: BST histogram, Role bar, Type bar."""
    tier_order = ["Low", "Mid", "High", "Very High"]
    fig_bst = px.histogram(
        filt, x="Stat Total", color="Stat Tier",
        category_orders={"Stat Tier": tier_order},
        template=TEMPLATE, title="BST Distribution",
        labels={"Stat Total": "Base Stat Total", "count": "Count"},
    )
    fig_bst.update_layout(bargap=0, legend_title_text="Stat Tier")

    role_counts = (
        filt["Role"].value_counts().reindex(ROLE_ORDER).dropna().reset_index()
    )
    role_counts.columns = ["Role", "Count"]
    fig_role = px.bar(
        role_counts, y="Role", x="Count", orientation="h",
        color="Role", color_discrete_map=ROLE_COLOR_MAP,
        category_orders={"Role": list(reversed(ROLE_ORDER))},
        template=TEMPLATE, title="Role Distribution",
    )
    fig_role.update_layout(showlegend=False)

    type_counts = filt["Type 1"].value_counts().reset_index()
    type_counts.columns = ["Type 1", "Count"]
    type_counts = type_counts.sort_values("Count", ascending=True)
    fig_type = px.bar(
        type_counts, y="Type 1", x="Count", orientation="h",
        color="Type 1", color_discrete_map=TYPE_COLORS,
        template=TEMPLATE, title="Type 1 Distribution",
    )
    fig_type.update_layout(showlegend=False)

    # Type 2 Distribution — only non-null Type 2 values
    t2_data = filt["Type 2"].dropna()
    type2_counts = t2_data.value_counts().reset_index()
    type2_counts.columns = ["Type 2", "Count"]
    type2_counts = type2_counts.sort_values("Count", ascending=True)
    fig_type2 = px.bar(
        type2_counts, y="Type 2", x="Count", orientation="h",
        color="Type 2", color_discrete_map=TYPE_COLORS,
        template=TEMPLATE, title="Type 2 Distribution",
    )
    fig_type2.update_layout(showlegend=False)

    return html.Div([
        dcc.Graph(figure=fig_bst),
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=fig_role, style={"flex": "1", "minWidth": "300px"}),
            dcc.Graph(figure=fig_type, style={"flex": "1", "minWidth": "300px"}),
            dcc.Graph(figure=fig_type2, style={"flex": "1", "minWidth": "300px"}),
        ]),
    ])


def _build_type_identity(filt: pd.DataFrame) -> html.Div:
    """Tab 2 — Type 1 radar, Type 2 radar, combat ratio profiles."""

    def _build_radar_grid(col_name, title):
        """Build a 2x3 radar grid for the top 6 types in the given column."""
        counts = filt[col_name].dropna().value_counts()
        top6 = counts.head(6).index.tolist()
        if len(top6) == 0:
            return _empty_fig(title)
        means = filt[filt[col_name].isin(top6)].groupby(col_name)[STAT_COLS].mean()
        n_types = len(top6)
        rows = (n_types + 2) // 3
        fig = make_subplots(
            rows=rows, cols=3,
            specs=[[{'type': 'polar'}] * 3] * rows,
            subplot_titles=top6,
        )
        for i, t in enumerate(top6):
            r_idx, c_idx = divmod(i, 3)
            vals = means.loc[t, STAT_COLS].tolist()
            vals_closed = vals + [vals[0]]
            theta = STAT_COLS + [STAT_COLS[0]]
            polar_key = 'polar' if i == 0 else f'polar{i + 1}'
            is_type2 = col_name == 'Type 2'
            fig.add_trace(
                go.Scatterpolar(
                    r=vals_closed, theta=theta, fill='toself',
                    fillcolor=TYPE_COLORS_DARK.get(t, '#444') if is_type2
                              else TYPE_COLORS_LIGHT.get(t, '#aaa'),
                    opacity=0.72 if is_type2 else 0.45,
                    line=dict(color='white' if is_type2 else 'black', width=3),
                    name=t, showlegend=False,
                ),
                row=r_idx + 1, col=c_idx + 1,
            )
            fig.update_layout(**{
                f'{polar_key}.bgcolor': 'rgba(0,0,0,0)',
                f'{polar_key}.angularaxis.gridcolor': 'rgba(255,255,255,0.2)',
                f'{polar_key}.radialaxis.gridcolor': 'rgba(255,255,255,0.2)',
            })
        fig.update_layout(template=TEMPLATE, title_text=title, height=500)
        return fig

    fig_radar_t1 = _build_radar_grid('Type 1', 'Stat Fingerprints — Top 6 Type 1s')
    fig_radar_t2 = _build_radar_grid('Type 2', 'Stat Fingerprints — Top 6 Type 2s')

    def _ratio_bar(col, title):
        med = filt.groupby('Type 1')[col].median().sort_values()
        types = med.index.tolist()
        colors = [TYPE_COLORS.get(t, '#888') for t in types]
        fig = go.Figure(go.Bar(x=med.values, y=types, orientation='h', marker_color=colors))
        fig.add_vline(x=1.0, line_dash='dash', line_color='red', line_width=2)
        fig.update_layout(template=TEMPLATE, title_text=title, height=700)
        return fig

    fig_phys = _ratio_bar('Physical/Special', 'Physical / Special Ratio by Type')
    fig_offdef = _ratio_bar('Offensive/Defensive', 'Offensive / Defensive Ratio by Type')

    return html.Div([
        dcc.Graph(figure=fig_radar_t1),
        dcc.Graph(figure=fig_radar_t2),
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=fig_phys, style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(figure=fig_offdef, style={"flex": "1", "minWidth": "400px"}),
        ]),
    ])


def _build_power(filt: pd.DataFrame) -> html.Div:
    """Tab 3 — Speed vs Bulk, Offense vs Bulk, Specialization vs Power."""

    def _scatter_ols(dff, x_col, y_col, color_col, title_tpl, hover_cols=None, color_map=None):
        x = dff[x_col].values.astype(float)
        y = dff[y_col].values.astype(float)
        mask = np.isfinite(x) & np.isfinite(y)
        xc, yc = x[mask], y[mask]
        r = np.corrcoef(xc, yc)[0, 1] if len(xc) > 1 else 0.0
        slope, intercept = np.polyfit(xc, yc, 1) if len(xc) > 1 else (0, 0)
        xr = np.linspace(xc.min(), xc.max(), 200) if len(xc) > 1 else np.array([0])
        fig = px.scatter(
            dff, x=x_col, y=y_col, color=color_col,
            hover_data=hover_cols, color_discrete_map=color_map,
            template=TEMPLATE, title=title_tpl.format(pearson_r=r),
        )
        fig.add_trace(go.Scatter(
            x=xr, y=slope * xr + intercept, mode='lines',
            line=dict(color='white', dash='dash', width=2),
            showlegend=False, name='OLS',
        ))
        fig.update_layout(height=700)
        return fig

    dff = filt.copy()
    dff['Bulk'] = dff['HP'] + dff['Defense'] + dff['Special Defense']
    dff['Gen_str'] = dff['Generation'].astype(str)
    hover = ['Pokemon', 'Type 1', 'Role', 'Stat Total']

    fig1 = _scatter_ols(dff, 'Speed', 'Bulk', 'Gen_str',
                        'Speed vs. Bulk (r = {pearson_r:.3f})', hover)
    fig1.update_layout(legend_title_text='Generation')

    fig2 = _scatter_ols(dff, 'Offensive Total', 'Bulk', 'Gen_str',
                        'Offense vs. Bulk (r = {pearson_r:.3f})', hover)
    fig2.update_layout(legend_title_text='Generation')

    tier_cm = {'Low': '#3b528b', 'Mid': '#21918c', 'High': '#5ec962', 'Very High': '#fde725'}
    fig3 = _scatter_ols(dff, 'Stat Total', 'Stat Std Dev', 'Stat Tier',
                        'Specialization vs. Power (r = {pearson_r:.3f})', color_map=tier_cm)
    fig3.update_layout(legend_title_text='Stat Tier')

    return html.Div([
        dcc.Graph(figure=fig1),
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=fig2, style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(figure=fig3, style={"flex": "1", "minWidth": "400px"}),
        ]),
    ])


def _build_gen_trends(filt: pd.DataFrame) -> html.Div:
    """Tab 4 — Offensive/Defensive balance, stat trends, BST boxes."""
    gen_means = filt.groupby('Generation').agg(
        off_mean=('Offensive Total', 'mean'),
        def_mean=('Defensive Total', 'mean'),
        ratio_mean=('Offensive/Defensive', 'mean'),
    ).sort_index()

    fig_od = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Mean Offensive & Defensive Totals", "Mean Off/Def Ratio"),
        horizontal_spacing=0.12,
    )
    fig_od.add_trace(go.Scatter(
        x=gen_means.index, y=gen_means['off_mean'], mode='lines+markers',
        name='Offensive Total', line=dict(color='#FC8D62', width=3),
    ), row=1, col=1)
    fig_od.add_trace(go.Scatter(
        x=gen_means.index, y=gen_means['def_mean'], mode='lines+markers',
        name='Defensive Total', line=dict(color='#66C2A5', width=3),
    ), row=1, col=1)
    fig_od.add_trace(go.Scatter(
        x=gen_means.index, y=gen_means['ratio_mean'], mode='lines+markers',
        name='Off/Def Ratio', line=dict(color='#8DA0CB', width=3),
    ), row=1, col=2)
    fig_od.add_hline(y=1.0, line_dash='dash', line_color='red', line_width=2, row=1, col=2)
    fig_od.update_xaxes(title_text='Generation', dtick=1)
    fig_od.update_layout(
        title='Offensive vs. Defensive Balance by Generation',
        template=TEMPLATE, height=500,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
    )

    stat_gen = filt.groupby('Generation')[STAT_COLS].mean().sort_index()
    fig_stats = make_subplots(rows=2, cols=3, subplot_titles=STAT_COLS,
                              vertical_spacing=0.15, horizontal_spacing=0.08)
    y_min = stat_gen.values.min() * 0.85
    y_max = stat_gen.values.max() * 1.10
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#a65628']
    for i, stat in enumerate(STAT_COLS):
        r, c = i // 3 + 1, i % 3 + 1
        fig_stats.add_trace(go.Scatter(
            x=stat_gen.index, y=stat_gen[stat], mode='lines+markers',
            line=dict(color=colors[i], width=2), showlegend=False,
        ), row=r, col=c)
        fig_stats.update_xaxes(title_text='Gen', dtick=1, row=r, col=c)
        fig_stats.update_yaxes(range=[y_min, y_max], row=r, col=c)
    fig_stats.update_layout(title='Individual Stat Trends by Generation',
                            template=TEMPLATE, height=600)

    overall_mean = filt['Stat Total'].mean()
    filt_box = filt.copy()
    filt_box['Gen_str'] = filt_box['Generation'].astype(str)
    fig_box = px.box(
        filt_box.sort_values('Generation'), x='Gen_str', y='Stat Total',
        color='Gen_str', template=TEMPLATE,
        title='Stat Total Distribution by Generation',
    )
    fig_box.add_hline(y=overall_mean, line_dash='dash', line_color='red', line_width=2,
                      annotation_text=f'Mean: {overall_mean:.0f}')
    fig_box.update_layout(height=500, showlegend=False,
                          xaxis_title='Generation', yaxis_title='BST')

    return html.Div([
        dcc.Graph(figure=fig_od),
        dcc.Graph(figure=fig_stats),
        dcc.Graph(figure=fig_box),
    ])


def _build_evo_roles(filt: pd.DataFrame) -> html.Div:
    """Tab 5 — Role by evo stage, mean stats by stage, legendary % by gen."""
    evo_df = filt[filt['Evolution Stage'].isin([1, 2, 3])].copy()
    evo_df['Evolution Stage'] = evo_df['Evolution Stage'].astype(int)

    # --- Created (rule-based) Role Distribution by Evolution Stage ---
    fig_role = go.Figure()
    role_evo = evo_df.groupby(['Evolution Stage', 'Role']).size().reset_index(name='Count')
    for role in ROLE_ORDER:
        sub = role_evo[role_evo['Role'] == role]
        fig_role.add_trace(go.Bar(
            x=sub['Evolution Stage'], y=sub['Count'],
            name=role, marker_color=ROLE_COLOR_MAP[role],
        ))
    fig_role.update_layout(
        barmode='stack', title='Created Role Distribution by Evolution Stage',
        xaxis=dict(title='Evolution Stage', tickmode='array', tickvals=[1, 2, 3]),
        yaxis_title='Count', template=TEMPLATE, height=500,
        legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
    )

    # --- Cluster Role Distribution by Evolution Stage ---
    # Generate a color palette for the 14 clusters
    _cluster_colors = px.colors.qualitative.Dark24[:14]
    _cluster_color_map = {name: _cluster_colors[i % len(_cluster_colors)]
                          for i, name in enumerate(sorted(CLUSTER_NAMES.values()))}
    fig_cluster_role = go.Figure()
    cluster_evo = (evo_df[evo_df['Cluster Role'] != 'Unassigned']
                   .groupby(['Evolution Stage', 'Cluster Role'])
                   .size().reset_index(name='Count'))
    for cname in sorted(CLUSTER_NAMES.values()):
        sub = cluster_evo[cluster_evo['Cluster Role'] == cname]
        fig_cluster_role.add_trace(go.Bar(
            x=sub['Evolution Stage'], y=sub['Count'],
            name=cname, marker_color=_cluster_color_map.get(cname, '#888'),
        ))
    fig_cluster_role.update_layout(
        barmode='stack', title='Cluster Role Distribution by Evolution Stage',
        xaxis=dict(title='Evolution Stage', tickmode='array', tickvals=[1, 2, 3]),
        yaxis_title='Count', template=TEMPLATE, height=500,
        legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5,
                    font=dict(size=9)),
    )

    stat_evo = evo_df.groupby('Evolution Stage')[STAT_COLS].mean()
    stage_colors = {1: '#636EFA', 2: '#EF553B', 3: '#00CC96'}
    fig_stat_evo = go.Figure()
    for stage in sorted(stat_evo.index):
        fig_stat_evo.add_trace(go.Bar(
            x=STAT_COLS, y=stat_evo.loc[stage].values,
            name=f'Stage {stage}', marker_color=stage_colors.get(stage, '#AB63FA'),
        ))
    fig_stat_evo.update_layout(
        barmode='group', title='Mean Stats by Evolution Stage',
        xaxis_title='Stat', yaxis_title='Mean Value',
        template=TEMPLATE, height=500,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
    )

    leg_pct = (
        filt.groupby('Generation')['Legendary']
        .apply(lambda s: s.sum() / len(s) * 100)
        .reset_index(name='Legendary %')
        .sort_values('Generation')
    )
    fig_leg = go.Figure(go.Bar(
        x=leg_pct['Generation'], y=leg_pct['Legendary %'],
        marker_color='#FFD92F',
        text=leg_pct['Legendary %'].round(1).astype(str) + '%',
        textposition='outside',
    ))
    fig_leg.update_layout(
        title='Legendary Percentage by Generation',
        xaxis=dict(title='Generation', dtick=1),
        yaxis=dict(title='Legendary %',
                   range=[0, leg_pct['Legendary %'].max() * 1.25 if len(leg_pct) else 50]),
        template=TEMPLATE, height=500,
    )

    return html.Div([
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=fig_role, style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(figure=fig_cluster_role, style={"flex": "1", "minWidth": "400px"}),
        ]),
        html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=[
            dcc.Graph(figure=fig_stat_evo, style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(figure=fig_leg, style={"flex": "1", "minWidth": "400px"}),
        ]),
    ])


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
