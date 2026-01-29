"""
Estimation des ventes pour les modules avec moins de 100 ventes.
Approche simple : tranches de 10 ventes + droite d'extrapolation.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import streamlit as st


def get_buckets_by_10(df, max_sales=1000, include_0_99=False):
    """
    Compte le nombre de modules par tranche de 10 ventes.
    Retourne un DataFrame avec : tranche_mid, nb_modules
    """
    if include_0_99:
        modules = df.copy()
        bins = list(range(0, max_sales + 10, 10))  # 0, 10, 20, ...
    else:
        modules = df[df['downloads'] >= 100].copy()
        bins = list(range(100, max_sales + 10, 10))  # 100, 110, 120, ...
    
    result = []
    for i in range(len(bins) - 1):
        low, high = bins[i], bins[i+1]
        count = len(modules[(modules['downloads'] >= low) & (modules['downloads'] < high)])
        if count > 0:
            result.append({
                'tranche_min': low,
                'tranche_max': high - 1,
                'tranche_mid': (low + high) / 2,
                'nb_modules': count
            })
    
    return pd.DataFrame(result)


def fit_line_and_extrapolate(df):
    """
    Analyse la distribution réelle par tranches de 10 ventes
    et estime les modules < 100 avec une distribution décroissante
    """
    modules_ge_100 = df[df['downloads'] >= 100].copy()
    modules_lt_100 = df[df['downloads'] < 100].copy()
    
    if len(modules_ge_100) == 0:
        return None
    
    # Compter par tranches de 10 (pour 100+)
    buckets_100plus = get_buckets_by_10(df, max_sales=2000)
    
    if len(buckets_100plus) < 3:
        return None
    
    # Régression linéaire sur les données 100+ (doit être décroissante)
    x = buckets_100plus['tranche_mid'].values
    y = buckets_100plus['nb_modules'].values
    
    # Forcer la pente à être négative (distribution décroissante)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Si la pente est positive, on la force à être légèrement négative
    if slope >= 0:
        slope = -0.5  # Pente négative raisonnable
    
    n_lt_100 = len(modules_lt_100)
    
    # Distribuer les n_lt_100 modules dans les tranches 0-99
    # suivant une distribution décroissante
    extrapolated = []
    remaining_modules = n_lt_100
    
    for i in range(0, 100, 10):
        mid = i + 5
        
        # Utiliser la droite pour estimer la proportion relative
        base_estimate = intercept + slope * mid
        base_estimate = max(0, base_estimate)
        
        extrapolated.append({
            'tranche_min': i,
            'tranche_max': i + 9,
            'tranche_mid': mid,
            'nb_modules_estime': base_estimate
        })
    
    extrapolated_df = pd.DataFrame(extrapolated)
    
    # Normaliser pour que le total = n_lt_100
    total_base = extrapolated_df['nb_modules_estime'].sum()
    if total_base > 0:
        extrapolated_df['nb_modules_estime'] = extrapolated_df['nb_modules_estime'] * (n_lt_100 / total_base)
    
    # Calculer la moyenne pondérée des ventes pour < 100
    total_modules_estime = extrapolated_df['nb_modules_estime'].sum()
    if total_modules_estime > 0:
        moyenne_ponderee = (extrapolated_df['tranche_mid'] * extrapolated_df['nb_modules_estime']).sum() / total_modules_estime
    else:
        moyenne_ponderee = 50
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value ** 2,
        'buckets_100plus': buckets_100plus,
        'extrapolated_0_99': extrapolated_df,
        'estimated_mean': moyenne_ponderee,
        'total_estimated_modules': total_modules_estime,
        'n_ge_100': len(modules_ge_100),
        'n_lt_100': n_lt_100
    }


def create_main_chart(params):
    """
    Graphique principal : barres par tranche de 10 + droite d'extrapolation décroissante
    """
    buckets = params['buckets_100plus']
    extrapolated = params['extrapolated_0_99']
    
    fig = go.Figure()
    
    # Barres pour tranches 0-99 (extrapolées) - en premier pour être en arrière-plan
    fig.add_trace(go.Bar(
        x=extrapolated['tranche_mid'],
        y=extrapolated['nb_modules_estime'],
        name='Estimation (0-99)',
        marker_color='orange',
        opacity=0.8,
        width=8
    ))
    
    # Barres pour tranches 100+ (données réelles)
    fig.add_trace(go.Bar(
        x=buckets['tranche_mid'],
        y=buckets['nb_modules'],
        name='Données réelles (100+)',
        marker_color='steelblue',
        width=8
    ))
    
    # Droite de régression (étendue sur toute la plage)
    x_line = np.linspace(5, buckets['tranche_mid'].max(), 100)
    y_line = params['intercept'] + params['slope'] * x_line
    y_line = np.maximum(y_line, 0)
    
    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        name=f'Droite décroissante (pente={params["slope"]:.2f})',
        line=dict(color='red', width=3)
    ))
    
    # Mettre en évidence la tranche 0-10
    fig.add_vrect(x0=0, x1=10, fillcolor="lightgreen", opacity=0.3,
                 annotation_text="Tranche 0-10 (max modules)")
    
    # Ligne verticale à 100
    fig.add_vline(x=100, line_dash="dash", line_color="green",
                  annotation_text="Seuil 100 ventes")
    
    fig.update_layout(
        title='📊 Distribution décroissante : plus de modules dans les faibles ventes',
        xaxis_title='Nombre de ventes (milieu de tranche)',
        yaxis_title='Nombre de modules',
        height=500,
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig


def create_extrapolation_table(params):
    """Tableau des tranches extrapolées 0-99"""
    df = params['extrapolated_0_99'].copy()
    df['Tranche'] = df.apply(lambda r: f"{int(r['tranche_min'])}-{int(r['tranche_max'])}", axis=1)
    df['Nb modules estimé'] = df['nb_modules_estime'].round(1)
    df['Ventes moyennes'] = df['tranche_mid']
    return df[['Tranche', 'Nb modules estimé', 'Ventes moyennes']]


def display_estimation_results(df):
    """Affiche les résultats d'estimation."""
    
    params = fit_line_and_extrapolate(df)
    
    if params is None:
        st.error("Pas assez de données pour l'estimation.")
        return None
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Modules 100+", params['n_ge_100'])
    with col2:
        st.metric("Modules < 100 (réel)", params['n_lt_100'])
    with col3:
        st.metric("Modules < 100 (estimé)", f"{params['total_estimated_modules']:.0f}")
    with col4:
        st.metric("R²", f"{params['r_squared']:.3f}")
    
    # Graphique principal
    st.subheader("📈 Distribution par tranches de 10 ventes")
    fig = create_main_chart(params)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **🔍 Logique de distribution :**
    - Si 50% des modules ont < 100 ventes, la distribution doit être **décroissante**
    - La tranche **0-10** doit contenir le **plus de modules** (beaucoup de modules avec très peu de ventes)
    - La tranche **90-99** doit contenir le **moins de modules**
    
    **📊 Méthode :**
    1. Observer la tendance décroissante des tranches 100+ (100-109, 110-119, etc.)
    2. Extrapoler cette droite décroissante vers 0-99
    3. Ajuster pour que le total corresponde exactement aux {params['n_lt_100']} modules réels
    
    **📈 Équation de la droite :** `y = {params['slope']:.2f}x + {params['intercept']:.1f}`
    - Pente négative = distribution décroissante ✓
    """)
    
    # Tableau des estimations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Estimation par tranche (0-99)")
        table = create_extrapolation_table(params)
        st.dataframe(table, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🎯 Résultat")
        st.metric(
            "Ventes moyennes estimées",
            f"{params['estimated_mean']:.1f} ventes",
            help="Moyenne pondérée des ventes pour les modules < 100"
        )
        
        # Impact CA
        prix_moyen = df[df['downloads'] < 100]['price'].mean()
        ca_estime = params['n_lt_100'] * params['estimated_mean'] * prix_moyen
        st.metric(
            "CA estimé (modules < 100)",
            f"{ca_estime:,.0f} €"
        )
        
        st.info(f"""
        **Formule :**  
        {params['n_lt_100']} modules × {params['estimated_mean']:.1f} ventes × {prix_moyen:.0f}€
        """)
    
    return params['estimated_mean']


def update_df_with_estimation(df, estimated_mean):
    """Met à jour le DataFrame avec les ventes estimées pour les modules < 100."""
    df_updated = df.copy()
    mask = df_updated['downloads'] < 100
    df_updated.loc[mask, 'downloads_estimes'] = estimated_mean
    df_updated.loc[~mask, 'downloads_estimes'] = df_updated.loc[~mask, 'downloads']
    
    # Recalculer le CA avec les estimations
    df_updated['ca_estime_avec_estimation'] = df_updated['price'] * df_updated['downloads_estimes']
    
    return df_updated
