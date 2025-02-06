from dotenv import load_dotenv
import os
from pathlib import Path
from core.logic import generate_qrcodes_model
from core.utils import get_base_dir, load_image, load_poweredBy, style
import keyboard
os.system('color')

def run_qrcode_generation():
    base_dir = get_base_dir()
    load_dotenv(base_dir / '.env')
    env = {
        "prod": os.getenv('PROD_HOST'),
        "pre-prod": os.getenv('PREPROD_HOST'),
        "re7": os.getenv('RE7_HOST'),
        "prod_V2": os.getenv('PROD_HOST_V2'),
        "pre-prod_V2": os.getenv('PREPROD_HOST_V2'),
        "re7_V2": os.getenv('RE7_HOST_V2'),
    }
    icon = load_image(base_dir, 'icon.png')

    # ---------------------------------------- Interaction avec l'utilisateur ----------------------------------------

    # Demander le nom du client, ne pas accepter une entrée vide
    while True:
        client_name = input(f"👷 Entrez le nom du client : {style.RESET}")
        if client_name:
            break
        print(f"{style.RED}Le nom du client ne peut pas être vide, veuillez réessayer.{style.RESET}")

    # Demander la quantité de QR codes à générer, ne pas accepter une entrée non valide
    while True:
        try:
            quantity = int(input(f"📦 Entrez la quantité de QR codes à générer : {style.RESET}"))
            if quantity > 0:
                break
            print(f"{style.RED}La quantité doit être supérieure à 0.{style.RESET}")
        except ValueError:
            print(f"{style.RED}Veuillez entrer un nombre valide.{style.RESET}")

    version = 1
    # Choisir la version des QR codes
    # while True:
    #     print(f"🔢 Choisissez la version des QR codes :")
    #     print(f"{style.MAGENTA}1. Version classic (21x21){style.RESET}")
    #     print(f"{style.CYAN}2. Version 20 (57x57) 🕒{style.RESET}")
    #     print(f"{style.GREEN}3. Version 40 (177x177) 🕒{style.RESET}")
    #     version_choice = input(f"Entrez le numéro correspondant à la version : {style.RESET}")

    #     if version_choice == '1':
    #         version = 1
    #         break
    #     elif version_choice == '2':
    #         version = 20
    #         break
    #     elif version_choice == '3':
    #         version = 40
    #         break
    #     else:
    #         print(f"{style.RED}Choix invalide, veuillez réessayer.{style.RESET}")

    while True:
        poweredByText = input(f"🔖 Entrez le texte de copyright © {style.YELLOW}(par exemple facildata){style.RESET} : ").upper()

        if len(poweredByText) == 9 and all(c.isalpha() or c.isspace() for c in poweredByText):
            break
        else:
            print(f"{style.RED}Veuillez entrer exactement 9 caractères alphabétiques (sans chiffres).{style.RESET}")

    # maitenant on va la générer nous même
    poweredBy = load_poweredBy(poweredByText, icon)

    # Demander si les QR codes doivent être personnalisés
    while True:
        costum_input = input(f"🎨 Souhaitez-vous une couleur personnalisée ? {style.YELLOW}(y/n){style.RESET} : ").lower()
        if costum_input == 'y':
            costum = True
            break
        elif costum_input == 'n':
            costum = False
            break
        else:
            print(f"{style.RED}Choix invalide, veuillez entrer 'y' pour Oui ou 'n' pour Non.{style.RESET}")

    # Choisir le format du fichier (png, JPEG, jpg, pdf)
    while True:
        print(f"📂 Choisissez le format de sortie :{style.RESET}")
        print(f"{style.MAGENTA}1. PNG{style.RESET}")
        print(f"{style.CYAN}2. JPEG{style.RESET}")
        print(f"{style.GREEN}3. PDF{style.RESET}")
        format_choice = input(f"Entrez le numéro correspondant au format souhaité : {style.RESET}")
        formats = {
            "1": "PNG",
            "2": "JPEG",
            "3": "PDF",
        }
        format = formats.get(format_choice)
        if format:
            break
        else:
            print(f"{style.RED}Choix invalide, veuillez réessayer.{style.RESET}")

    # Demander si border radius
    if format in ["PNG", "JPEG"]:
        while True:
            radius_input = input(f"✂️  Souhaitez-vous que les coins de l'étiquette soient arrondis (radius) ? {style.YELLOW}(y/n){style.RESET} : ").lower()
            if radius_input == 'y':
                radius = True
                break
            elif radius_input == 'n':
                radius = False
                break
            else:
                print(f"{style.RED}Choix invalide, veuillez entrer 'y' pour Oui ou 'n' pour Non.{style.RESET}")
    else:
        radius = False

    bordered = False
    # Demander si les QR codes doivent avoir une bordure
    # while True:
    #     bordered_input = input(f"🖼️  Souhaitez-vous ajouter une bordure autour des QR codes ? {style.YELLOW}(y/n){style.RESET} : ").lower()
    #     if bordered_input == 'y':
    #         bordered = True
    #         break
    #     elif bordered_input == 'n':
    #         bordered = False
    #         break
    #     else:
    #         print(f"{style.RED}Choix invalide, veuillez entrer 'y' pour Oui ou 'n' pour Non.{style.RESET}")

    # ---------------------------------------- Choix du modèle ----------------------------------------

    # Demander le modèle à utiliser (1, 2, 3), avec validation
    while True:
        print(f"🎴 Choisissez le modèle à utiliser : {style.RESET}")
        print(f"{style.MAGENTA}1. Modèle classic{style.RESET}")
        print(f"{style.CYAN}2. Modèle vertical (avec logo){style.RESET}")
        print(f"{style.GREEN}3. Modèle divisé en deux (avec logo){style.RESET}")
        print(f"{style.YELLOW}4. Modèle divisé en deux moitié (avec logo) {style.RESET}")
        model_choice = input(f"Entrez le numéro correspondant au modèle à utiliser : {style.RESET}")
        try:
            model = int(model_choice)
            if model in [1, 2, 3, 4]:
                break
            else:
                print(f"{style.RED}Choix invalide, veuillez entrer 1, 2, 3 ou 4.{style.RESET}")
        except ValueError:
            print(f"{style.RED}Veuillez entrer un nombre valide (1, 2, 3 ou 4).{style.RESET}")

    # ---------------------------------------- Questions spécifiques aux modèles ----------------------------------------

    # Si le modèle 2, 3 ou 4 est choisi, demander le chemin du logo
    logo = None
    if model in [2, 3, 4]:
        while True:
            logo_path = input(f"Veuillez entrer le chemin du logo (copiez-collez le chemin) : {style.RESET}")
            if os.path.isfile(logo_path):
                logo = load_image(base_dir, logo_path)
                break
            else:
                print(f"{style.RED}Le chemin fourni n'est pas valide, veuillez réessayer.{style.RESET}")

    # Si le modèle 2 est choisi, demander si le logo doit s'étendre
    if model == 2:
        while True:
            expand_input = input(f"Pour le modèle 2, souhaitez-vous que le logo s'étende pour remplir l'espace (expand) ? {style.YELLOW}(y/n){style.RESET} : ").lower()
            if expand_input == 'y':
                expand = True
                break
            elif expand_input == 'n':
                expand = False
                break
            else:
                print(f"{style.RED}Choix invalide, veuillez entrer 'y' pour Oui ou 'n' pour Non.{style.RESET}")
    else:
        expand = False  # par défaut, false pour les autres modèles

    # Si le modèle 3 est choisi, demander si un ID doit être inclus et son ID de départ
    if model == 3:
        while True:
            withID_input = input(f"Pour le modèle 3, souhaitez-vous inclure un ID ? {style.YELLOW}(y/n){style.RESET} : ").lower()
            if withID_input == 'y':
                withID = True
                break
            elif withID_input == 'n':
                withID = False
                beginID = "0"
                break
            else:
                print(f"{style.RED}Choix invalide, veuillez entrer 'y' pour Oui ou 'n' pour Non.{style.RESET}")

        if withID:
            while True:
                    beginID = input(f"Entrez l'ID de départ pour le modèle 3 {style.YELLOW}(par exemple 100, 000100, etc.){style.RESET} : ")
                    if beginID.isdigit():
                        break
                    else:
                        print(f"{style.RED}Veuillez entrer un nombre valide pour l'ID de départ.{style.RESET}")
    elif model == 4:
        while True:
            withID_input = input(f"Pour le modèle 4, souhaitez-vous inclure un ID ? {style.YELLOW}(y/n){style.RESET} : ").lower()
            if withID_input == 'y':
                withID = True
                break
            elif withID_input == 'n':
                withID = False
                beginID = "0"
                break
            else:
                print(f"{style.RED}Choix invalide, veuillez entrer 'y' pour Oui ou 'n' pour Non.{style.RESET}")

        if withID:
            while True:
                beginID = input(f"Entrez l'ID de départ pour le modèle 4 {style.YELLOW}(par exemple 100, 000100, etc.){style.RESET} : ")
                if beginID.isdigit():
                    break
                else:
                    print(f"{style.RED}Veuillez entrer un nombre valide pour l'ID de départ.{style.RESET}")
    else:
        withID = False  # par défaut, false pour les autres modèles
        beginID = "0"

    # Choisir l'environnement d'hébergement (prod, pre-prod, re7)
    while True:
        print(f"🌐 Choisissez l'environnement d'hébergement :{style.RESET}")
        print(f"{style.MAGENTA}1. prod{style.RESET}")
        print(f"{style.CYAN}2. pre-prod{style.RESET}")
        print(f"{style.GREEN}3. re7{style.RESET}")
        print(f"{style.BRIGHT_RED}4. prod (V2){style.RESET}")
        print(f"{style.ORANGE}5. pre-prod (V2){style.RESET}")
        print(f"{style.YELLOW}6. re7 (V2){style.RESET}")
        env_choice = input(f"Entrez le numéro correspondant à l'environnement : {style.RESET}")
        if env_choice == "1":
            host = env.get('prod')
            break
        elif env_choice == "2":
            host = env.get('pre-prod')
            break
        elif env_choice == "3":
            host = env.get('re7')
            break
        elif env_choice == "4":
            host = env.get('prod_V2')
            break
        elif env_choice == "5":
            host = env.get('pre-prod_V2')
            break
        elif env_choice == "6":
            host = env.get('re7_V2')
            break
        else:
            print(f"{style.RED}Choix invalide, veuillez réessayer.{style.RESET}")

    # ---------------------------------------- Phase de préparation ----------------------------------------

    zip_folder_name = F"{client_name}_qrcodes ({quantity})"
    output_dir = Path(os.getcwd())
    output_folder = output_dir / "output"
    output_folder.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------- Génération des QR codes en fonction du modèle choisi ----------------------------------------
    print("model", model, "withid", withID, "beginid", beginID)
    generate_qrcodes_model(
        base_dir=output_folder,
        host=host,
        quantity=quantity,
        version=version,
        costum=costum,
        zip_folder_name=zip_folder_name,
        format=format,
        poweredBy=poweredBy,
        model=model,
        logo=logo,
        bordered=bordered,
        expand=expand,
        radius=radius,
        withID=withID,
        beginID=beginID
    )

# ---------------------------------------- Redémarrer ou fermer le programme ----------------------------------------

while True:
    run_qrcode_generation()
    print(f"\n{style.YELLOW}🔄 Tapez 'R' pour réexécuter ou toute autre touche pour fermer le générateur...{style.RESET}")

    event = keyboard.read_event(suppress=True)
    if event.name.lower() != 'r':
        break