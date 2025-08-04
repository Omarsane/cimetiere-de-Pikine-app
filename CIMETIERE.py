# Importation des bibliothèques nécessaires
import streamlit as st
from PIL import Image

# Titre centré de la page
st.markdown(
    "<h1 style='text-align: center; color: green;'>Gestion du Cimetière Municipal de la Ville de Pikine</h1>",
    unsafe_allow_html=True
)

# Utilisation de Pillow pour ouvrir l'image de manière fiable
try:
    # Changement du nom de fichier ici pour utiliser le .ovr
    image_path = "images/cimetiere.tif.ovr"
    image = Image.open(image_path)
    st.image(image)
except FileNotFoundError:
    st.error("Le fichier images/cimetiere.tif.ovr n'a pas été trouvé.")

# Création de la barre latérale
with st.sidebar:
    st.info("Sur cette plateforme, vous pouvez rechercher, ajouter ou supprimer un défunt.")
    st.warning("NB: Seuls les gestionnaires du cimetière ont le droit de supprimer ou d'ajouter un défunt.")

# Lien vers la carte du cimetière
st.page_link(
    "https://umap.openstreetmap.fr/fr/map/cimetiere-de-piking_1226453?scaleControl=false&miniMap=fa", 
    label="Cliquer ici pour aller vers la carte du Cimetière de Piking"
)