import pandas as pd
import streamlit as st
import folium as flm
import geopandas as gpd
import json
from streamlit_folium import st_folium

st.title("Page de gestion des défunts")
st.title("Bienvenue")

# Initialisation de la base de données
if 'BD' not in st.session_state:
    st.session_state.BD = {
        'Nom': [], 'Prenom': [], 'Date_de_naissance': [],
        'Lieux_de_naissance': [], 'Lieux_de_residence': [],
        'CNI': [], 'Date_du_deces': [], 'Heure_du_deces': [],
        'Nom_du_déclarant': [], 'Prenom_du_déclarant': [],
        'CNI_du_déclarant': [], 'Liens_avec_le_defunt': [],
        'Numero_de_telephone': [], 'Delivrance_du_Permis_d_inhumer': [],
        'Numero_de_section': [], 'Numero_de_la_serie': [], 'Numero_de_la_tombe': [],
    }

# Mémoriser les choix dans la session
if 'choix_utilisateur' not in st.session_state:
    st.session_state.choix_utilisateur = []

choix = st.multiselect("Que voulez-vous faire ?", ['Ajouter defunt', 'Rechercher defunt'])

if st.button("Valider"):
    st.session_state.choix_utilisateur = choix

# ---------------------------------------
# Partie : Ajout de défunt
# ---------------------------------------
if 'Ajouter defunt' in st.session_state.choix_utilisateur:
    st.header("📝 Ajout d'un défunt")
    st.subheader("Informations du défunt")

    NOM = st.text_input("Nom du défunt", key="nom_defunt")
    PRENOM = st.text_input("Prénom du défunt", key="prenom_defunt")
    DATE_NAISSANCE = st.date_input("Date de naissance", key="date_naissance")
    LIEU_NAISSANCE = st.text_input("Lieu de naissance", key="lieu_naissance")
    LIEU_RESIDENCE = st.text_input("Lieu de résidence", key="lieu_residence")
    CNI_DEFUNT = st.number_input("Numéro de CNI du défunt", step=1, key="cni_defunt")
    DATE_DECES = st.date_input("Date du décès", key="date_deces")
    HEURE_DECES = st.time_input("Heure du décès", key="heure_deces")

    st.subheader("Personne à contacter")
    NOM_CONTACT = st.text_input("Nom", key="nom_contact")
    PRENOM_CONTACT = st.text_input("Prénom", key="prenom_contact")
    CNI_CONTACT = st.number_input("Numéro de CNI", step=1, key="cni_contact")
    LIEN_CONTACT = st.text_input("Lien avec le défunt", key="lien_contact")
    TELEPHONE_CONTACT = st.number_input("Téléphone", step=1, key="tel_contact")

    st.subheader("Inhumation")
    PERMIS_INHUMER = st.number_input("Numéro du permis d'inhumer", step=1, key="permis_inhumer")
    SECTION_TOMBE = st.number_input("Numéro de section", step=1, key="section_tombe")
    SERIE_TOMBE = st.number_input("Numéro de série", step=1, key="serie_tombe")
    NUMERO_TOMBE = st.number_input("Numéro de la tombe", step=1, key="numero_tombe")

    if st.button("Enregistrer"):
        BD = st.session_state.BD
        BD['Nom'].append(NOM)
        BD['Prenom'].append(PRENOM)
        BD['Date_de_naissance'].append(DATE_NAISSANCE)
        BD['Lieux_de_naissance'].append(LIEU_NAISSANCE)
        BD['Lieux_de_residence'].append(LIEU_RESIDENCE)
        BD['CNI'].append(CNI_DEFUNT)
        BD['Date_du_deces'].append(DATE_DECES)
        BD['Heure_du_deces'].append(HEURE_DECES)
        BD['Nom_du_déclarant'].append(NOM_CONTACT)
        BD['Prenom_du_déclarant'].append(PRENOM_CONTACT)
        BD['CNI_du_déclarant'].append(CNI_CONTACT)
        BD['Liens_avec_le_defunt'].append(LIEN_CONTACT)
        BD['Numero_de_telephone'].append(TELEPHONE_CONTACT)
        BD['Delivrance_du_Permis_d_inhumer'].append(PERMIS_INHUMER)
        BD['Numero_de_section'].append(SECTION_TOMBE)
        BD['Numero_de_la_serie'].append(SERIE_TOMBE)
        BD['Numero_de_la_tombe'].append(NUMERO_TOMBE)

        st.success("✅ Défunt enregistré avec succès.")
        st.dataframe(pd.DataFrame(BD))
       
