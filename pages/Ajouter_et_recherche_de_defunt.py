import pandas as pd
import streamlit as st
import folium as flm
import geopandas as gpd
import json
import os # Importation du module os pour gérer les chemins de fichiers
from streamlit_folium import st_folium

# --- Configuration des fichiers ---
# Nom du fichier pour la sauvegarde des données des défunts.
# Ce fichier sera créé dans le même répertoire que votre script app.py.
DATA_FILE = "defunts_data.json"

# Chemin du fichier GeoJSON pour la carte.
# Assurez-vous que "tombes.geojson" est AUSSI dans le même répertoire que app.py sur GitHub.
GEOJSON_FILE_PATH = "tombes.geojson"

# --- Fonctions pour la persistance des données ---

def load_data():
    """
    Charge les données des défunts depuis le fichier JSON.
    Si le fichier n'existe pas, initialise une base de données vide.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Convertir les listes en types de données appropriés si nécessaire après chargement
            # Exemple: Les dates/heures chargées comme str doivent être gérées comme telles dans l'app
            return data
        except json.JSONDecodeError:
            st.error("Erreur lors de la lecture du fichier de données. Le fichier est peut-être corrompu.")
            return initialize_empty_data() # Retourne une BD vide en cas d'erreur de lecture
    else:
        return initialize_empty_data()

def initialize_empty_data():
    """Initialise une structure de données vide pour les défunts."""
    return {
        'Nom': [], 'Prenom': [], 'Date_de_naissance': [],
        'Lieux_de_naissance': [], 'Lieux_de_residence': [],
        'CNI': [], 'Date_du_deces': [], 'Heure_du_deces': [],
        'Nom_du_déclarant': [], 'Prenom_du_déclarant': [],
        'CNI_du_déclarant': [], 'Liens_avec_le_defunt': [],
        'Numero_de_telephone': [], 'Delivrance_du_Permis_d_inhumer': [],
        'Numero_de_section': [], 'Numero_de_la_serie': [], 'Numero_de_la_tombe': [],
    }

def save_data(data):
    """
    Sauvegarde les données des défunts dans un fichier JSON.
    Utilise 'default=str' pour gérer la sérialisation des objets non JSON (comme les dates/temps).
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # st.date_input et st.time_input retournent des objets date et time.
            # json.dump ne sait pas les sérialiser directement.
            # default=str convertira ces objets en chaînes de caractères avant la sauvegarde.
            json.dump(data, f, default=str, indent=4)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des données : {e}")

# --- Titres de l'application ---
st.title("Page de gestion des défunts")
st.title("Bienvenue")

# --- Initialisation de la base de données en session_state ---
# La base de données est chargée au démarrage de l'application.
# Si elle n'est pas encore dans st.session_state, on la charge depuis le fichier.
if 'BD' not in st.session_state:
    st.session_state.BD = load_data()

# --- Gestion des choix utilisateur (Ajouter/Rechercher) ---
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

    # Clés uniques ajoutées pour éviter les warnings si le même widget est appelé plusieurs fois
    NOM = st.text_input("Nom du défunt", key="add_nom_defunt")
    PRENOM = st.text_input("Prénom du défunt", key="add_prenom_defunt")
    DATE_NAISSANCE = st.date_input("Date de naissance", key="add_date_naissance")
    LIEU_NAISSANCE = st.text_input("Lieu de naissance", key="add_lieu_naissance")
    LIEU_RESIDENCE = st.text_input("Lieu de résidence", key="add_lieu_residence")
    CNI_DEFUNT = st.number_input("Numéro de CNI du défunt", step=1, key="add_cni_defunt")
    DATE_DECES = st.date_input("Date du décès", key="add_date_deces")
    HEURE_DECES = st.time_input("Heure du décès", key="add_heure_deces")

    st.subheader("Personne à contacter")
    NOM_CONTACT = st.text_input("Nom", key="add_nom_contact")
    PRENOM_CONTACT = st.text_input("Prénom", key="add_prenom_contact")
    CNI_CONTACT = st.number_input("Numéro de CNI", step=1, key="add_cni_contact")
    LIEN_CONTACT = st.text_input("Lien avec le défunt", key="add_lien_contact")
    TELEPHONE_CONTACT = st.number_input("Téléphone", step=1, key="add_tel_contact")

    st.subheader("Inhumation")
    PERMIS_INHUMER = st.number_input("Numéro du permis d'inhumer", step=1, key="add_permis_inhumer")
    SECTION_TOMBE = st.number_input("Numéro de section", step=1, key="add_section_tombe")
    SERIE_TOMBE = st.number_input("Numéro de série", step=1, key="add_serie_tombe")
    NUMERO_TOMBE = st.number_input("Numéro de la tombe", step=1, key="add_numero_tombe")

    if st.button("Enregistrer", key="btn_enregistrer_defunt"):
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

        # --- Sauvegarde des données après l'enregistrement ---
        save_data(BD)

# ---------------------------------------
# Partie : Recherche
# ---------------------------------------
# Le 'choix_utilisateur' par défaut est 'Rechercher defunt' si rien n'a été choisi
if 'choix_utilisateur' not in st.session_state:
    st.session_state.choix_utilisateur = ['Rechercher defunt'] # Pour que la recherche soit visible par défaut

if 'Rechercher defunt' in st.session_state.choix_utilisateur:
    st.header("🔍 Rechercher un défunt")

    # Utilisation de st.form pour regrouper les éléments de recherche et le bouton
    with st.form(key='form_recherche_defunt'):
        st.subheader("Critères de recherche")
        nom_recherche = st.text_input("Nom du défunt", key="search_nom_input")
        prenom_recherche = st.text_input("Prénom du défunt", key="search_prenom_input")
        permis_recherche = st.text_input("Numéro du permis d'inhumer", key="search_permis_input")

        submitted = st.form_submit_button("Rechercher le défunt")

    # La logique de recherche se déclenche UNIQUEMENT quand le formulaire est soumis
    if submitted:
        df = pd.DataFrame(st.session_state.BD)

        if df.empty:
            st.warning("⚠️ La base de données est vide. Aucun défunt à rechercher.")
        else:
            # Assurez-vous que les colonnes sont des chaînes de caractères pour la recherche
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

    # --- Localisation sur le plan du cimetière ---
    st.subheader("Localisation sur le plan du cimetière")

    try:
        # Charger le fichier GeoJSON en utilisant le chemin relatif corrigé
        with open(GEOJSON_FILE_PATH, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        # Coordonnées centrées sur le cimetière (à ajuster si besoin)
        # Ces coordonnées (latitude, longitude) sont pour le centre du cimetière de Yoff, Dakar.
        carte = flm.Map(location=[14.755922, -17.399996], zoom_start=15, tiles="OpenStreetMap")
        flm.GeoJson(geojson_data, name="cimetiere_tombes").add_to(carte)
        flm.LayerControl().add_to(carte)

        # Afficher la carte Folium dans Streamlit
        st_folium(carte, width=700, height=500)

    except FileNotFoundError:
        st.error(f"❌ Erreur : Le fichier GeoJSON '{GEOJSON_FILE_PATH}' est introuvable. Veuillez vous assurer qu'il est bien dans le même dossier que votre application.")
    except json.JSONDecodeError:
        st.error(f"❌ Erreur : Le fichier '{GEOJSON_FILE_PATH}' n'est pas un fichier JSON valide ou est corrompu.")
    except Exception as e:
        st.error(f"❌ Une erreur inattendue est survenue lors du chargement ou de l'affichage de la carte : {e}")
