"""
Dashboard Analytics PrestaShop Addons
=====================================
Analyse des modules du marketplace pour identifier les opportunités de développement.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from data_loader import load_modules
from metrics import (calculate_metrics, get_category_stats, get_top_modules, 
                     get_opportunities, get_global_kpis, get_advanced_stats, 
                     get_trimmed_comparison, get_category_advanced_stats, trimmed_mean,
                     get_age_stats, get_age_stats_paid_only, get_age_bucket,
                     get_keyword_stats, get_keyword_opportunities, get_modules_by_keyword,
                     get_publisher_stats, get_publisher_stats_paid_only, get_top_publishers,
                     get_language_stats, get_languages_count_stats,
                     get_prestashop_version_stats, get_last_update_stats, get_addon_version_stats)
from sales_estimation import display_estimation_results, update_df_with_estimation

# Configuration de la page
st.set_page_config(
    page_title="PrestaShop Addons Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .stMetric > div {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Charge et prépare les données (avec cache)."""
    df = load_modules()
    df = calculate_metrics(df)
    return df


def format_currency(value):
    """Formate un nombre en euros."""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M €"
    elif value >= 1_000:
        return f"{value/1_000:.1f}k €"
    else:
        return f"{value:.0f} €"


def format_number(value):
    """Formate un nombre avec séparateurs."""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}k"
    else:
        return f"{value:.0f}"


# Chargement des données
df = load_data()
kpis = get_global_kpis(df)
category_stats = get_category_stats(df)

# Sidebar
st.sidebar.title("🔍 Filtres")

# =============================================================================
# FILTRES DE BASE
# =============================================================================
st.sidebar.subheader("Filtres de base")

