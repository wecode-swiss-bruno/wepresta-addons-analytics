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
from metrics import calculate_metrics, get_category_stats, get_top_modules, get_opportunities, get_global_kpis

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
    st.metric("Modules filtrés", f"{len(filtered_df):,}")

st.divider()

# ============================================================================
# SECTION 2: ANALYSE PAR CATÉGORIE
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
# SECTION 3: TOP MODULES & OPPORTUNITÉS
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
# SECTION 4: EXPLORATION DES DONNÉES
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

