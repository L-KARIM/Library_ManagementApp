import streamlit as st
import datetime

# Classe pour représenter un livre
class Livre:
    def __init__(self, titre, auteur, genre, statut="Disponible"):
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.statut = statut
        self.next = None  # Pour la liste chaînée

# Classe pour gérer les livres avec liste chaînée
class GestionLivres:
    def __init__(self):
        self.head = None
    
    def ajouter_livre(self, titre, auteur, genre):
        nouveau_livre = Livre(titre, auteur, genre)
        
        # Si la liste est vide
        if not self.head:
            self.head = nouveau_livre
            return
        
        # Sinon, ajouter à la fin
        current = self.head
        while current.next:
            current = current.next
        current.next = nouveau_livre
    
    def supprimer_livre(self, titre):
        if not self.head:
            return False
        
        # Si c'est le premier élément
        if self.head.titre == titre:
            self.head = self.head.next
            return True
        
        # Sinon, chercher dans la liste
        current = self.head
        while current.next and current.next.titre != titre:
            current = current.next
        
        if current.next:
            current.next = current.next.next
            return True
        return False
    
    def obtenir_tous_livres(self):
        livres = []
        current = self.head
        while current:
            livres.append({
                "titre": current.titre,
                "auteur": current.auteur,
                "genre": current.genre,
                "statut": current.statut
            })
            current = current.next
        return livres
    
    def changer_statut(self, titre, nouveau_statut):
        current = self.head
        while current:
            if current.titre == titre:
                current.statut = nouveau_statut
                return True
            current = current.next
        return False
    
    def rechercher_livre(self, titre):
        current = self.head
        while current:
            if current.titre == titre:
                return {
                    "titre": current.titre,
                    "auteur": current.auteur,
                    "genre": current.genre,
                    "statut": current.statut
                }
            current = current.next
        return None

# Classe pour gérer les emprunts avec pile
class Emprunts:
    def __init__(self):
        self.pile = []
    
    def enregistrer_emprunt(self, titre):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        self.pile.append({"titre": titre, "date": date, "type": "Emprunt"})
    
    def enregistrer_retour(self, titre):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        self.pile.append({"titre": titre, "date": date, "type": "Retour"})
    
    def obtenir_historique(self):
        return self.pile

# Nœud pour l'arbre binaire
class NoeudArbre:
    def __init__(self, livre):
        self.livre = livre
        self.gauche = None
        self.droite = None

# Classe pour l'organisation et recherche avec arbre binaire
class Bibliotheque:
    def __init__(self):
        self.racine = None
    
    def ajouter_livre(self, livre):
        if not self.racine:
            self.racine = NoeudArbre(livre)
        else:
            self._ajouter_recursif(self.racine, livre)
    
    def _ajouter_recursif(self, noeud, livre):
        if livre.titre < noeud.livre.titre:
            if noeud.gauche is None:
                noeud.gauche = NoeudArbre(livre)
            else:
                self._ajouter_recursif(noeud.gauche, livre)
        else:
            if noeud.droite is None:
                noeud.droite = NoeudArbre(livre)
            else:
                self._ajouter_recursif(noeud.droite, livre)
    
    def rechercher_livre(self, titre):
        return self._rechercher_recursif(self.racine, titre)
    
    def _rechercher_recursif(self, noeud, titre):
        if noeud is None:
            return None
        
        if titre == noeud.livre.titre:
            return noeud.livre
        
        if titre < noeud.livre.titre:
            return self._rechercher_recursif(noeud.gauche, titre)
        else:
            return self._rechercher_recursif(noeud.droite, titre)
    
    def obtenir_livres_ordre_alphabetique(self):
        livres = []
        self._parcours_infixe(self.racine, livres)
        return livres
    
    def _parcours_infixe(self, noeud, livres):
        if noeud:
            self._parcours_infixe(noeud.gauche, livres)
            livres.append({
                "titre": noeud.livre.titre,
                "auteur": noeud.livre.auteur,
                "genre": noeud.livre.genre,
                "statut": noeud.livre.statut
            })
            self._parcours_infixe(noeud.droite, livres)