# Filtre par catégorie
categories = ['Toutes'] + sorted(df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Catégorie", categories)

# Filtre par type (gratuit/payant)
price_filter = st.sidebar.radio("Type de module", ["Tous", "Payants uniquement", "Gratuits uniquement"])

# Filtre par note minimum
min_rating = st.sidebar.slider("Note minimum", 0.0, 5.0, 0.0, 0.5)

# =============================================================================
# FILTRES AVANCÉS
# =============================================================================
st.sidebar.divider()
st.sidebar.subheader("🎚️ Filtres avancés")

# Downloads range
max_downloads_data = int(df['downloads'].max())
st.sidebar.markdown("**Downloads**")
dl_col1, dl_col2 = st.sidebar.columns(2)
with dl_col1:
    downloads_min = st.number_input(
        "Min",
        min_value=0,
        max_value=max_downloads_data,
        value=0,
        step=100,
        key="dl_min"
    )
with dl_col2:
    downloads_max = st.number_input(
        "Max",
        min_value=0,
        max_value=max_downloads_data,
        value=max_downloads_data,
        step=100,
        key="dl_max"
    )
downloads_range = (downloads_min, downloads_max)

# Prix range
max_price_data = int(df['price'].max())
st.sidebar.markdown("**Prix (€)**")
price_col1, price_col2 = st.sidebar.columns(2)
with price_col1:
    price_min = st.number_input(
        "Min",
        min_value=0,
        max_value=max_price_data,
        value=0,
        step=10,
        key="price_min"
    )
with price_col2:
    price_max = st.number_input(
        "Max",
        min_value=0,
        max_value=max_price_data,
        value=max_price_data,
        step=10,
        key="price_max"
    )
price_range = (price_min, price_max)

# Age du module (mois)
max_age = int(df['mois_depuis_publication'].max()) if df['mois_depuis_publication'].notna().any() else 120
st.sidebar.markdown("**Âge du module (mois)**")
age_col1, age_col2 = st.sidebar.columns(2)
with age_col1:
    age_min = st.number_input(
        "Min",
        min_value=0,
        max_value=max_age,
        value=0,
        step=1,
        key="age_min"
    )
with age_col2:
    age_max = st.number_input(
        "Max",
        min_value=0,
        max_value=max_age,
        value=max_age,
        step=1,
        key="age_max"
    )
age_range = (age_min, age_max)

# Minimum d'avis
st.sidebar.markdown("**Avis**")
min_reviews = st.sidebar.number_input(
    "Minimum d'avis",
    min_value=0,
    max_value=1000,
    value=0,
    step=1,
    help="Exclure les modules avec moins d'avis"
)

# Exclusions
st.sidebar.divider()
st.sidebar.subheader("🚫 Exclusions")

exclude_prestashop_official = st.sidebar.checkbox(
    "Exclure PrestaShop officiel",
    value=False,
    help="Exclure les modules de PrestaShop et PrestaShop Partners"
)

exclude_no_reviews = st.sidebar.checkbox(
    "Exclure modules sans avis",
    value=False,
    help="Exclure les modules qui n'ont aucun avis"
)

# =============================================================================
# APPLIQUER TOUS LES FILTRES
# =============================================================================
filtered_df = df.copy()

# Filtres de base
if selected_category != 'Toutes':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if price_filter == "Payants uniquement":
    filtered_df = filtered_df[filtered_df['price'] > 0]
elif price_filter == "Gratuits uniquement":
    filtered_df = filtered_df[filtered_df['price'] == 0]
if min_rating > 0:
    filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

# Filtres avancés
filtered_df = filtered_df[
    (filtered_df['downloads'] >= downloads_range[0]) & 
    (filtered_df['downloads'] <= downloads_range[1])
]
filtered_df = filtered_df[
    (filtered_df['price'] >= price_range[0]) & 
    (filtered_df['price'] <= price_range[1])
]
filtered_df = filtered_df[
    (filtered_df['mois_depuis_publication'].isna()) |
    ((filtered_df['mois_depuis_publication'] >= age_range[0]) & 
     (filtered_df['mois_depuis_publication'] <= age_range[1]))
]
if min_reviews > 0:
    filtered_df = filtered_df[filtered_df['reviews_count'] >= min_reviews]

# Exclusions
if exclude_prestashop_official:
    filtered_df = filtered_df[
        ~filtered_df['publisher'].str.lower().str.contains('prestashop', na=False)
    ]
if exclude_no_reviews:
    filtered_df = filtered_df[filtered_df['reviews_count'] > 0]

# Afficher le nombre de modules après filtrage
st.sidebar.divider()
st.sidebar.metric("Modules filtrés", f"{len(filtered_df):,} / {len(df):,}")

# ============================================================================
# HEADER
# ============================================================================
st.title("📊 PrestaShop Addons Analytics")
st.markdown("*Analysez le marketplace pour identifier les meilleures opportunités de développement*")
st.divider()

# ============================================================================
# SECTION 1: KPIs GLOBAUX
# ============================================================================
st.header("🎯 Vue d'ensemble")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total modules", f"{kpis['total_modules']:,}")
with col2:
    st.metric("Modules payants", f"{kpis['modules_payants']:,}")
with col3:
    st.metric("CA total estimé", format_currency(kpis['ca_total']))
with col4:
    st.metric("Prix moyen", f"{kpis['prix_moyen_payants']:.0f} €")
with col5:
    st.metric("Note moyenne", f"{kpis['note_moyenne']:.1f}/5 ⭐")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Downloads totaux", format_number(kpis['downloads_total']))
with col2:
    st.metric("Catégories", kpis['nb_categories'])
with col3:
    st.metric("Éditeurs", kpis['nb_publishers'])
with col4:
    st.metric("CA/mois total", format_currency(kpis['ca_mois_total']))

st.divider()

# ============================================================================
# SECTION 2: ESTIMATION DES VENTES (< 100 ventes)
# ============================================================================
st.header("🔍 Estimation des Ventes pour Modules < 100")

st.markdown("""
*Les modules avec moins de 100 ventes sont tous marqués comme "0 vente". 
Cette section utilise la distribution des modules avec 100+ ventes pour estimer 
le nombre réel de ventes moyennes pour ces modules.*
""")

# Afficher les résultats d'estimation
estimated_mean = display_estimation_results(filtered_df)

st.divider()

# ============================================================================
# SECTION 3: STATISTIQUES AVANCÉES (Médianes, Trimmed Mean)
# ============================================================================
st.header("📈 Statistiques Avancées")

st.markdown("""
*Analyse robuste avec médianes et moyennes tronquées pour éviter le biais des gros modules.*
""")

# Slider pour le trim
trim_pct = st.slider(
    "Exclure les extrêmes (% de chaque côté)", 
    min_value=0, max_value=25, value=10, step=5,
    help="Exclut les X% modules les plus vendus et les X% les moins vendus pour avoir une moyenne plus représentative"
)

# Calculer les stats avancées
advanced_stats = get_advanced_stats(filtered_df, trim_pct)

tab_stats1, tab_stats2, tab_stats3, tab_stats4 = st.tabs([
    "📊 Comparaison Moyenne vs Médiane", 
    "📉 Distribution Percentiles",
    "🔄 Impact du Trimming",
    "📁 Stats par Catégorie"
])

with tab_stats1:
    st.subheader("Moyenne vs Médiane vs Trimmed Mean")
    st.markdown(f"*Trim actuel: {trim_pct}% de chaque côté exclus*")
    
    # Tableau comparatif
    if advanced_stats:
        comparison_data = []
        for col, stats in advanced_stats.items():
            if col in ['ca_estime', 'ca_par_mois', 'price', 'downloads', 'downloads_par_mois']:
                comparison_data.append({
                    'Métrique': stats['label'],
                    'Moyenne': f"{stats['moyenne']:,.0f}",
                    'Médiane': f"{stats['mediane']:,.0f}",
                    f'Trim {trim_pct}%': f"{stats['trimmed']:,.0f}",
                    'Écart moy/méd': f"{stats['ecart_pct']:+.0f}%"
                })
        
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
        
        # Graphique barres
        fig_compare = go.Figure()
        metrics_to_plot = ['ca_estime', 'ca_par_mois']
        for metric in metrics_to_plot:
            if metric in advanced_stats:
                s = advanced_stats[metric]
                fig_compare.add_trace(go.Bar(
                    name=s['label'],
                    x=['Moyenne', 'Médiane', f'Trim {trim_pct}%'],
                    y=[s['moyenne'], s['mediane'], s['trimmed']],
                    text=[f"{v:,.0f}€" for v in [s['moyenne'], s['mediane'], s['trimmed']]],
                    textposition='auto'
                ))
        
        fig_compare.update_layout(
            title="Comparaison des méthodes de calcul",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_compare, use_container_width=True)
        
        st.info(f"""
        **💡 Interprétation:**
        - **Écart élevé** (>100%) = distribution très asymétrique, quelques gros modules tirent la moyenne
        - **Médiane** = valeur d'un module "typique" (50% font moins, 50% font plus)
        - **Trim {trim_pct}%** = moyenne sans les extrêmes, bon compromis
        """)

with tab_stats2:
    st.subheader("Distribution par Percentiles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'ca_estime' in advanced_stats:
            s = advanced_stats['ca_estime']
            percentile_data = {
                'Percentile': ['P10', 'P25', 'P50 (Médiane)', 'P75', 'P90', 'P95', 'P99'],
                'CA Estimé (€)': [f"{s['p10']:,.0f}", f"{s['p25']:,.0f}", f"{s['p50']:,.0f}", 
                                 f"{s['p75']:,.0f}", f"{s['p90']:,.0f}", f"{s['p95']:,.0f}", f"{s['p99']:,.0f}"]
            }
            st.markdown("**CA Estimé**")
            st.dataframe(pd.DataFrame(percentile_data), use_container_width=True, hide_index=True)
    
    with col2:
        if 'ca_par_mois' in advanced_stats:
            s = advanced_stats['ca_par_mois']
            percentile_data = {
                'Percentile': ['P10', 'P25', 'P50 (Médiane)', 'P75', 'P90', 'P95', 'P99'],
                'CA/mois (€)': [f"{s['p10']:,.0f}", f"{s['p25']:,.0f}", f"{s['p50']:,.0f}", 
                               f"{s['p75']:,.0f}", f"{s['p90']:,.0f}", f"{s['p95']:,.0f}", f"{s['p99']:,.0f}"]
            }
            st.markdown("**CA par Mois**")
            st.dataframe(pd.DataFrame(percentile_data), use_container_width=True, hide_index=True)
    
    # Box plot
    paid_filtered = filtered_df[filtered_df['price'] > 0]
    if len(paid_filtered) > 0:
        fig_box = px.box(
            paid_filtered,
            y='ca_par_mois',
            title="Distribution CA/mois (Box Plot)",
            labels={'ca_par_mois': 'CA/mois (€)'}
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)

with tab_stats3:
    st.subheader("Impact du niveau de Trimming")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**CA Estimé**")
        trim_ca = get_trimmed_comparison(filtered_df, 'ca_estime')
        if len(trim_ca) > 0:
            trim_ca['Moyenne'] = trim_ca['Moyenne'].apply(lambda x: f"{x:,.0f}€")
            st.dataframe(trim_ca, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**CA/mois**")
        trim_ca_mois = get_trimmed_comparison(filtered_df, 'ca_par_mois')
        if len(trim_ca_mois) > 0:
            trim_ca_mois['Moyenne'] = trim_ca_mois['Moyenne'].apply(lambda x: f"{x:,.0f}€")
            st.dataframe(trim_ca_mois, use_container_width=True, hide_index=True)
    
    # Graphique évolution trim
    paid_filtered = filtered_df[filtered_df['price'] > 0]
    if len(paid_filtered) > 0:
        trim_values = []
        for t in range(0, 26, 5):
            trim_values.append({
                'Trim (%)': t,
                'CA moyen': trimmed_mean(paid_filtered['ca_estime'], t),
                'CA/mois moyen': trimmed_mean(paid_filtered['ca_par_mois'], t)
            })
        
        trim_df = pd.DataFrame(trim_values)
        
        fig_trim = px.line(
            trim_df, x='Trim (%)', y=['CA moyen', 'CA/mois moyen'],
            title="Évolution des moyennes selon le niveau de trimming",
            labels={'value': 'Valeur (€)', 'variable': 'Métrique'}
        )
        fig_trim.update_layout(height=400)
        st.plotly_chart(fig_trim, use_container_width=True)

with tab_stats4:
    st.subheader("Catégories par CA/mois Médian")
    st.markdown("*Classement plus fiable que la moyenne, moins biaisé par les outliers*")
    
    cat_advanced = get_category_advanced_stats(filtered_df)
    if len(cat_advanced) > 0:
        display_cat = cat_advanced[['category', 'nb_modules', 'ca_mois_median', 'ca_mois_moyen', 
                                    'ca_median', 'ca_moyen', 'prix_median', 'note_moy']].copy()
        display_cat.columns = ['Catégorie', 'Modules', 'CA/mois Médian', 'CA/mois Moyen',
                              'CA Médian', 'CA Moyen', 'Prix Médian', 'Note']
        
        st.dataframe(display_cat.head(25), use_container_width=True, hide_index=True)
        
        # Bar chart médiane vs moyenne
        fig_cat = go.Figure()
        top_cats = cat_advanced.head(15)
        fig_cat.add_trace(go.Bar(
            name='CA/mois Médian',
            x=top_cats['category'],
            y=top_cats['ca_mois_median'],
            marker_color='#667eea'
        ))
        fig_cat.add_trace(go.Bar(
            name='CA/mois Moyen',
            x=top_cats['category'],
            y=top_cats['ca_mois_moyen'],
            marker_color='#764ba2'
        ))
        fig_cat.update_layout(
            title="Top 15 Catégories: CA/mois Médian vs Moyen",
            barmode='group',
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# ============================================================================
# SECTION 4: ANALYSE PAR ÂGE
# ============================================================================
st.header("📅 Analyse par Âge des Modules")

st.markdown("""
*Comprendre comment les ventes évoluent selon l'ancienneté des modules. 
Identifiez le "sweet spot" : l'âge optimal pour maximiser le CA/mois.*
""")

tab_age1, tab_age2, tab_age3 = st.tabs([
    "📊 Stats par Tranche d'Âge",
    "📈 Graphiques",
    "🎯 Sweet Spot Analysis"
])

with tab_age1:
    st.subheader("Statistiques par tranche d'âge (modules payants)")
    
    age_stats_paid = get_age_stats_paid_only(filtered_df)
    
    if len(age_stats_paid) > 0:
        display_age = age_stats_paid[[
            'age_bucket', 'nb_modules', 'prix_moyen', 'prix_median',
            'ca_mois_moyen', 'ca_mois_median', 'dl_mois_moyen', 'note_moyenne'
        ]].copy()
        display_age.columns = [
            'Tranche d\'âge', 'Modules', 'Prix moyen (€)', 'Prix médian (€)',
            'CA/mois moyen (€)', 'CA/mois médian (€)', 'DL/mois moyen', 'Note moy.'
        ]
        st.dataframe(display_age, use_container_width=True, hide_index=True)
        
        # Stats globales
        age_stats_all = get_age_stats(filtered_df)
        if len(age_stats_all) > 0:
            st.subheader("Statistiques globales (tous modules)")
            display_all = age_stats_all[[
                'age_bucket', 'nb_modules', 'nb_payants', 'nb_gratuits', 'pct_payants',
                'downloads_total', 'ca_total', 'note_moyenne'
            ]].copy()
            display_all.columns = [
                'Tranche d\'âge', 'Total', 'Payants', 'Gratuits', '% Payants',
                'Downloads total', 'CA total (€)', 'Note moy.'
            ]
            st.dataframe(display_all, use_container_width=True, hide_index=True)
    else:
        st.info("Pas assez de données après filtrage.")

with tab_age2:
    age_stats_paid = get_age_stats_paid_only(filtered_df)
    
    if len(age_stats_paid) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart CA/mois médian par âge
            fig_age_ca = px.bar(
                age_stats_paid,
                x='age_bucket',
                y='ca_mois_median',
                title="CA/mois médian par tranche d'âge",
                labels={'age_bucket': 'Âge du module', 'ca_mois_median': 'CA/mois médian (€)'},
                color='ca_mois_median',
                color_continuous_scale='Viridis'
            )
            fig_age_ca.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_age_ca, use_container_width=True)
        
        with col2:
            # Bar chart Downloads/mois par âge
            fig_age_dl = px.bar(
                age_stats_paid,
                x='age_bucket',
                y='dl_mois_median',
                title="Downloads/mois médian par tranche d'âge",
                labels={'age_bucket': 'Âge du module', 'dl_mois_median': 'Downloads/mois médian'},
                color='dl_mois_median',
                color_continuous_scale='Blues'
            )
            fig_age_dl.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_age_dl, use_container_width=True)
        
        # Graphique comparatif moyenne vs médiane
        fig_compare_age = go.Figure()
        fig_compare_age.add_trace(go.Bar(
            name='CA/mois Moyen',
            x=age_stats_paid['age_bucket'],
            y=age_stats_paid['ca_mois_moyen'],
            marker_color='#667eea'
        ))
        fig_compare_age.add_trace(go.Bar(
            name='CA/mois Médian',
            x=age_stats_paid['age_bucket'],
            y=age_stats_paid['ca_mois_median'],
            marker_color='#764ba2'
        ))
        fig_compare_age.update_layout(
            title="CA/mois: Moyenne vs Médiane par tranche d'âge",
            barmode='group',
            height=400,
            xaxis_title="Âge du module",
            yaxis_title="CA/mois (€)"
        )
        st.plotly_chart(fig_compare_age, use_container_width=True)
    else:
        st.info("Pas assez de données après filtrage.")

with tab_age3:
    st.subheader("🎯 Identification du Sweet Spot")
    
    age_stats_paid = get_age_stats_paid_only(filtered_df)
    
    if len(age_stats_paid) > 0:
        # Trouver le sweet spot (meilleur CA/mois médian)
        best_age = age_stats_paid.loc[age_stats_paid['ca_mois_median'].idxmax()]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "🏆 Meilleure tranche d'âge",
                best_age['age_bucket'],
                help="Tranche d'âge avec le CA/mois médian le plus élevé"
            )
        with col2:
            st.metric(
                "CA/mois médian",
                f"{best_age['ca_mois_median']:,.0f} €"
            )
        with col3:
            st.metric(
                "Modules dans cette tranche",
                f"{int(best_age['nb_modules'])}"
            )
        
        st.markdown("---")
        
        st.markdown("""
        **💡 Insights:**
        - Les modules **récents** (< 6 mois) ont souvent un bon CA/mois car ils sont dans leur phase de lancement
        - Les modules **établis** (1-2 ans) ont généralement une base d'utilisateurs stable
        - Les modules **anciens** (> 5 ans) peuvent avoir un CA/mois plus faible mais un CA total important
        
        **Stratégie recommandée:**
        - Analysez les modules dans la tranche optimale pour voir ce qui fonctionne
        - Les niches avec des modules anciens mal notés = opportunité de disruption
        """)
        
        # Top modules dans la meilleure tranche
        st.subheader(f"Top 10 modules dans la tranche '{best_age['age_bucket']}'")
        
        filtered_with_age = filtered_df.copy()
        filtered_with_age['age_bucket'] = filtered_with_age['mois_depuis_publication'].apply(get_age_bucket)
        best_age_modules = filtered_with_age[
            (filtered_with_age['age_bucket'] == best_age['age_bucket']) & 
            (filtered_with_age['price'] > 0)
        ].nlargest(10, 'ca_par_mois')
        
        if len(best_age_modules) > 0:
            display_best = best_age_modules[[
                'name', 'publisher', 'category', 'price', 'ca_par_mois', 
                'downloads_par_mois', 'rating', 'mois_depuis_publication'
            ]].copy()
            display_best.columns = [
                'Nom', 'Éditeur', 'Catégorie', 'Prix (€)', 'CA/mois (€)',
                'DL/mois', 'Note', 'Âge (mois)'
            ]
            st.dataframe(display_best, use_container_width=True, hide_index=True)
    else:
        st.info("Pas assez de données après filtrage.")

st.divider()

# ============================================================================
# SECTION 5: ANALYSE DES MOTS-CLÉS
# ============================================================================
st.header("🔤 Intelligence Mots-Clés")

st.markdown("""
*Analysez les mots-clés des descriptions pour identifier les thématiques rentables 
et les niches sous-exploitées.*
""")

tab_kw1, tab_kw2, tab_kw3, tab_kw4 = st.tabs([
    "📊 Top Mots-Clés par CA",
    "🎯 Opportunités Keywords",
    "🔍 Recherche par Mot-Clé",
    "☁️ Word Cloud"
])

with tab_kw1:
    st.subheader("Mots-clés les plus rentables")
    
    min_kw_occurrences = st.slider(
        "Occurrences minimum du mot-clé",
        min_value=3, max_value=50, value=10, step=1,
        help="Nombre minimum de modules contenant ce mot-clé"
    )
    
    keyword_stats = get_keyword_stats(filtered_df, min_occurrences=min_kw_occurrences, top_n=50)
    
    if len(keyword_stats) > 0:
        display_kw = keyword_stats[[
            'keyword', 'nb_modules', 'ca_mois_moyen', 'ca_mois_median',
            'prix_moyen', 'note_moyenne', 'categorie_principale'
        ]].copy()
        display_kw.columns = [
            'Mot-clé', 'Nb modules', 'CA/mois moy (€)', 'CA/mois méd (€)',
            'Prix moy (€)', 'Note moy', 'Catégorie principale'
        ]
        
        st.dataframe(display_kw, use_container_width=True, hide_index=True)
        
        # Graphique top 20 keywords
        top_20_kw = keyword_stats.head(20)
        fig_kw = px.bar(
            top_20_kw,
            x='keyword',
            y='ca_mois_moyen',
            title="Top 20 mots-clés par CA/mois moyen",
            labels={'keyword': 'Mot-clé', 'ca_mois_moyen': 'CA/mois moyen (€)'},
            color='nb_modules',
            color_continuous_scale='Viridis'
        )
        fig_kw.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_kw, use_container_width=True)
    else:
        st.info("Pas assez de données pour l'analyse des mots-clés.")

