import streamlit as st

# Titre centré de la page
st.markdown(
    "<h1 style='text-align: center; color: green;'>Gestion du Cimetière Municipal de la Ville de Pikine</h1>",
    unsafe_allow_html=True
)

# Remplacement de l'image par le texte descriptif
st.markdown(
    """
    Créé en 1952, le cimetière municipal de la ville de
    Pikine s'étend sur une superficie de 40 733 mètres carrés. Il est situé dans le
    département de Pikine, plus précisément dans la commune de Pikine Ouest. Ses
    coordonnées géographiques sont comprises entre 14°45'25" de latitude Nord
    et 17°24'0" de longitude Ouest. Cette commune est délimitée au nord par
    les communes de Pikine Nord et Pikine Sud, à l'est par la commune de Pikine
    Est, au sud-est par la commune de Guinaw Rail Sud, au sud-ouest par la commune
    de Dalifort, et à l'ouest par la commune de Golf Sud.
    """
)

# Création de la barre latérale
with st.sidebar:
    st.info("Sur cette plateforme, vous pouvez rechercher, ajouter ou supprimer un défunt.")
    st.warning("NB: Seuls les gestionnaires du cimetière ont le droit de supprimer ou d'ajouter un défunt.")

# Lien vers la carte du cimetière
st.page_link(
    "https://umap.openstreetmap.fr/fr/map/cimetiere-de-piking_1226453?scaleControl=false&miniMap=fa", 
    label="Cliquer ici pour aller vers la carte du Cimetière de Piking"
)
