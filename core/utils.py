from pathlib import Path
import sys
import zipfile
import io
from tqdm import tqdm
from PIL import Image, ImageFont, ImageDraw

# ---------------------------------------- Récupérer le chemin racine en fonction de l'environnement (local ou exécutable) ----------------------------------------
def get_base_dir(font=False):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    if font:
        return base_path / "fonts" / "Poppins-SemiBold.ttf"
    else:
        return base_path

# ---------------------------------------- Récupération du font utilisé ----------------------------------------
font_path = get_base_dir(font=True)

# ---------------------------------------- Colors collection for terminal ----------------------------------------
class style():
    RED = '\033[31m'
    BRIGHT_RED = '\033[91m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'

# ---------------------------------------- Chercher une image source ----------------------------------------
def load_image(base_dir, image_name):
    image_path = base_dir / 'static' / image_name
    return Image.open(image_path)

# ---------------------------------------- Formatter le type des fichiers ----------------------------------------
def format_output(image, output_format='PNG', dpi=(300, 300)):
    output_format = output_format.upper()
    if output_format not in ['PNG', 'JPEG', 'PDF']:
        raise ValueError(f"Format {output_format} non supporté. Veuillez choisir entre PNG, JPEG, ou PDF.")

    img_byte_arr = io.BytesIO()

    if output_format == 'PDF':
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.save(img_byte_arr, format="PDF", resolution=dpi[0])

    elif output_format == 'JPEG':
        if image.mode == "RGBA":
            image = image.convert("RGB")
        image.save(img_byte_arr, format="JPEG", dpi=dpi)

    else: # PNG
        image.save(img_byte_arr, format=output_format, dpi=dpi)

    img_byte_arr.seek(0)

    return img_byte_arr

# ---------------------------------------- Enregistre un dossier final zip des images générées ----------------------------------------
def zip_qrcodes(base_dir, zip_folder_name, format, qrcode_images):
    zip_path = base_dir / f"{zip_folder_name}.zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for i, qrcode_img in enumerate(tqdm(qrcode_images, desc="Zipping images (3/3)                 ",  ncols=110 , leave=True, unit=" it", colour="RED")):
            img_byte_arr = format_output(qrcode_img, format)

            extension = format.lower()
            zipf.writestr(f'qrcode_{i + 1}.{extension}', img_byte_arr.read())

    print(f"{style.GREEN}✅ Traitement terminé ! Fichier ZIP créé: {zip_path}{style.RESET}")
    return zip_path

# ---------------------------------------- Générer le poweredBy automatiquement (Max 9 caractères) ----------------------------------------
def load_poweredBy(poweredByText, icon):
    frame_width = 292
    frame_height = 48

    plan = Image.new(mode="RGBA", size=(frame_width, frame_height), color=(0, 0, 0, 0))
    icon = icon.resize((icon.width, icon.height))

    icon_position = (0, (frame_height - icon.height) // 2)
    plan.paste(icon, icon_position, icon)

    font = ImageFont.truetype(str(font_path), 42)

    draw = ImageDraw.Draw(plan)

    text_width, text_height = draw.textbbox((0, 0), poweredByText, font=font)[2:]
    text_x = icon_position[0] + icon.width + 8
    text_y = (frame_height - text_height) // 2 - 6

    draw.text((text_x, text_y), poweredByText, font=font, fill=(0, 88, 163))

    return plan

# Test copyRight
# poweredByText = "facildata"
# icon = Image.open('static/icon.png')
# poweredBy = load_poweredBy(poweredByText, icon)
# poweredBy.save('poweredBy_image.png', format='PNG')