with tab_kw2:
    st.subheader("🎯 Opportunités: Mots-clés rentables avec peu de concurrence")
    
    st.markdown("""
    *Ces mots-clés ont un bon CA/mois moyen mais relativement peu de modules - 
    ce sont des niches potentiellement sous-exploitées.*
    """)
    
    kw_opportunities = get_keyword_opportunities(filtered_df, min_occurrences=5, top_n=30)
    
    if len(kw_opportunities) > 0:
        display_opp = kw_opportunities[[
            'keyword', 'nb_modules', 'ca_mois_moyen', 'ca_mois_median',
            'opportunite_score', 'note_moyenne', 'categorie_principale'
        ]].copy()
        display_opp.columns = [
            'Mot-clé', 'Nb modules', 'CA/mois moy (€)', 'CA/mois méd (€)',
            'Score opportunité', 'Note moy', 'Catégorie'
        ]
        
        st.dataframe(display_opp, use_container_width=True, hide_index=True)
        
        # Scatter: CA moyen vs Nombre de modules
        fig_scatter_kw = px.scatter(
            kw_opportunities,
            x='nb_modules',
            y='ca_mois_moyen',
            size='opportunite_score',
            color='opportunite_score',
            hover_name='keyword',
            title="Opportunités: CA/mois vs Concurrence",
            labels={
                'nb_modules': 'Nombre de modules (concurrence)',
                'ca_mois_moyen': 'CA/mois moyen (€)',
                'opportunite_score': 'Score opportunité'
            },
            color_continuous_scale='RdYlGn'
        )
        fig_scatter_kw.update_layout(height=500)
        st.plotly_chart(fig_scatter_kw, use_container_width=True)
        
        st.info("""
        **💡 Interprétation du scatter:**
        - **En haut à gauche** = Haute rentabilité + Peu de concurrence = 🎯 Opportunité idéale
        - **En bas à droite** = Faible rentabilité + Beaucoup de concurrence = ⚠️ À éviter
        """)
    else:
        st.info("Pas assez de données pour l'analyse des opportunités.")

