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


# =============================================================================
# PUBLISHER STATISTICS
# =============================================================================

def get_publisher_stats(df: pd.DataFrame, min_modules: int = 2) -> pd.DataFrame:
    """
    Calcule les statistiques par éditeur (publisher).
    """
    stats = df.groupby('publisher').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'downloads': ['sum', 'mean'],
        'ca_estime': ['sum', 'mean', 'median'],
        'ca_par_mois': ['sum', 'mean', 'median'],
        'downloads_par_mois': ['mean', 'median'],
        'rating': 'mean',
        'reviews_count': ['sum', 'mean'],
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'downloads_total', 'downloads_moyen',
        'ca_total', 'ca_moyen', 'ca_median',
        'ca_mois_total', 'ca_mois_moyen', 'ca_mois_median',
        'dl_mois_moyen', 'dl_mois_median',
        'note_moyenne', 'avis_total', 'avis_moyen',
        'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    stats['pct_payants'] = (stats['nb_payants'] / stats['nb_modules'] * 100).round(1)
    
    # Filtrer par minimum de modules
    stats = stats[stats['nb_modules'] >= min_modules]
    stats = stats.sort_values('ca_total', ascending=False)
    
    return stats.reset_index()


def get_publisher_stats_paid_only(df: pd.DataFrame, min_modules: int = 2) -> pd.DataFrame:
    """
    Calcule les statistiques par éditeur pour les modules payants uniquement.
    """
    paid_df = df[df['price'] > 0]
    
    stats = paid_df.groupby('publisher').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean', 'median'],
        'ca_par_mois': ['sum', 'mean', 'median'],
        'downloads_par_mois': ['mean', 'median'],
        'rating': 'mean',
        'reviews_count': 'sum',
        'category': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen', 'ca_median',
        'ca_mois_total', 'ca_mois_moyen', 'ca_mois_median',
        'dl_mois_moyen', 'dl_mois_median',
        'note_moyenne', 'avis_total',
        'categorie_principale'
    ]
    
    # Filtrer par minimum de modules
    stats = stats[stats['nb_modules'] >= min_modules]
    stats = stats.sort_values('ca_mois_moyen', ascending=False)
    
    return stats.reset_index()


def get_top_publishers(df: pd.DataFrame, metric: str = 'ca_total', n: int = 20) -> pd.DataFrame:
    """
    Retourne le top N éditeurs selon une métrique.
    """
    stats = get_publisher_stats(df, min_modules=1)
    return stats.nlargest(n, metric)


# =============================================================================
# AGE-BASED STATISTICS
# =============================================================================

AGE_BUCKETS = [
    (0, 1, "< 1 mois"),
    (1, 3, "1-3 mois"),
    (3, 6, "3-6 mois"),
    (6, 12, "6-12 mois"),
    (12, 24, "1-2 ans"),
    (24, 60, "2-5 ans"),
    (60, float('inf'), "> 5 ans"),
]


def get_age_bucket(months: float) -> str:
    """Retourne le bucket d'âge pour un nombre de mois donné."""
    if pd.isna(months) or months is None:
        return "Inconnu"
    for min_m, max_m, label in AGE_BUCKETS:
        if min_m <= months < max_m:
            return label
    return "> 5 ans"


