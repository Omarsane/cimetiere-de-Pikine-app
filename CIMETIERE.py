import streamlit as st
#titre centre
st.markdown(
    "<h1 style='text-align: center; color: green;'>Gestion du Cimetière Municipal de la Ville de Pikine</h1>",
    unsafe_allow_html=True
)

st.image("C:\\Users\\dell\\Desktop\\plateforme\\images\\cimetiere.tif")
with st.sidebar:
    st.info("Sur cette plateforme;vous pouvez rechercher,ajouter ou supprimer un défunt ")
    
    st.warning("NB:Seul les gestionnaires du cimetiere ont le droit de supprimer ou d'ajouter un défunt.")

st.page_link("https://umap.openstreetmap.fr/fr/map/cimetiere-de-piking_1226453?scaleControl=false&miniMap=fa", label="Cliquer ici pour aller vers la carte du Cimetière de Piking")