with tab_kw3:
    st.subheader("🔍 Explorer les modules par mot-clé")
    
    search_keyword = st.text_input(
        "Rechercher un mot-clé",
        placeholder="ex: seo, export, facture, livraison...",
        help="Entrez un mot-clé pour voir tous les modules associés"
    )
    
    if search_keyword:
        modules_with_kw = get_modules_by_keyword(filtered_df, search_keyword)
        
        if len(modules_with_kw) > 0:
            st.success(f"**{len(modules_with_kw)} modules** contiennent le mot-clé '{search_keyword}'")
            
            # Stats résumées
            paid_kw = modules_with_kw[modules_with_kw['price'] > 0]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Modules payants", len(paid_kw))
            with col2:
                st.metric("CA/mois moyen", f"{paid_kw['ca_par_mois'].mean():,.0f} €" if len(paid_kw) > 0 else "N/A")
            with col3:
                st.metric("Prix moyen", f"{paid_kw['price'].mean():,.0f} €" if len(paid_kw) > 0 else "N/A")
            with col4:
                st.metric("Note moyenne", f"{modules_with_kw['rating'].mean():.1f}/5")
            
            # Liste des modules
            display_search = modules_with_kw[[
                'name', 'publisher', 'category', 'price', 'ca_par_mois',
                'downloads', 'rating', 'reviews_count'
            ]].head(50).copy()
            display_search.columns = [
                'Nom', 'Éditeur', 'Catégorie', 'Prix (€)', 'CA/mois (€)',
                'Downloads', 'Note', 'Avis'
            ]
            st.dataframe(display_search, use_container_width=True, hide_index=True)
        else:
            st.warning(f"Aucun module trouvé avec le mot-clé '{search_keyword}'")

