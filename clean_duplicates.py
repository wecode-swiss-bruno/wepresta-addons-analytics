"""
Script pour supprimer les doublons dans modules_prestashop.json
Garde le module le plus récent (basé sur scraped_at) en cas de doublon.
"""

import json
from pathlib import Path
from datetime import datetime


def clean_duplicates(input_file: str = "modules_prestashop.json", 
                     output_file: str = None,
                     dry_run: bool = False):
    """
    Supprime les doublons du fichier JSON.
    
    Args:
        input_file: Chemin du fichier JSON source
        output_file: Chemin du fichier de sortie (si None, écrase l'original)
        dry_run: Si True, affiche seulement les stats sans modifier le fichier
    """
    input_path = Path(input_file)
    output_path = Path(output_file) if output_file else input_path
    
    print(f"📂 Chargement de {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        modules = json.load(f)
    
    print(f"📊 Modules chargés: {len(modules)}")
    
    # Dictionnaire pour garder le meilleur module par ID
    unique_modules = {}
    duplicates_found = []
    
    for module in modules:
        # Utiliser module_id comme clé primaire, sinon url
        module_id = module.get('module_id') or module.get('url')
        
        if not module_id:
            # Pas d'identifiant, on garde le module quand même
            unique_modules[f"unknown_{len(unique_modules)}"] = module
            continue
        
        if module_id in unique_modules:
            # Doublon trouvé - garder le plus récent
            existing = unique_modules[module_id]
            existing_date = existing.get('scraped_at', '')
            new_date = module.get('scraped_at', '')
            
            # Comparer les dates
            if new_date > existing_date:
                duplicates_found.append({
                    'id': module_id,
                    'name': existing.get('name', 'N/A'),
                    'kept': 'nouveau',
                    'old_date': existing_date,
                    'new_date': new_date
                })
                unique_modules[module_id] = module
            else:
                duplicates_found.append({
                    'id': module_id,
                    'name': module.get('name', 'N/A'),
                    'kept': 'ancien',
                    'old_date': existing_date,
                    'new_date': new_date
                })
        else:
            unique_modules[module_id] = module
    
    # Convertir en liste
    cleaned_modules = list(unique_modules.values())
    
    # Stats
    print(f"\n{'='*60}")
    print(f"📈 RÉSULTATS")
    print(f"{'='*60}")
    print(f"   Modules originaux:  {len(modules):,}")
    print(f"   Doublons trouvés:   {len(duplicates_found):,}")
    print(f"   Modules uniques:    {len(cleaned_modules):,}")
    print(f"   Réduction:          {len(modules) - len(cleaned_modules):,} modules")
    
    if duplicates_found:
        print(f"\n📋 Exemples de doublons (max 10):")
        for dup in duplicates_found[:10]:
            print(f"   - ID {dup['id']}: {dup['name'][:40]}...")
    
    if dry_run:
        print(f"\n⚠️  Mode DRY RUN - Aucune modification effectuée")
        return
    
    # Sauvegarder
    print(f"\n💾 Sauvegarde vers {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_modules, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Terminé! Fichier sauvegardé.")
    
    return {
        'original_count': len(modules),
        'duplicates_count': len(duplicates_found),
        'unique_count': len(cleaned_modules),
        'duplicates': duplicates_found
    }


def analyze_duplicates(input_file: str = "modules_prestashop.json"):
    """
    Analyse les doublons sans modifier le fichier.
    """
    print("🔍 Analyse des doublons (mode lecture seule)...\n")
    return clean_duplicates(input_file, dry_run=True)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        # Mode analyse seulement
        analyze_duplicates()
    elif len(sys.argv) > 1 and sys.argv[1] == "--backup":
        # Créer une copie de sauvegarde puis nettoyer
        import shutil
        backup_path = "modules_prestashop_backup.json"
        shutil.copy("modules_prestashop.json", backup_path)
        print(f"📦 Backup créé: {backup_path}")
        clean_duplicates()
    else:
        # Nettoyage direct
        print("Usage:")
        print("  python clean_duplicates.py --dry-run    # Analyse sans modification")
        print("  python clean_duplicates.py --backup     # Backup + nettoyage")
        print("  python clean_duplicates.py --clean      # Nettoyage direct (ATTENTION!)")
        print()
        
        if len(sys.argv) > 1 and sys.argv[1] == "--clean":
            clean_duplicates()
        else:
            # Par défaut, mode analyse
            analyze_duplicates()


