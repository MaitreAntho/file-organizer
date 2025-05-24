import os
import shutil
from pathlib import Path
import logging
from datetime import datetime

def setup_logging():
    """Configurer le journalisation pour le script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_file_category(extension):
    """Déterminer la catégorie d'un fichier en fonction de son extension."""
    categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.csv'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
        'audio': ['.mp3', '.wav', '.flac', '.m4a'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'code': ['.py', '.js', '.html', '.css', '.java', '.cpp']
    }
    
    extension = extension.lower()
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    return 'others'

def organize_files(directory):
    """Organiser les fichiers dans le dossier spécifié par leurs catégories."""
    try:
        directory = Path(directory)
        if not directory.exists():
            logging.error(f"Le dossier {directory} n'existe pas!")
            return False

        total_files = len([f for f in directory.glob('*') if f.is_file()])
        if total_files == 0:
            logging.info("Aucun fichier à organiser!")
            return True

        files_moved = 0
        for file_path in directory.glob('*'):
            if file_path.is_file():
                category = get_file_category(file_path.suffix)
                category_dir = directory / category
                category_dir.mkdir(exist_ok=True)
                
                try:
                    shutil.move(str(file_path), str(category_dir / file_path.name))
                    files_moved += 1
                    logging.info(f"Déplacé: {file_path.name} → {category}")
                except Exception as e:
                    logging.error(f"Erreur lors du déplacement de {file_path.name}: {e}")

        logging.info(f"\nRésumé:\nFichiers traités: {total_files}\nFichiers déplacés: {files_moved}")
        return True

    except Exception as e:
        logging.error(f"Une erreur est survenue: {e}")
        return False

if __name__ == "__main__":
    setup_logging()
    print("=== Organisateur de Fichiers ===")
    
    while True:
        directory = input("\nEntrez le chemin du dossier à organiser (ou 'q' pour quitter): ")
        if directory.lower() == 'q':
            break
            
        if organize_files(directory):
            print("\nOrganisation terminée! Vérifiez les dossiers créés.")
        else:
            print("\nUne erreur s'est produite. Veuillez vérifier le chemin du dossier.")