with tab_kw4:
    st.subheader("☁️ Nuage de mots-clés")
    
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        
        keyword_stats = get_keyword_stats(filtered_df, min_occurrences=5, top_n=200)
        
        if len(keyword_stats) > 0:
            # Créer le dictionnaire pour le word cloud
            word_freq = dict(zip(keyword_stats['keyword'], keyword_stats['ca_mois_moyen']))
            
            # Générer le word cloud
            wc = WordCloud(
                width=1200, height=600,
                background_color='white',
                colormap='viridis',
                max_words=100,
                min_font_size=10
            ).generate_from_frequencies(word_freq)
            
            fig_wc, ax = plt.subplots(figsize=(15, 8))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Mots-clés pondérés par CA/mois moyen', fontsize=16, pad=20)
            st.pyplot(fig_wc)
            
            st.caption("*Plus le mot est grand, plus le CA/mois moyen des modules contenant ce mot est élevé.*")
        else:
            st.info("Pas assez de données pour générer le word cloud.")
    except ImportError:
        st.warning("⚠️ La librairie 'wordcloud' n'est pas installée. Installez-la avec: `pip install wordcloud`")

st.divider()

# ============================================================================
# SECTION 6: ANALYSE PAR CATÉGORIE
# ============================================================================
st.header("📁 Analyse par catégorie")

# Recalculer les stats par catégorie avec les données filtrées
category_stats_filtered = get_category_stats(filtered_df)

tab1, tab2, tab3 = st.tabs(["📊 CA par catégorie", "📈 Tableau détaillé", "🗺️ Treemap"])

with tab1:
    # Bar chart CA par catégorie
    fig_ca = px.bar(
        category_stats_filtered.head(20),
        x='ca_total',
        y='category',
        orientation='h',
        title="Top 20 catégories par CA estimé",
        labels={'ca_total': 'CA estimé (€)', 'category': 'Catégorie'},
        color='ca_total',
        color_continuous_scale='Viridis'
    )
    fig_ca.update_layout(
        height=600,
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    st.plotly_chart(fig_ca, use_container_width=True)

with tab2:
    # Tableau des stats par catégorie
    display_cols = ['category', 'nb_modules', 'nb_payants', 'prix_moyen', 
                    'ca_total', 'downloads_total', 'note_moyenne']
    st.dataframe(
        category_stats_filtered[display_cols].rename(columns={
            'category': 'Catégorie',
            'nb_modules': 'Modules',
            'nb_payants': 'Payants',
            'prix_moyen': 'Prix moyen (€)',
            'ca_total': 'CA total (€)',
            'downloads_total': 'Downloads',
            'note_moyenne': 'Note moy.'
        }),
        use_container_width=True,
        hide_index=True
    )

with tab3:
    # Treemap CA
    fig_treemap = px.treemap(
        category_stats_filtered[category_stats_filtered['ca_total'] > 0],
        path=['category'],
        values='ca_total',
        title="Répartition du CA par catégorie",
        color='ca_total',
        color_continuous_scale='RdYlGn'
    )
    fig_treemap.update_layout(height=600)
    st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()

# ============================================================================
# SECTION 7: ANALYSE PAR ÉDITEUR
# ============================================================================
st.header("👥 Analyse par Éditeur")

st.markdown("""
*Identifiez les éditeurs les plus performants, leurs stratégies de prix et leur portefeuille de modules.*
""")

# Paramètres
col_pub1, col_pub2 = st.columns(2)
with col_pub1:
    min_modules_publisher = st.number_input(
        "Minimum de modules par éditeur",
        min_value=1, max_value=20, value=2, step=1,
        help="Filtrer les éditeurs avec au moins X modules"
    )
with col_pub2:
    sort_publisher_by = st.selectbox(
        "Trier par",
        options=['ca_total', 'ca_mois_moyen', 'nb_modules', 'note_moyenne', 'prix_moyen'],
        format_func=lambda x: {
            'ca_total': 'CA Total',
            'ca_mois_moyen': 'CA/mois Moyen',
            'nb_modules': 'Nombre de modules',
            'note_moyenne': 'Note moyenne',
            'prix_moyen': 'Prix moyen'
        }.get(x, x)
    )

tab_pub1, tab_pub2, tab_pub3, tab_pub4 = st.tabs([
    "📊 Top Éditeurs",
    "📈 Stats Détaillées",
    "🔍 Recherche Éditeur",
    "📉 Comparaison"
])

with tab_pub1:
    st.subheader("🏆 Top Éditeurs par CA")
    
    publisher_stats = get_publisher_stats(filtered_df, min_modules=min_modules_publisher)
    
    if len(publisher_stats) > 0:
        # Trier selon le critère choisi
        publisher_stats_sorted = publisher_stats.sort_values(sort_publisher_by, ascending=False)
        
        # Top 20 bar chart
        top_20_pub = publisher_stats_sorted.head(20)
        fig_pub = px.bar(
            top_20_pub,
            x='publisher',
            y='ca_total',
            title=f"Top 20 Éditeurs par CA Total",
            labels={'publisher': 'Éditeur', 'ca_total': 'CA Total (€)'},
            color='nb_modules',
            color_continuous_scale='Viridis',
            hover_data=['nb_modules', 'prix_moyen', 'note_moyenne']
        )
        fig_pub.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig_pub, use_container_width=True)
        
        # Tableau
        display_pub = publisher_stats_sorted[[
            'publisher', 'nb_modules', 'nb_payants', 'prix_moyen',
            'ca_total', 'ca_mois_moyen', 'note_moyenne', 'avis_total'
        ]].head(30).copy()
        display_pub.columns = [
            'Éditeur', 'Modules', 'Payants', 'Prix moy (€)',
            'CA Total (€)', 'CA/mois moy (€)', 'Note moy', 'Avis'
        ]
        st.dataframe(display_pub, use_container_width=True, hide_index=True)
    else:
        st.info("Pas assez de données après filtrage.")