# ---------------------------------------
# Partie : Recherche
# ---------------------------------------
if 'choix_utilisateur' not in st.session_state:
    st.session_state.choix_utilisateur = ['Rechercher defunt']


if 'Rechercher defunt' in st.session_state.choix_utilisateur:
    st.header("🔍 Rechercher un défunt")

    # --- Début du formulaire pour la recherche ---
    # Tous les éléments du formulaire (champs de saisie et bouton de soumission)
    # doivent être placés à l'intérieur de ce bloc `with st.form(...)`.
    with st.form(key='form_recherche_defunt'):
        st.subheader("Critères de recherche")
        nom_recherche = st.text_input("Nom du défunt", key="search_nom_input") # Clé unique
        prenom_recherche = st.text_input("Prénom du défunt", key="search_prenom_input") # Clé unique
        permis_recherche = st.text_input("Numéro du permis d'inhumer", key="search_permis_input") # Clé unique

        # Le bouton de soumission du formulaire doit être DANS le bloc 'with st.form'
        submitted = st.form_submit_button("Rechercher le défunt")

    # --- La logique de recherche se déclenche UNIQUEMENT quand le formulaire est soumis ---
    if submitted:
        # S'assurer que la BD est transformée en DataFrame pour la recherche
        df = pd.DataFrame(st.session_state.BD)

        if df.empty:
            st.warning("⚠️ La base de données est vide. Aucun défunt à rechercher.")
        else:
            
            
            df['Nom'] = df['Nom'].astype(str)
            df['Prenom'] = df['Prenom'].astype(str)
            df['Delivrance_du_Permis_d_inhumer'] = df['Delivrance_du_Permis_d_inhumer'].astype(str)

            # Effectuer la recherche en ignorant la casse et les espaces superflus
            resultats = df[
                (df['Nom'].str.strip().str.lower() == nom_recherche.strip().lower()) &
                (df['Prenom'].str.strip().str.lower() == prenom_recherche.strip().lower()) &
                (df['Delivrance_du_Permis_d_inhumer'].str.strip() == permis_recherche.strip())
            ]

            if not resultats.empty:
                st.success(f"✅ {len(resultats)} résultat(s) trouvé(s) :")
                st.dataframe(resultats)
            else:
                st.error("❌ Aucun défunt trouvé avec ces critères. Veuillez vérifier les informations saisies.")

    

    ## Localisation sur le plan du cimetière

    # Cette partie de la carte peut être affichée indépendamment de la soumission du formulaire.
    st.subheader("Localisation sur le plan du cimetière")

    # Assurez-vous que ce chemin est correct et accessible depuis l'environnement où l'application s'exécute.
    # Le chemin indiqué est un chemin absolu Windows. Assurez-vous que le fichier est bien là.
    geojson_path = "C:\\Users\\dell\\Desktop\\plateforme\\tombes.geojson"
    try:
        # Charger le fichier GeoJSON
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        
        # Coordonnées : [Latitude, Longitude] pour le centre du cimetière 
        carte = flm.Map(location=[14.755922, -17.399996], zoom_start=15, tiles="OpenStreetMap")
        flm.GeoJson(geojson_data, name="cimetiere_tombes").add_to(carte)
        flm.LayerControl().add_to(carte)

        # Afficher la carte Folium dans Streamlit
        st_folium(carte, width=700, height=500)

    except FileNotFoundError:
        st.error(f"❌ Erreur : Le fichier GeoJSON '{geojson_path}' est introuvable. Vérifiez le chemin d'accès.")
    except json.JSONDecodeError:
        st.error(f"❌ Erreur : Le fichier '{geojson_path}' n'est pas un fichier JSON valide.")
    except Exception as e:
        st.error(f"❌ Une erreur inattendue est survenue lors du chargement ou de l'affichage de la carte : {e}")