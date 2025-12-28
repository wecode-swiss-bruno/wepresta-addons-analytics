"""
Data loader pour les modules PrestaShop Addons.
Charge le JSON et parse les dates françaises.
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Mapping des mois français vers numéros
MOIS_FR = {
    'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
    'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
    'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
}


def parse_date_fr(date_str: str) -> datetime | None:
    """
    Parse une date française comme "13 août 2019" en datetime.
    Retourne None si le parsing échoue.
    """
    if not date_str or pd.isna(date_str):
        return None
    
    try:
        parts = date_str.strip().split()
        if len(parts) != 3:
            return None
        
        jour = int(parts[0])
        mois = MOIS_FR.get(parts[1].lower())
        annee = int(parts[2])
        
        if mois is None:
            return None
        
        return datetime(annee, mois, jour)
    except (ValueError, IndexError):
        return None


def load_modules(json_path: str | Path = "modules_prestashop.json") -> pd.DataFrame:
    """
    Charge les modules depuis le fichier JSON et retourne un DataFrame pandas.
    Parse les dates françaises en datetime.
    """
    json_path = Path(json_path)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Parser les dates françaises
    df['publication_datetime'] = df['publication_date'].apply(parse_date_fr)
    df['last_update_datetime'] = df['last_update'].apply(parse_date_fr)
    
    # Convertir en types appropriés
    df['module_id'] = df['module_id'].astype(str)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['downloads'] = pd.to_numeric(df['downloads'], errors='coerce').fillna(0).astype(int)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
    df['reviews_count'] = pd.to_numeric(df['reviews_count'], errors='coerce').fillna(0).astype(int)
    df['languages_count'] = pd.to_numeric(df['languages_count'], errors='coerce').fillna(0).astype(int)
    
    # Flag modules gratuits vs payants
    df['is_free'] = df['price'] == 0
    
    return df


if __name__ == "__main__":
    # Test du loader
    df = load_modules()
    print(f"Modules chargés: {len(df)}")
    print(f"Colonnes: {list(df.columns)}")
    print(f"\nExemple de module:")
    print(df.iloc[0][['name', 'price', 'downloads', 'publication_datetime', 'category']])

