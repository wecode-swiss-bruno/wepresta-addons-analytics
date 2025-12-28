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
                     get_trimmed_comparison, get_category_advanced_stats, trimmed_mean)

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

# Filtre par catégorie
categories = ['Toutes'] + sorted(df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Catégorie", categories)

# Filtre par type (gratuit/payant)
price_filter = st.sidebar.radio("Type de module", ["Tous", "Payants uniquement", "Gratuits uniquement"])

# Filtre par note minimum
min_rating = st.sidebar.slider("Note minimum", 0.0, 5.0, 0.0, 0.5)

# Appliquer les filtres
filtered_df = df.copy()
if selected_category != 'Toutes':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if price_filter == "Payants uniquement":
    filtered_df = filtered_df[filtered_df['price'] > 0]
elif price_filter == "Gratuits uniquement":
    filtered_df = filtered_df[filtered_df['price'] == 0]
if min_rating > 0:
    filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

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
# SECTION 2: STATISTIQUES AVANCÉES (Médianes, Trimmed Mean)
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
# SECTION 3: ANALYSE PAR CATÉGORIE
# ============================================================================
st.header("📁 Analyse par catégorie")

tab1, tab2, tab3 = st.tabs(["📊 CA par catégorie", "📈 Tableau détaillé", "🗺️ Treemap"])

with tab1:
    # Bar chart CA par catégorie
    fig_ca = px.bar(
        category_stats.head(20),
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
        category_stats[display_cols].rename(columns={
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
        category_stats[category_stats['ca_total'] > 0],
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
# SECTION 4: TOP MODULES & OPPORTUNITÉS
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
# SECTION 5: EXPLORATION DES DONNÉES
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

