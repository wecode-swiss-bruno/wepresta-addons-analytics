"""
Calcul des métriques dérivées pour l'analyse des modules PrestaShop.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute les métriques calculées au DataFrame:
    - CA estimé (price × downloads)
    - Mois depuis publication
    - Downloads/mois
    - CA/mois
    - Score pondéré (rating × log(reviews_count + 1))
    """
    df = df.copy()
    now = datetime.now()
    
    # CA estimé = prix × téléchargements
    df['ca_estime'] = df['price'] * df['downloads']
    
    # Calcul des mois depuis publication
    def months_since(dt):
        if pd.isna(dt) or dt is None:
            return None
        delta = now - dt
        return max(1, delta.days / 30.44)  # Moyenne de jours par mois
    
    df['mois_depuis_publication'] = df['publication_datetime'].apply(months_since)
    
    # Downloads par mois
    df['downloads_par_mois'] = df.apply(
        lambda row: row['downloads'] / row['mois_depuis_publication'] 
        if row['mois_depuis_publication'] and row['mois_depuis_publication'] > 0 
        else 0,
        axis=1
    )
    
    # CA par mois (uniquement pour modules payants)
    df['ca_par_mois'] = df.apply(
        lambda row: row['ca_estime'] / row['mois_depuis_publication']
        if row['mois_depuis_publication'] and row['mois_depuis_publication'] > 0
        else 0,
        axis=1
    )
    
    # Score pondéré: rating × log(reviews + 1)
    # Un module noté 5/5 avec 100 avis vaut plus qu'un 5/5 avec 1 avis
    df['score_pondere'] = df['rating'] * np.log1p(df['reviews_count'])
    
    # Arrondir pour affichage
    df['downloads_par_mois'] = df['downloads_par_mois'].round(0).astype(int)
    df['ca_par_mois'] = df['ca_par_mois'].round(2)
    df['mois_depuis_publication'] = df['mois_depuis_publication'].round(1)
    
    return df