# Interface Streamlit
def main():
    st.set_page_config(page_title="Gestion de Bibliothèque", page_icon="📚")
    
    # CSS personnalisé
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .title {
        color: #1e3d59;
        text-align: center;
    }
    .section-header {
        background-color: #1e3d59;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .book-card {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #1e3d59;
    }
    .available {
        color: green;
        font-weight: bold;
    }
    .borrowed {
        color: red;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="title">Gestion de Bibliothèque</h1>', unsafe_allow_html=True)
    
    # Initialisation des instances dans le state de session
    if 'gestion_livres' not in st.session_state:
        st.session_state.gestion_livres = GestionLivres()
        st.session_state.emprunts = Emprunts()
        st.session_state.bibliotheque = Bibliotheque()
        
        # Ajout de livres exemples
        st.session_state.gestion_livres.ajouter_livre("Python Basics", "John Smith", "Informatique")
        st.session_state.gestion_livres.ajouter_livre("L'Histoire de l'Humanité", "Anne Dubois", "Histoire")
        
        # Mise à jour de l'arbre binaire
        livre1 = Livre("Python Basics", "John Smith", "Informatique")
        livre2 = Livre("L'Histoire de l'Humanité", "Anne Dubois", "Histoire")
        st.session_state.bibliotheque.ajouter_livre(livre1)
        st.session_state.bibliotheque.ajouter_livre(livre2)
    
    # Création des onglets
    tab1, tab2, tab3, tab4 = st.tabs(["Ajouter un livre", "Gestion des livres", "Emprunts/Retours", "Recherche"])
    
    # Onglet Ajouter un livre
    with tab1:
        st.markdown('<div class="section-header">Ajouter un nouveau livre</div>', unsafe_allow_html=True)
        
        titre = st.text_input("Titre du livre")
        auteur = st.text_input("Auteur")
        genre = st.selectbox("Genre", ["Fiction", "Histoire", "Science", "Informatique", "Biographie", "Autre"])
        
        if st.button("Ajouter le livre"):
            if titre and auteur:
                st.session_state.gestion_livres.ajouter_livre(titre, auteur, genre)
                
                # Ajouter à l'arbre binaire
                nouveau_livre = Livre(titre, auteur, genre)
                st.session_state.bibliotheque.ajouter_livre(nouveau_livre)
                
                st.success(f"Le livre '{titre}' a été ajouté avec succès!")
            else:
                st.error("Veuillez remplir tous les champs obligatoires.")
    
    # Onglet Gestion des livres
    with tab2:
        st.markdown('<div class="section-header">Liste des livres</div>', unsafe_allow_html=True)
        
        livres = st.session_state.gestion_livres.obtenir_tous_livres()
        
        if not livres:
            st.info("Aucun livre dans la bibliothèque.")
        else:
            for livre in livres:
                statut_class = "available" if livre["statut"] == "Disponible" else "borrowed"
                st.markdown(f"""
                <div class="book-card">
                    <h3>{livre["titre"]}</h3>
                    <p><strong>Auteur:</strong> {livre["auteur"]}</p>
                    <p><strong>Genre:</strong> {livre["genre"]}</p>
                    <p><strong>Statut:</strong> <span class="{statut_class}">{livre["statut"]}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">Supprimer un livre</div>', unsafe_allow_html=True)
        
        titres = [livre["titre"] for livre in livres]
        if titres:
            titre_a_supprimer = st.selectbox("Sélectionner un livre à supprimer", titres)
            
            if st.button("Supprimer"):
                if st.session_state.gestion_livres.supprimer_livre(titre_a_supprimer):
                    st.success(f"Le livre '{titre_a_supprimer}' a été supprimé avec succès!")
                else:
                    st.error("Erreur lors de la suppression du livre.")
        else:
            st.info("Aucun livre à supprimer.")
    
    # Onglet Emprunts/Retours
    with tab3:
        st.markdown('<div class="section-header">Gestion des emprunts et retours</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Emprunter un livre")
            
            livres_dispo = [livre["titre"] for livre in st.session_state.gestion_livres.obtenir_tous_livres() 
                             if livre["statut"] == "Disponible"]
            
            if livres_dispo:
                livre_a_emprunter = st.selectbox("Sélectionner un livre à emprunter", livres_dispo)
                
                if st.button("Emprunter"):
                    st.session_state.gestion_livres.changer_statut(livre_a_emprunter, "Emprunté")
                    st.session_state.emprunts.enregistrer_emprunt(livre_a_emprunter)
                    st.success(f"Le livre '{livre_a_emprunter}' a été emprunté avec succès!")
            else:
                st.info("Aucun livre disponible pour emprunt.")
        
        with col2:
            st.subheader("Retourner un livre")
            
            livres_empruntes = [livre["titre"] for livre in st.session_state.gestion_livres.obtenir_tous_livres() 
                                 if livre["statut"] == "Emprunté"]
            
            if livres_empruntes:
                livre_a_retourner = st.selectbox("Sélectionner un livre à retourner", livres_empruntes)
                
                if st.button("Retourner"):
                    st.session_state.gestion_livres.changer_statut(livre_a_retourner, "Disponible")
                    st.session_state.emprunts.enregistrer_retour(livre_a_retourner)
                    st.success(f"Le livre '{livre_a_retourner}' a été retourné avec succès!")
            else:
                st.info("Aucun livre emprunté à retourner.")
        
        st.markdown('<div class="section-header">Historique des emprunts et retours</div>', unsafe_allow_html=True)
        
        historique = st.session_state.emprunts.obtenir_historique()
        
        if historique:
            for operation in historique:
                icon = "📤" if operation["type"] == "Emprunt" else "📥"
                st.write(f"{icon} **{operation['type']}** - '{operation['titre']}' le {operation['date']}")
        else:
            st.info("Aucun historique d'emprunts ou de retours.")
    
    # Onglet Recherche
    with tab4:
        st.markdown('<div class="section-header">Rechercher un livre</div>', unsafe_allow_html=True)
        
        recherche = st.text_input("Titre du livre à rechercher")
        
        if recherche:
            resultat = st.session_state.bibliotheque.rechercher_livre(recherche)
            
            if resultat:
                statut_class = "available" if resultat.statut == "Disponible" else "borrowed"
                st.markdown(f"""
                <div class="book-card">
                    <h3>{resultat.titre}</h3>
                    <p><strong>Auteur:</strong> {resultat.auteur}</p>
                    <p><strong>Genre:</strong> {resultat.genre}</p>
                    <p><strong>Statut:</strong> <span class="{statut_class}">{resultat.statut}</span></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"Aucun livre trouvé avec le titre '{recherche}'")
        
        st.markdown('<div class="section-header">Livres par ordre alphabétique</div>', unsafe_allow_html=True)
        
        if st.button("Afficher tous les livres par ordre alphabétique"):
            livres_ordonnes = st.session_state.bibliotheque.obtenir_livres_ordre_alphabetique()
            
            if livres_ordonnes:
                for livre in livres_ordonnes:
                    statut_class = "available" if livre["statut"] == "Disponible" else "borrowed"
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{livre["titre"]}</h3>
                        <p><strong>Auteur:</strong> {livre["auteur"]}</p>
                        <p><strong>Genre:</strong> {livre["genre"]}</p>
                        <p><strong>Statut:</strong> <span class="{statut_class}">{livre["statut"]}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aucun livre dans la bibliothèque.")

if __name__ == "__main__":
    main()