def get_age_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par tranche d'âge des modules.
    """
    df_copy = df.copy()
    df_copy['age_bucket'] = df_copy['mois_depuis_publication'].apply(get_age_bucket)
    
    # Ordre des buckets pour le tri
    bucket_order = [b[2] for b in AGE_BUCKETS] + ["Inconnu"]
    
    # Stats globales par bucket
    stats = df_copy.groupby('age_bucket').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean', 'median'],
        'ca_par_mois': ['mean', 'median'],
        'downloads': ['sum', 'mean'],
        'downloads_par_mois': ['mean', 'median'],
        'rating': 'mean',
        'reviews_count': ['sum', 'mean'],
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen', 'ca_median',
        'ca_mois_moyen', 'ca_mois_median',
        'downloads_total', 'downloads_moyen',
        'dl_mois_moyen', 'dl_mois_median',
        'note_moyenne', 'avis_total', 'avis_moyen',
        'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    stats['pct_payants'] = (stats['nb_payants'] / stats['nb_modules'] * 100).round(1)
    
    stats = stats.reset_index()
    
    # Trier par ordre logique des buckets
    stats['sort_order'] = stats['age_bucket'].apply(
        lambda x: bucket_order.index(x) if x in bucket_order else 999
    )
    stats = stats.sort_values('sort_order').drop('sort_order', axis=1)
    
    return stats


def get_age_stats_paid_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par tranche d'âge pour les modules payants uniquement.
    """
    paid_df = df[df['price'] > 0].copy()
    paid_df['age_bucket'] = paid_df['mois_depuis_publication'].apply(get_age_bucket)
    
    bucket_order = [b[2] for b in AGE_BUCKETS] + ["Inconnu"]
    
    stats = paid_df.groupby('age_bucket').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean', 'median'],
        'ca_par_mois': ['mean', 'median'],
        'downloads_par_mois': ['mean', 'median'],
        'rating': 'mean',
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen', 'ca_median',
        'ca_mois_moyen', 'ca_mois_median',
        'dl_mois_moyen', 'dl_mois_median',
        'note_moyenne'
    ]
    
    stats = stats.reset_index()
    stats['sort_order'] = stats['age_bucket'].apply(
        lambda x: bucket_order.index(x) if x in bucket_order else 999
    )
    stats = stats.sort_values('sort_order').drop('sort_order', axis=1)
    
    return stats


# =============================================================================
# KEYWORD ANALYSIS
# =============================================================================

# Stopwords français courants + mots non pertinents pour l'analyse
FRENCH_STOPWORDS = {
    # Articles
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'l',
    # Prépositions
    'à', 'au', 'aux', 'avec', 'pour', 'par', 'sur', 'sous', 'dans', 'en', 'sans',
    # Conjonctions
    'et', 'ou', 'mais', 'donc', 'car', 'ni', 'que', 'qui', 'quoi',
    # Pronoms
    'ce', 'cette', 'ces', 'cet', 'il', 'elle', 'ils', 'elles', 'on', 'nous', 'vous',
    'je', 'tu', 'son', 'sa', 'ses', 'leur', 'leurs', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes',
    # Verbes communs
    'est', 'sont', 'être', 'avoir', 'fait', 'faire', 'peut', 'peuvent', 'permet',
    'permettent', 'permettant', 'offre', 'offrir', 'utiliser', 'utilise',
    # Adverbes
    'plus', 'moins', 'très', 'bien', 'aussi', 'tout', 'tous', 'toutes', 'toute',
    'même', 'autres', 'autre', 'comme', 'ainsi', 'pas', 'ne', 'n',
    # Mots génériques e-commerce/PrestaShop
    'module', 'modules', 'prestashop', 'boutique', 'boutiques', 'shop', 'store',
    'site', 'sites', 'page', 'pages', 'web', 'ligne', 'online',
    'client', 'clients', 'visiteur', 'visiteurs', 'utilisateur', 'utilisateurs',
    'produit', 'produits', 'commande', 'commandes', 'achat', 'achats',
    'vente', 'ventes', 'panier', 'paniers',
    # Mots vides
    'etc', 'via', 'nbsp', 'br', 'http', 'https', 'www', 'com', 'fr',
    # Nombres et symboles (généralement filtrés autrement)
    'nouveau', 'nouvelle', 'nouveaux', 'nouvelles', 'version',
}


def extract_keywords(text: str, min_length: int = 3) -> list[str]:
    """
    Extrait les mots-clés significatifs d'un texte.
    """
    import re
    
    if not text or pd.isna(text):
        return []
    
    # Nettoyer et normaliser
    text = text.lower()
    # Remplacer les caractères spéciaux par des espaces
    text = re.sub(r'[^a-zàâäéèêëïîôùûüç\s-]', ' ', text)
    # Séparer les mots
    words = text.split()
    
    # Filtrer
    keywords = []
    for word in words:
        word = word.strip('-')
        if (len(word) >= min_length and 
            word not in FRENCH_STOPWORDS and
            not word.isdigit()):
            keywords.append(word)
    
    return keywords


