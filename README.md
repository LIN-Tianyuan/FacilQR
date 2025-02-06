# 👷 FacilQR
FacildataQR est un générateur de QR codes autonome, développé entièrement en Python.

## 📜 Notice d'utilisation
Pour utiliser le générateur, il suffit de lancer le fichier FacilQR V.exe et de suivre les instructions à l'écran.

**Notes :**
- Pour les modèles avec les logos, il suffit de (copier/coller) le chemin absolu de la ou se trouve le logo exemple : **C:\Users\senou\Downloads\logo.png**
- Pour copier le chemin absolu d'un fichier sur Windows, il suffit de **Click droit** sur le fichier, dans l'onglet **sécurité**, puis copier le **nom de l'objet** sans espaces.

⚠️ Il faut que logo soit en format : PNG (pour le moment)

## Modéles
```
First model => h: 468 w:400 (sans log)
1st qrcode h:360 w:360 /
2nd copyright: h:48 w:292 /


Second model => h: 600 w:400 (avec logo)
1st logo h:112 w:360 /
2nd: qrcode h:360 w:360 /
3td: copyright: h:48 w:292 /


- Third model => h:400 w:600 h: 400 w:600 (avec logo)
left : 1st qrcode h:292 w:292 /
2nd copyright: h:48 w:292 /
right logo : logo h:360 w:248 /

## withID
right logo : logo h:292 w:248 /
withID text cadre : h:48 w:248 /
(texte police 42 - ExtraBold poppins)

- Forth model => en cours...
```

# TODO:
- Refctoriser le code et les fonctions.
- Notice pour l'utilisation

### ⚒️ Dépendances nécessaires pour ce projet
- pip install qrcode[pil] Pillow
- pip install tqdm
- pip install keyboard

## Pour installer les dépendances
```
pip install -r requirements.txt
```

## Pour run en local
```
python main.py
```

## Pour build .exe
commande pour build le .exe :

```
pyinstaller --onefile --name "FacilQR v1.1.0" --add-data "fonts;fonts" --add-data ".env;." --add-data "core;core" --add-data "static;static" main.py
```

© 2024 [Facildata](support@facildata.com).