def get_category_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques agrégées par catégorie.
    """
    stats = df.groupby('category').agg({
        'module_id': 'count',
        'price': 'mean',
        'downloads': ['sum', 'mean'],
        'ca_estime': 'sum',
        'ca_par_mois': 'mean',
        'downloads_par_mois': 'mean',
        'rating': 'mean',
        'reviews_count': 'sum',
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    # Aplatir les colonnes multi-index
    stats.columns = [
        'nb_modules', 'prix_moyen', 'downloads_total', 'downloads_moyen',
        'ca_total', 'ca_moyen_par_mois', 'downloads_moyen_par_mois',
        'note_moyenne', 'nb_avis_total', 'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    stats = stats.sort_values('ca_total', ascending=False)
    
    return stats.reset_index()


def get_top_modules(df: pd.DataFrame, metric: str, n: int = 20, ascending: bool = False) -> pd.DataFrame:
    """
    Retourne le top N modules selon une métrique donnée.
    """
    cols = ['name', 'publisher', 'category', 'price', 'downloads', 
            'rating', 'reviews_count', 'ca_estime', 'ca_par_mois', 
            'downloads_par_mois', 'publication_date', 'url']
    
    return df.nsmallest(n, metric) if ascending else df.nlargest(n, metric)


def get_opportunities(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """
    Trouve les opportunités: modules avec mauvaises notes mais gros CA.
    Ces catégories/niches ont de la demande mais des produits insatisfaisants.
    """
    # Filtrer modules payants avec au moins quelques avis
    paid_with_reviews = df[(df['price'] > 0) & (df['reviews_count'] >= 5)]
    
    # Score d'opportunité: CA élevé + mauvaise note = opportunité
    # Plus le score est haut, plus c'est une opportunité
    paid_with_reviews = paid_with_reviews.copy()
    paid_with_reviews['opportunite_score'] = (
        paid_with_reviews['ca_estime'] / paid_with_reviews['ca_estime'].max() * 
        (5 - paid_with_reviews['rating']) / 5
    )
    
    return paid_with_reviews.nlargest(n, 'opportunite_score')


def get_global_kpis(df: pd.DataFrame) -> dict:
    """
    Calcule les KPIs globaux du marketplace.
    """
    paid_df = df[df['price'] > 0]
    
    return {
        'total_modules': len(df),
        'modules_gratuits': len(df[df['is_free']]),
        'modules_payants': len(paid_df),
        'ca_total': df['ca_estime'].sum(),
        'ca_mois_total': paid_df['ca_par_mois'].sum() if len(paid_df) > 0 else 0,
        'prix_moyen_payants': paid_df['price'].mean() if len(paid_df) > 0 else 0,
        'prix_median_payants': paid_df['price'].median() if len(paid_df) > 0 else 0,
        'downloads_total': df['downloads'].sum(),
        'downloads_moyen': df['downloads'].mean(),
        'note_moyenne': df['rating'].mean(),
        'nb_categories': df['category'].nunique(),
        'nb_publishers': df['publisher'].nunique(),
    }


def trimmed_mean(series: pd.Series, trim_pct: float) -> float:
    """
    Calcule la moyenne tronquée en excluant les X% extrêmes de chaque côté.
    trim_pct: pourcentage à exclure de chaque côté (ex: 10 = exclure 10% bas et 10% haut)
    """
    if len(series) == 0:
        return 0
    n = len(series)
    k = int(n * trim_pct / 100)
    if k == 0:
        return series.mean()
    sorted_vals = series.sort_values().values
    trimmed = sorted_vals[k:-k] if k > 0 else sorted_vals
    return np.mean(trimmed) if len(trimmed) > 0 else series.mean()


def get_advanced_stats(df: pd.DataFrame, trim_pct: float = 10) -> dict:
    """
    Calcule les statistiques avancées: moyenne, médiane, trimmed mean, percentiles.
    """
    paid_df = df[df['price'] > 0].copy()
    
    if len(paid_df) == 0:
        return {}
    
    stats = {}
    metrics = {
        'ca_estime': 'CA Estimé',
        'ca_par_mois': 'CA/mois',
        'price': 'Prix',
        'downloads': 'Downloads',
        'downloads_par_mois': 'Downloads/mois',
        'rating': 'Note',
        'reviews_count': 'Avis'
    }
    
    for col, label in metrics.items():
        data = paid_df[col].dropna()
        if len(data) == 0:
            continue
        stats[col] = {
            'label': label,
            'moyenne': data.mean(),
            'mediane': data.median(),
            'trimmed': trimmed_mean(data, trim_pct),
            'ecart_pct': ((data.mean() - data.median()) / data.median() * 100) if data.median() != 0 else 0,
            'p10': data.quantile(0.10),
            'p25': data.quantile(0.25),
            'p50': data.quantile(0.50),
            'p75': data.quantile(0.75),
            'p90': data.quantile(0.90),
            'p95': data.quantile(0.95),
            'p99': data.quantile(0.99),
            'min': data.min(),
            'max': data.max(),
            'std': data.std(),
        }
    
    return stats


def get_trimmed_comparison(df: pd.DataFrame, metric: str = 'ca_estime') -> pd.DataFrame:
    """
    Compare les moyennes avec différents niveaux de trimming.
    """
    paid_df = df[df['price'] > 0]
    if len(paid_df) == 0:
        return pd.DataFrame()
    
    data = paid_df[metric].dropna()
    results = []
    
    for trim in [0, 5, 10, 15, 20, 25]:
        results.append({
            'Trim %': f"{trim}%",
            'Moyenne': trimmed_mean(data, trim),
            'N modules': len(data) - 2 * int(len(data) * trim / 100) if trim > 0 else len(data)
        })
    
    return pd.DataFrame(results)


def get_category_advanced_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les stats avancées par catégorie avec médianes.
    """
    paid_df = df[df['price'] > 0]
    
    stats = paid_df.groupby('category').agg({
        'module_id': 'count',
        'ca_estime': ['sum', 'mean', 'median'],
        'ca_par_mois': ['sum', 'mean', 'median'],
        'price': ['mean', 'median'],
        'rating': 'mean'
    }).round(2)
    
    stats.columns = ['nb_modules', 'ca_total', 'ca_moyen', 'ca_median', 
                     'ca_mois_total', 'ca_mois_moyen', 'ca_mois_median', 
                     'prix_moyen', 'prix_median', 'note_moy']
    
    # Filtrer catégories avec au moins 3 modules
    stats = stats[stats['nb_modules'] >= 3]
    stats = stats.sort_values('ca_mois_median', ascending=False)
    
    return stats.reset_index()


if __name__ == "__main__":
    from data_loader import load_modules
    
    df = load_modules()
    df = calculate_metrics(df)
    
    print("=== KPIs Globaux ===")
    kpis = get_global_kpis(df)
    for k, v in kpis.items():
        print(f"{k}: {v:,.2f}" if isinstance(v, float) else f"{k}: {v:,}")
    
    print("\n=== Top 5 CA ===")
    top_ca = get_top_modules(df, 'ca_estime', 5)
    print(top_ca[['name', 'price', 'downloads', 'ca_estime']].to_string())