def get_keyword_stats(df: pd.DataFrame, min_occurrences: int = 5, top_n: int = 100) -> pd.DataFrame:
    """
    Analyse les mots-clés des descriptions et calcule les statistiques CA associées.
    
    Args:
        df: DataFrame avec les modules
        min_occurrences: Nombre minimum d'occurrences pour inclure un mot-clé
        top_n: Nombre de mots-clés à retourner
    
    Returns:
        DataFrame avec stats par mot-clé
    """
    # Extraire les keywords de chaque module
    keyword_data = []
    
    for _, row in df.iterrows():
        keywords = extract_keywords(row.get('short_description', ''))
        keywords_set = set(keywords)  # Unique par module
        
        for kw in keywords_set:
            keyword_data.append({
                'keyword': kw,
                'module_id': row['module_id'],
                'price': row['price'],
                'ca_estime': row['ca_estime'],
                'ca_par_mois': row['ca_par_mois'],
                'downloads': row['downloads'],
                'downloads_par_mois': row['downloads_par_mois'],
                'rating': row['rating'],
                'category': row['category'],
                'is_paid': row['price'] > 0
            })
    
    if not keyword_data:
        return pd.DataFrame()
    
    kw_df = pd.DataFrame(keyword_data)
    
    # Agréger par keyword
    stats = kw_df.groupby('keyword').agg({
        'module_id': 'count',
        'price': 'mean',
        'ca_estime': ['sum', 'mean', 'median'],
        'ca_par_mois': ['mean', 'median'],
        'downloads': ['sum', 'mean'],
        'downloads_par_mois': 'mean',
        'rating': 'mean',
        'is_paid': 'sum',
        'category': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen',
        'ca_total', 'ca_moyen', 'ca_median',
        'ca_mois_moyen', 'ca_mois_median',
        'downloads_total', 'downloads_moyen',
        'dl_mois_moyen', 'note_moyenne',
        'nb_payants', 'categorie_principale'
    ]
    
    # Filtrer par occurrences minimum
    stats = stats[stats['nb_modules'] >= min_occurrences]
    
    # Score d'opportunité: CA moyen élevé mais peu de modules = niche rentable
    if len(stats) > 0:
        stats['opportunite_score'] = (
            (stats['ca_mois_moyen'] / stats['ca_mois_moyen'].max()) * 
            (1 - stats['nb_modules'] / stats['nb_modules'].max())
        ).round(3)
    
    # Trier par CA moyen par mois (les keywords les plus rentables)
    stats = stats.sort_values('ca_mois_moyen', ascending=False)
    
    return stats.head(top_n).reset_index()


def get_keyword_opportunities(df: pd.DataFrame, min_occurrences: int = 3, top_n: int = 50) -> pd.DataFrame:
    """
    Trouve les mots-clés avec un bon potentiel: CA élevé mais peu de concurrence.
    """
    stats = get_keyword_stats(df, min_occurrences=min_occurrences, top_n=500)
    
    if len(stats) == 0:
        return pd.DataFrame()
    
    # Filtrer les keywords avec un bon score d'opportunité
    # et un CA/mois minimum significatif
    ca_threshold = stats['ca_mois_moyen'].quantile(0.25)  # Top 75%
    opportunities = stats[
        (stats['ca_mois_moyen'] >= ca_threshold) & 
        (stats['nb_modules'] <= stats['nb_modules'].quantile(0.5))  # Moins concurrentiel
    ]
    
    return opportunities.sort_values('opportunite_score', ascending=False).head(top_n)


def get_modules_by_keyword(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Retourne tous les modules contenant un mot-clé spécifique.
    """
    keyword = keyword.lower()
    
    mask = df['short_description'].apply(
        lambda x: keyword in extract_keywords(str(x)) if pd.notna(x) else False
    )
    
    result = df[mask].copy()
    return result.sort_values('ca_par_mois', ascending=False)


# =============================================================================
# LANGUAGE STATISTICS
# =============================================================================

def get_language_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par langue disponible.
    Explose la liste des langues pour avoir une ligne par langue.
    """
    # Exploser la colonne available_languages
    df_exploded = df.explode('available_languages')
    df_exploded = df_exploded[df_exploded['available_languages'].notna()]
    df_exploded['language'] = df_exploded['available_languages'].str.strip().str.lower()
    
    stats = df_exploded.groupby('language').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean'],
        'ca_par_mois': ['mean', 'median'],
        'downloads': 'sum',
        'rating': 'mean',
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen',
        'ca_mois_moyen', 'ca_mois_median',
        'downloads_total', 'note_moyenne', 'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    stats = stats.sort_values('nb_modules', ascending=False)
    
    return stats.reset_index()


def get_languages_count_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par nombre de langues supportées.
    """
    df_copy = df.copy()
    df_copy['lang_count_bucket'] = df_copy['languages_count'].apply(
        lambda x: '0' if pd.isna(x) or x == 0 else 
                  '1' if x == 1 else 
                  '2-3' if x <= 3 else 
                  '4-5' if x <= 5 else 
                  '6-10' if x <= 10 else '10+'
    )
    
    stats = df_copy.groupby('lang_count_bucket').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean'],
        'ca_par_mois': ['mean', 'median'],
        'downloads_par_mois': 'mean',
        'rating': 'mean',
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen',
        'ca_mois_moyen', 'ca_mois_median',
        'dl_mois_moyen', 'note_moyenne', 'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    
    # Trier dans l'ordre logique
    order = ['0', '1', '2-3', '4-5', '6-10', '10+']
    stats = stats.reset_index()
    stats['sort_order'] = stats['lang_count_bucket'].apply(lambda x: order.index(x) if x in order else 99)
    stats = stats.sort_values('sort_order').drop('sort_order', axis=1)
    
    return stats


# =============================================================================
# PRESTASHOP VERSION STATISTICS
# =============================================================================

def parse_prestashop_versions(version_str: str) -> tuple:
    """
    Parse une chaîne de versions PrestaShop comme '1.6.0 à 9.0' 
    et retourne (version_min, version_max).
    """
    if pd.isna(version_str) or not version_str:
        return (None, None)
    
    version_str = str(version_str).strip()
    
    if ' à ' in version_str:
        parts = version_str.split(' à ')
        return (parts[0].strip(), parts[1].strip())
    elif ' - ' in version_str:
        parts = version_str.split(' - ')
        return (parts[0].strip(), parts[1].strip())
    else:
        return (version_str, version_str)


def get_version_compatibility_bucket(version_str: str) -> str:
    """
    Catégorise un module selon sa compatibilité PrestaShop.
    """
    if pd.isna(version_str) or not version_str:
        return "Inconnu"
    
    _, max_version = parse_prestashop_versions(version_str)
    
    if max_version is None:
        return "Inconnu"
    
    try:
        # Extraire le numéro majeur
        major = max_version.split('.')[0]
        if major == '9':
            return "PS 9.x (Latest)"
        elif major == '8':
            return "PS 8.x"
        elif major == '1':
            minor = max_version.split('.')[1] if '.' in max_version else '0'
            if minor == '7':
                return "PS 1.7.x"
            elif minor == '6':
                return "PS 1.6.x (Legacy)"
            else:
                return "PS 1.5 ou moins"
        else:
            return "Autre"
    except:
        return "Inconnu"


def get_prestashop_version_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par compatibilité de version PrestaShop.
    """
    df_copy = df.copy()
    df_copy['version_bucket'] = df_copy['prestashop_versions'].apply(get_version_compatibility_bucket)
    
    stats = df_copy.groupby('version_bucket').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean'],
        'ca_par_mois': ['mean', 'median'],
        'downloads': 'sum',
        'rating': 'mean',
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen',
        'ca_mois_moyen', 'ca_mois_median',
        'downloads_total', 'note_moyenne', 'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    
    # Trier dans l'ordre logique
    order = ['PS 9.x (Latest)', 'PS 8.x', 'PS 1.7.x', 'PS 1.6.x (Legacy)', 'PS 1.5 ou moins', 'Autre', 'Inconnu']
    stats = stats.reset_index()
    stats['sort_order'] = stats['version_bucket'].apply(lambda x: order.index(x) if x in order else 99)
    stats = stats.sort_values('sort_order').drop('sort_order', axis=1)
    
    return stats


# =============================================================================
# LAST UPDATE STATISTICS
# =============================================================================

def get_update_recency_bucket(months_since_update: float) -> str:
    """
    Catégorise un module selon la fraîcheur de sa dernière mise à jour.
    """
    if pd.isna(months_since_update):
        return "Inconnu"
    
    if months_since_update < 1:
        return "< 1 mois"
    elif months_since_update < 3:
        return "1-3 mois"
    elif months_since_update < 6:
        return "3-6 mois"
    elif months_since_update < 12:
        return "6-12 mois"
    elif months_since_update < 24:
        return "1-2 ans"
    elif months_since_update < 36:
        return "2-3 ans"
    else:
        return "> 3 ans (obsolète?)"


def get_last_update_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par fraîcheur de mise à jour.
    """
    df_copy = df.copy()
    
    # Calculer les mois depuis la dernière mise à jour
    from datetime import datetime
    now = datetime.now()
    
    def months_since_update(dt):
        if pd.isna(dt) or dt is None:
            return None
        delta = now - dt
        return delta.days / 30.44
    
    df_copy['months_since_update'] = df_copy['last_update_datetime'].apply(months_since_update)
    df_copy['update_bucket'] = df_copy['months_since_update'].apply(get_update_recency_bucket)
    
    stats = df_copy.groupby('update_bucket').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean'],
        'ca_par_mois': ['mean', 'median'],
        'downloads_par_mois': 'mean',
        'rating': 'mean',
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen',
        'ca_mois_moyen', 'ca_mois_median',
        'dl_mois_moyen', 'note_moyenne', 'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    
    # Trier dans l'ordre logique
    order = ['< 1 mois', '1-3 mois', '3-6 mois', '6-12 mois', '1-2 ans', '2-3 ans', '> 3 ans (obsolète?)', 'Inconnu']
    stats = stats.reset_index()
    stats['sort_order'] = stats['update_bucket'].apply(lambda x: order.index(x) if x in order else 99)
    stats = stats.sort_values('sort_order').drop('sort_order', axis=1)
    
    return stats


# =============================================================================
# ADDON VERSION STATISTICS
# =============================================================================

def get_addon_version_major(version_str: str) -> str:
    """
    Extrait la version majeure d'un addon (ex: '2.1.5' -> '2.x').
    """
    if pd.isna(version_str) or not version_str:
        return "Inconnu"
    
    try:
        version_str = str(version_str).strip()
        major = version_str.split('.')[0]
        if major.isdigit():
            return f"{major}.x"
        return "Autre"
    except:
        return "Inconnu"


def get_addon_version_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques par version majeure de l'addon.
    """
    df_copy = df.copy()
    df_copy['version_major'] = df_copy['addon_version'].apply(get_addon_version_major)
    
    stats = df_copy.groupby('version_major').agg({
        'module_id': 'count',
        'price': ['mean', 'median'],
        'ca_estime': ['sum', 'mean'],
        'ca_par_mois': ['mean', 'median'],
        'rating': 'mean',
        'is_free': lambda x: (x == True).sum()
    }).round(2)
    
    stats.columns = [
        'nb_modules', 'prix_moyen', 'prix_median',
        'ca_total', 'ca_moyen',
        'ca_mois_moyen', 'ca_mois_median',
        'note_moyenne', 'nb_gratuits'
    ]
    
    stats['nb_payants'] = stats['nb_modules'] - stats['nb_gratuits']
    stats = stats.sort_values('nb_modules', ascending=False)
    
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