with tab_pub2:
    st.subheader("📈 Statistiques Détaillées par Éditeur (Payants)")
    
    publisher_stats_paid = get_publisher_stats_paid_only(filtered_df, min_modules=min_modules_publisher)
    
    if len(publisher_stats_paid) > 0:
        display_paid = publisher_stats_paid[[
            'publisher', 'nb_modules', 'prix_moyen', 'prix_median',
            'ca_total', 'ca_mois_moyen', 'ca_mois_median',
            'note_moyenne', 'categorie_principale'
        ]].head(50).copy()
        display_paid.columns = [
            'Éditeur', 'Modules', 'Prix moy (€)', 'Prix méd (€)',
            'CA Total (€)', 'CA/mois moy (€)', 'CA/mois méd (€)',
            'Note moy', 'Catégorie principale'
        ]
        st.dataframe(display_paid, use_container_width=True, hide_index=True)
        
        # Scatter: Prix moyen vs CA/mois
        fig_scatter_pub = px.scatter(
            publisher_stats_paid.head(50),
            x='prix_moyen',
            y='ca_mois_moyen',
            size='nb_modules',
            color='note_moyenne',
            hover_name='publisher',
            title="Prix Moyen vs CA/mois Moyen par Éditeur",
            labels={
                'prix_moyen': 'Prix Moyen (€)',
                'ca_mois_moyen': 'CA/mois Moyen (€)',
                'note_moyenne': 'Note'
            },
            color_continuous_scale='RdYlGn'
        )
        fig_scatter_pub.update_layout(height=500)
        st.plotly_chart(fig_scatter_pub, use_container_width=True)
    else:
        st.info("Pas assez de données après filtrage.")

with tab_pub3:
    st.subheader("🔍 Explorer un Éditeur")
    
    # Liste des éditeurs
    publishers_list = sorted(filtered_df['publisher'].dropna().unique().tolist())
    
    selected_publisher = st.selectbox(
        "Sélectionner un éditeur",
        options=[''] + publishers_list,
        format_func=lambda x: 'Choisir un éditeur...' if x == '' else x
    )
    
    if selected_publisher:
        pub_modules = filtered_df[filtered_df['publisher'] == selected_publisher]
        pub_paid = pub_modules[pub_modules['price'] > 0]
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total modules", len(pub_modules))
        with col2:
            st.metric("Modules payants", len(pub_paid))
        with col3:
            st.metric("CA Total", f"{pub_modules['ca_estime'].sum():,.0f} €")
        with col4:
            st.metric("Note moyenne", f"{pub_modules['rating'].mean():.1f}/5")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Prix moyen", f"{pub_paid['price'].mean():,.0f} €" if len(pub_paid) > 0 else "N/A")
        with col2:
            st.metric("CA/mois moyen", f"{pub_paid['ca_par_mois'].mean():,.0f} €" if len(pub_paid) > 0 else "N/A")
        with col3:
            st.metric("Downloads total", f"{pub_modules['downloads'].sum():,}")
        with col4:
            st.metric("Avis total", f"{pub_modules['reviews_count'].sum():,}")
        
        st.markdown("---")
        
        # Liste des modules
        st.markdown(f"**Modules de {selected_publisher}:**")
        display_pub_modules = pub_modules[[
            'name', 'category', 'price', 'ca_estime', 'ca_par_mois',
            'downloads', 'rating', 'reviews_count'
        ]].sort_values('ca_estime', ascending=False).copy()
        display_pub_modules.columns = [
            'Nom', 'Catégorie', 'Prix (€)', 'CA (€)', 'CA/mois (€)',
            'Downloads', 'Note', 'Avis'
        ]
        st.dataframe(display_pub_modules, use_container_width=True, hide_index=True)
        
        # Répartition par catégorie
        if len(pub_modules) > 1:
            cat_dist = pub_modules.groupby('category').size().reset_index(name='count')
            fig_cat_pub = px.pie(
                cat_dist,
                values='count',
                names='category',
                title=f"Répartition par catégorie - {selected_publisher}"
            )
            fig_cat_pub.update_layout(height=400)
            st.plotly_chart(fig_cat_pub, use_container_width=True)

