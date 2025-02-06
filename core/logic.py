import uuid
from tqdm import tqdm
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, VerticalBarsDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from core.models import first_model_qrcode, second_model_qrcode, third_model_qrcode, fourth_model_qrcode
from core.utils import zip_qrcodes

# ---------------------------------------- Logique de génération des liens ----------------------------------------
def generate_urls(host, quantity):
    urls = []

    for _ in range(quantity):
        uuid4 = str(uuid.uuid4())
        url = f"{host}/check/{uuid4}"
        urls.append(url)

    return urls

# ---------------------------------------- Conversion des liens en image QrCodes ----------------------------------------
def convert_urls_to_qrcodes(urls, version, costum):
    qrcode_images = []

    for url in tqdm(urls, desc="Converting uuid links to images (1/3)", ncols=110, leave=True, unit=" it", colour="BLUE"):
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=50,
            border=0
        )
        qr.add_data(url)
        qr.make(fit=True)

        if costum:
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=VerticalBarsDrawer(),
                eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                color_mask=SolidFillColorMask(front_color=(255, 120, 48))) # augmente le temps de traitement
        else:
            img = qr.make_image(
                image_factory=StyledPilImage,
                eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                module_drawer=VerticalBarsDrawer())

        qrcode_images.append(img)

    return qrcode_images

# ---------------------------------------- Generation des Qrcodes en fonction d'un modèle choisi ----------------------------------------
def generate_qrcodes_model(base_dir, host, quantity, version, costum, zip_folder_name, format, poweredBy, model, logo=None, bordered=False, expand=False, radius=False, withID=False, beginID=None):

    urls = generate_urls(host, quantity)
    qrcode_images = convert_urls_to_qrcodes(urls, version, costum)
    output = []

    for _, qrcode_img in enumerate(tqdm(qrcode_images, desc="Generating Qrcodes models (2/3)      ",  ncols=110 , leave=True, unit=" it", colour="WHITE")):
        if model == 1:
            image_output = first_model_qrcode(bordered, radius, poweredBy, qrcode_img)
        elif model == 2:
            image_output = second_model_qrcode(bordered, radius, expand, poweredBy, qrcode_img, logo)
        elif model == 3:
            image_output = third_model_qrcode(bordered, radius, withID, beginID, poweredBy, qrcode_img, logo)
        elif model == 4:
            image_output = fourth_model_qrcode(bordered, radius, withID, beginID, poweredBy, qrcode_img, logo)
        else:
            print("Modèle non valide. Choisissez 1, 2 ou 3.")
            return None

        output.append(image_output)
        beginID = str(int(beginID) + 1).zfill(len(beginID))

    zip_path = zip_qrcodes(base_dir, zip_folder_name, format, output)
    return zip_path