with tab_pub4:
    st.subheader("📉 Comparer des Éditeurs")
    
    # Sélection multiple
    publishers_to_compare = st.multiselect(
        "Sélectionner des éditeurs à comparer",
        options=publishers_list,
        default=[],
        max_selections=5
    )
    
    if len(publishers_to_compare) >= 2:
        comparison_data = []
        for pub in publishers_to_compare:
            pub_data = filtered_df[filtered_df['publisher'] == pub]
            pub_paid = pub_data[pub_data['price'] > 0]
            comparison_data.append({
                'Éditeur': pub,
                'Modules': len(pub_data),
                'Payants': len(pub_paid),
                'CA Total (€)': pub_data['ca_estime'].sum(),
                'CA/mois moy (€)': pub_paid['ca_par_mois'].mean() if len(pub_paid) > 0 else 0,
                'Prix moy (€)': pub_paid['price'].mean() if len(pub_paid) > 0 else 0,
                'Note moy': pub_data['rating'].mean(),
                'Downloads': pub_data['downloads'].sum()
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Bar chart comparatif
        fig_compare_pub = go.Figure()
        for metric, color in [('CA Total (€)', '#667eea'), ('CA/mois moy (€)', '#764ba2')]:
            fig_compare_pub.add_trace(go.Bar(
                name=metric,
                x=comparison_df['Éditeur'],
                y=comparison_df[metric],
            ))
        fig_compare_pub.update_layout(
            title="Comparaison CA",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_compare_pub, use_container_width=True)
    elif len(publishers_to_compare) == 1:
        st.info("Sélectionnez au moins 2 éditeurs pour comparer.")
    else:
        st.info("Sélectionnez des éditeurs dans la liste ci-dessus.")

st.divider()

# ============================================================================
# SECTION 8: ANALYSE TECHNIQUE (Langues, Versions, Updates)
# ============================================================================
st.header("🔧 Analyse Technique")

st.markdown("""
*Analysez les modules par caractéristiques techniques : langues supportées, 
versions PrestaShop compatibles, fraîcheur des mises à jour.*
""")

tab_tech1, tab_tech2, tab_tech3, tab_tech4, tab_tech5 = st.tabs([
    "🌍 Langues",
    "🔢 Nb Langues",
    "🏷️ Version PS",
    "🔄 Dernière MAJ",
    "📦 Version Addon"
])

with tab_tech1:
    st.subheader("🌍 Statistiques par Langue")
    
    lang_stats = get_language_stats(filtered_df)
    
    if len(lang_stats) > 0:
        # Top langues bar chart
        fig_lang = px.bar(
            lang_stats.head(15),
            x='language',
            y='nb_modules',
            title="Top 15 Langues par nombre de modules",
            labels={'language': 'Langue', 'nb_modules': 'Nombre de modules'},
            color='ca_mois_moyen',
            color_continuous_scale='Viridis'
        )
        fig_lang.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_lang, use_container_width=True)
        
        # Tableau complet
        display_lang = lang_stats[[
            'language', 'nb_modules', 'nb_payants', 'prix_moyen',
            'ca_total', 'ca_mois_moyen', 'note_moyenne'
        ]].copy()
        display_lang.columns = [
            'Langue', 'Modules', 'Payants', 'Prix moy (€)',
            'CA Total (€)', 'CA/mois moy (€)', 'Note moy'
        ]
        st.dataframe(display_lang, use_container_width=True, hide_index=True)
        
        st.info("""
        **💡 Insight:** Les modules multilingues ont généralement un meilleur potentiel de vente. 
        Vérifiez si votre niche cible est bien couverte dans les langues principales (FR, EN, ES, DE, IT).
        """)
    else:
        st.info("Pas de données de langues disponibles.")

with tab_tech2:
    st.subheader("🔢 Statistiques par Nombre de Langues")
    
    lang_count_stats = get_languages_count_stats(filtered_df)
    
    if len(lang_count_stats) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            fig_lc = px.bar(
                lang_count_stats,
                x='lang_count_bucket',
                y='nb_modules',
                title="Distribution par nombre de langues",
                labels={'lang_count_bucket': 'Nb langues', 'nb_modules': 'Modules'},
                color='ca_mois_moyen',
                color_continuous_scale='Blues'
            )
            fig_lc.update_layout(height=400)
            st.plotly_chart(fig_lc, use_container_width=True)
        
        with col2:
            # CA/mois par nb langues
            fig_lc_ca = px.bar(
                lang_count_stats,
                x='lang_count_bucket',
                y='ca_mois_moyen',
                title="CA/mois moyen par nombre de langues",
                labels={'lang_count_bucket': 'Nb langues', 'ca_mois_moyen': 'CA/mois moy (€)'},
                color='ca_mois_moyen',
                color_continuous_scale='Greens'
            )
            fig_lc_ca.update_layout(height=400)
            st.plotly_chart(fig_lc_ca, use_container_width=True)
        
        # Tableau
        display_lc = lang_count_stats[[
            'lang_count_bucket', 'nb_modules', 'nb_payants', 'prix_moyen',
            'ca_mois_moyen', 'ca_mois_median', 'note_moyenne'
        ]].copy()
        display_lc.columns = [
            'Nb Langues', 'Modules', 'Payants', 'Prix moy (€)',
            'CA/mois moy (€)', 'CA/mois méd (€)', 'Note moy'
        ]
        st.dataframe(display_lc, use_container_width=True, hide_index=True)
    else:
        st.info("Pas de données disponibles.")

with tab_tech3:
    st.subheader("🏷️ Statistiques par Version PrestaShop Compatible")
    
    version_stats = get_prestashop_version_stats(filtered_df)
    
    if len(version_stats) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart répartition
            fig_ver_pie = px.pie(
                version_stats,
                values='nb_modules',
                names='version_bucket',
                title="Répartition par compatibilité PS"
            )
            fig_ver_pie.update_layout(height=400)
            st.plotly_chart(fig_ver_pie, use_container_width=True)
        
        with col2:
            # Bar chart CA/mois
            fig_ver_ca = px.bar(
                version_stats,
                x='version_bucket',
                y='ca_mois_moyen',
                title="CA/mois moyen par version PS",
                labels={'version_bucket': 'Version PS', 'ca_mois_moyen': 'CA/mois moy (€)'},
                color='ca_mois_moyen',
                color_continuous_scale='RdYlGn'
            )
            fig_ver_ca.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_ver_ca, use_container_width=True)
        
        # Tableau
        display_ver = version_stats[[
            'version_bucket', 'nb_modules', 'nb_payants', 'prix_moyen',
            'ca_total', 'ca_mois_moyen', 'note_moyenne'
        ]].copy()
        display_ver.columns = [
            'Version PS', 'Modules', 'Payants', 'Prix moy (€)',
            'CA Total (€)', 'CA/mois moy (€)', 'Note moy'
        ]
        st.dataframe(display_ver, use_container_width=True, hide_index=True)
        
        st.warning("""
        **⚠️ Attention:** Les modules compatibles uniquement PS 1.6 sont considérés comme legacy.
        Privilégiez les modules compatibles PS 8.x et 9.x pour un meilleur potentiel de vente.
        """)
    else:
        st.info("Pas de données de version disponibles.")

with tab_tech4:
    st.subheader("🔄 Statistiques par Fraîcheur de Mise à Jour")
    
    update_stats = get_last_update_stats(filtered_df)
    
    if len(update_stats) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart nb modules
            fig_upd = px.bar(
                update_stats,
                x='update_bucket',
                y='nb_modules',
                title="Distribution par dernière mise à jour",
                labels={'update_bucket': 'Dernière MAJ', 'nb_modules': 'Modules'},
                color='nb_modules',
                color_continuous_scale='Blues'
            )
            fig_upd.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_upd, use_container_width=True)
        
        with col2:
            # CA/mois par fraîcheur
            fig_upd_ca = px.bar(
                update_stats,
                x='update_bucket',
                y='ca_mois_moyen',
                title="CA/mois moyen par fraîcheur de MAJ",
                labels={'update_bucket': 'Dernière MAJ', 'ca_mois_moyen': 'CA/mois moy (€)'},
                color='ca_mois_moyen',
                color_continuous_scale='RdYlGn'
            )
            fig_upd_ca.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_upd_ca, use_container_width=True)
        
        # Tableau
        display_upd = update_stats[[
            'update_bucket', 'nb_modules', 'nb_payants', 'prix_moyen',
            'ca_mois_moyen', 'ca_mois_median', 'note_moyenne'
        ]].copy()
        display_upd.columns = [
            'Dernière MAJ', 'Modules', 'Payants', 'Prix moy (€)',
            'CA/mois moy (€)', 'CA/mois méd (€)', 'Note moy'
        ]
        st.dataframe(display_upd, use_container_width=True, hide_index=True)
        
        st.info("""
        **💡 Insight:** Les modules régulièrement mis à jour (< 6 mois) inspirent confiance aux acheteurs.
        Les modules non mis à jour depuis > 2 ans peuvent être des opportunités de disruption.
        """)
    else:
        st.info("Pas de données de mise à jour disponibles.")

with tab_tech5:
    st.subheader("📦 Statistiques par Version Majeure de l'Addon")
    
    addon_stats = get_addon_version_stats(filtered_df)
    
    if len(addon_stats) > 0:
        # Bar chart
        fig_addon = px.bar(
            addon_stats.head(15),
            x='version_major',
            y='nb_modules',
            title="Distribution par version majeure de l'addon",
            labels={'version_major': 'Version', 'nb_modules': 'Modules'},
            color='ca_mois_moyen',
            color_continuous_scale='Viridis'
        )
        fig_addon.update_layout(height=400)
        st.plotly_chart(fig_addon, use_container_width=True)
        
        # Tableau
        display_addon = addon_stats[[
            'version_major', 'nb_modules', 'nb_payants', 'prix_moyen',
            'ca_total', 'ca_mois_moyen', 'note_moyenne'
        ]].head(20).copy()
        display_addon.columns = [
            'Version', 'Modules', 'Payants', 'Prix moy (€)',
            'CA Total (€)', 'CA/mois moy (€)', 'Note moy'
        ]
        st.dataframe(display_addon, use_container_width=True, hide_index=True)
        
        st.caption("""
        *Les versions 1.x sont souvent des modules anciens ou simples. 
        Les versions 2.x+ indiquent généralement des modules plus matures avec plus de fonctionnalités.*
        """)
    else:
        st.info("Pas de données de version d'addon disponibles.")

st.divider()

# ============================================================================
# SECTION 9: TOP MODULES & OPPORTUNITÉS
# ============================================================================
st.header("🏆 Top Modules & Opportunités")

tab_top1, tab_top2, tab_top3, tab_top4 = st.tabs([
    "💰 Top CA", 
    "📈 Top CA/mois", 
    "⬇️ Top Downloads/mois",
    "🎯 Opportunités"
])

def display_top_modules(data, highlight_col):
    """Affiche un tableau de top modules avec mise en forme."""
    display_data = data[['name', 'publisher', 'category', 'price', 'downloads', 
                         'rating', 'reviews_count', 'ca_estime', 'ca_par_mois', 
                         'downloads_par_mois']].copy()
    display_data.columns = ['Nom', 'Éditeur', 'Catégorie', 'Prix (€)', 'Downloads',
                           'Note', 'Avis', 'CA estimé (€)', 'CA/mois (€)', 'DL/mois']
    st.dataframe(display_data, use_container_width=True, hide_index=True)

with tab_top1:
    st.subheader("🥇 Modules générant le plus de revenus")
    paid_df = filtered_df[filtered_df['price'] > 0]
    top_ca = get_top_modules(paid_df, 'ca_estime', 25)
    display_top_modules(top_ca, 'ca_estime')

with tab_top2:
    st.subheader("📈 Modules les plus rentables dans le temps")
    paid_df = filtered_df[filtered_df['price'] > 0]
    top_ca_month = get_top_modules(paid_df, 'ca_par_mois', 25)
    display_top_modules(top_ca_month, 'ca_par_mois')

with tab_top3:
    st.subheader("⬇️ Modules les plus téléchargés par mois")
    top_downloads = get_top_modules(filtered_df, 'downloads_par_mois', 25)
    display_top_modules(top_downloads, 'downloads_par_mois')

with tab_top4:
    st.subheader("🎯 Opportunités: Gros CA + Mauvaises notes")
    st.markdown("""
    *Ces modules génèrent beaucoup de revenus malgré des notes médiocres. 
    C'est une opportunité de créer un meilleur produit dans cette niche!*
    """)
    opportunities = get_opportunities(filtered_df, 25)
    if len(opportunities) > 0:
        display_top_modules(opportunities, 'opportunite_score')
    else:
        st.info("Pas assez de modules payants avec avis pour cette analyse.")

st.divider()

# ============================================================================
# SECTION 10: EXPLORATION DES DONNÉES
# ============================================================================
st.header("🔬 Explorer les données")

tab_exp1, tab_exp2, tab_exp3 = st.tabs(["📊 Scatter Plot", "📋 Données brutes", "📉 Distribution"])

with tab_exp1:
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Axe X", ['price', 'downloads', 'rating', 'reviews_count', 
                                        'ca_estime', 'downloads_par_mois', 'ca_par_mois'], 
                              index=0)
    with col2:
        y_axis = st.selectbox("Axe Y", ['downloads', 'price', 'rating', 'reviews_count', 
                                        'ca_estime', 'downloads_par_mois', 'ca_par_mois'], 
                              index=0)
    
    # Scatter plot
    fig_scatter = px.scatter(
        filtered_df[filtered_df['price'] > 0] if 'ca' in x_axis or 'ca' in y_axis else filtered_df,
        x=x_axis,
        y=y_axis,
        color='category',
        size='reviews_count',
        hover_name='name',
        hover_data=['publisher', 'price', 'downloads', 'rating'],
        title=f"{y_axis} vs {x_axis}",
        height=600
    )
    fig_scatter.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab_exp2:
    st.subheader("📋 Toutes les données (filtrées)")
    
    # Sélection des colonnes à afficher
    all_cols = ['name', 'publisher', 'category', 'price', 'downloads', 'rating', 
                'reviews_count', 'ca_estime', 'ca_par_mois', 'downloads_par_mois',
                'publication_date', 'last_update', 'addon_version', 'prestashop_versions']
    
    display_df = filtered_df[all_cols].copy()
    display_df = display_df.sort_values('ca_estime', ascending=False)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Export CSV
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Télécharger en CSV",
        csv,
        "prestashop_modules_analytics.csv",
        "text/csv"
    )

with tab_exp3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des prix
        fig_price = px.histogram(
            filtered_df[filtered_df['price'] > 0],
            x='price',
            nbins=50,
            title="Distribution des prix (modules payants)",
            labels={'price': 'Prix (€)', 'count': 'Nombre de modules'}
        )
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        # Distribution des notes
        fig_rating = px.histogram(
            filtered_df,
            x='rating',
            nbins=10,
            title="Distribution des notes",
            labels={'rating': 'Note', 'count': 'Nombre de modules'}
        )
        st.plotly_chart(fig_rating, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>📊 Dashboard créé avec Streamlit | Données scrappées depuis PrestaShop Addons</p>
</div>
""", unsafe_allow_html=True)

