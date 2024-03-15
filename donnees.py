# %%
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
import plotly.colors as pc

# %%
ensemble_clients_olist  = pd.read_csv('data/olist_customers_dataset.csv')
ensemble_geolocalisation_olist = pd.read_csv('data/olist_geolocation_dataset.csv')
ensemble_articles_commandes_olist = pd.read_csv('data/olist_order_items_dataset.csv')
ensemble_paiements_commandes_olist = pd.read_csv('data/olist_order_payments_dataset.csv')
ensemble_avis_commandes_olist = pd.read_csv('data/olist_order_reviews_dataset.csv')
ensemble_commandes_olist = pd.read_csv('data/olist_orders_dataset.csv')
ensemble_produits_olist = pd.read_csv('data/olist_products_dataset.csv')
ensemble_vendeurs_olist = pd.read_csv('data/olist_sellers_dataset.csv')
traduction_nom_categorie_produit = pd.read_csv('data/product_category_name_translation.csv')

# %% [markdown]
# # Traduction des champs des datasets

# %%
ensemble_clients_olist_dict = {
    'customer_id': 'identifiant_client',
    'customer_unique_id': 'identifiant_unique_client',
    'customer_zip_code_prefix': 'prefixe_code_postal_client',
    'customer_city': 'ville_client',
    'customer_state': 'etat_client'
}

# %%
ensemble_clients_olist = ensemble_clients_olist.rename(columns=ensemble_clients_olist_dict)

# %%
ensemble_clients_olist.head()

# %%
ensemble_geolocalisation_olist_dict = {
    'geolocation_zip_code_prefix': 'prefixe_code_postal_geolocalisation',
    'geolocation_lat': 'latitude_geolocalisation',
    'geolocation_lng': 'longitude_geolocalisation',
    'geolocation_city': 'ville_geolocalisation',
    'geolocation_state': 'etat_geolocalisation'
}

# %%
ensemble_geolocalisation_olist = ensemble_geolocalisation_olist.rename(columns=ensemble_geolocalisation_olist_dict)

# %%
ensemble_geolocalisation_olist.head()

# %%
ensemble_articles_commandes_olist_dict = {
    'order_id': 'identifiant_commande',
    'order_item_id': 'identifiant_article_commande',
    'product_id': 'identifiant_produit',
    'seller_id': 'identifiant_vendeur',
    'shipping_limit_date': 'date_limite_expedition',
    'price': 'prix',
    'freight_value': 'valeur_fret'
}

# %%
ensemble_articles_commandes_olist = ensemble_articles_commandes_olist.rename(columns=ensemble_articles_commandes_olist_dict)

# %%
ensemble_articles_commandes_olist.head()

# %%
ensemble_paiements_commandes_olist_dict= {
    'order_id': 'identifiant_commande',
    'payment_sequential': 'sequence_paiement',
    'payment_type': 'type_paiement',
    'payment_installments': 'versements_paiement',
    'payment_value': 'valeur_paiement'
}

# %%
ensemble_paiements_commandes_olist = ensemble_paiements_commandes_olist.rename(columns=ensemble_paiements_commandes_olist_dict)

# %%
ensemble_paiements_commandes_olist.head()

# %%
ensemble_avis_commandes_olist_dict = {
    'review_id': 'identifiant_avis',
    'order_id': 'identifiant_commande',
    'review_score': 'score_avis',
    'review_comment_title': 'titre_commentaire_avis',
    'review_comment_message': 'message_commentaire_avis',
    'review_creation_date': 'date_creation_avis',
    'review_answer_timestamp': 'timestamp_reponse_avis'
}

# %%
ensemble_avis_commandes_olist = ensemble_avis_commandes_olist.rename(columns = ensemble_avis_commandes_olist_dict)

# %%
ensemble_avis_commandes_olist.head()

# %%
ensemble_commandes_olist_dict = {
    'order_id': 'identifiant_commande',
    'customer_id': 'identifiant_client',
    'order_status': 'statut_commande',
    'order_purchase_timestamp': 'timestamp_achat_commande',
    'order_approved_at': 'commande_approuvee_a',
    'order_delivered_carrier_date': 'date_livraison_transporteur_commande',
    'order_delivered_customer_date': 'date_livraison_client_commande',
    'order_estimated_delivery_date': 'date_livraison_estimee_commande'
}

# %%
ensemble_commandes_olist = ensemble_commandes_olist.rename(columns=ensemble_commandes_olist_dict)

# %%
ensemble_commandes_olist.head()

# %%
ensemble_produits_olist_dict = {
    'product_id': 'identifiant_produit',
    'product_category_name': 'nom_categorie_produit',
    'product_name_lenght': 'longueur_nom_produit',
    'product_description_lenght': 'longueur_description_produit',
    'product_photos_qty': 'quantite_photos_produit',
    'product_weight_g': 'poids_produit_g',
    'product_length_cm': 'longueur_produit_cm',
    'product_height_cm': 'hauteur_produit_cm',
    'product_width_cm': 'largeur_produit_cm'
}

# %%
ensemble_produits_olist = ensemble_produits_olist.rename(columns=ensemble_produits_olist_dict)

# %%
ensemble_produits_olist.head()

# %%
ensemble_vendeurs_olist_dict = {
    'seller_id': 'identifiant_vendeur',
    'seller_zip_code_prefix': 'prefixe_code_postal_vendeur',
    'seller_city': 'ville_vendeur',
    'seller_state': 'etat_vendeur'
}

# %%
ensemble_vendeurs_olist = ensemble_vendeurs_olist.rename(columns=ensemble_vendeurs_olist_dict)

# %%
ensemble_vendeurs_olist.head()

# %%
traduction_nom_categorie_produit_dict = {
    'product_category_name': 'nom_categorie_produit',
    'product_category_name_english': 'nom_categorie_produit_anglais'
}

# %%
traduction_nom_categorie_produit =traduction_nom_categorie_produit.rename(columns=traduction_nom_categorie_produit_dict)

# %%
traduction_nom_categorie_produit.head()

# %% [markdown]
# # Nettoyage des données

# %% [markdown]
# Suppression des doublons

# %%
def supprimer_les_doublons(liste_datas):
    """supprimer_les_doublons

    Args:
        liste_datas (liste): listes des Dataframes
    """
    for i, data in enumerate(liste_datas):
        liste_datas[i] = data.drop_duplicates(inplace=True)


# %%
liste_datas=[
    ensemble_clients_olist,
    ensemble_geolocalisation_olist,
    ensemble_articles_commandes_olist,
    ensemble_paiements_commandes_olist,
    ensemble_avis_commandes_olist,
    ensemble_commandes_olist,
    ensemble_produits_olist,
    ensemble_vendeurs_olist,
    traduction_nom_categorie_produit
]
supprimer_les_doublons(liste_datas=liste_datas)

# %% [markdown]
# Traitement des valeurs aberrantes ou manquantes.

# %%
def calculer_les_indices_de_dispertions(data,target):
    """Calculer les indices de dispertions
    Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter

    Returns:
        tuple: indice_dispertion_positive,indice_dispertion_négative
    """
    indice_dispertion_positive = 1.5 * (data[target].quantile(q=0.75 - 0.25))
    indice_dispertion_négative = -1.5 * (data[target].quantile(q=0.75 - 0.25))
    return indice_dispertion_positive,indice_dispertion_négative

# %%
def créer_un_sous_ensemble_de_données(data,target):
    """Calculer les indices de dispertions
    Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter

    Returns:
        Dataframe: indice_dispertion_positive,indice_dispertion_négative
    """
    indice_dispertion_positive,indice_dispertion_négative = calculer_les_indices_de_dispertions(data,target)
    data_sub = data[~((data[target] > indice_dispertion_positive) | (data[target] < indice_dispertion_négative))] 
    return data_sub

# %%
def remplacer_les_valeurs_extrèmes_par_des_NaN(data,target):
    """Remplacer les valeurs extrèmes par des NaN
    Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter
    """
    indice_dispertion_positive,indice_dispertion_négative = calculer_les_indices_de_dispertions(data,target)
    condition = (data[target] > indice_dispertion_positive) | (data[target] < indice_dispertion_négative)
    data.loc[condition, target] = np.nan

# %%
def découpage_train_test(data,target,feature):
    """découpage train test
    Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    x = data[target].to_numpy()
    y = data[feature].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# %%
def entrainer_régression_linéaire_et_prédire(data,target,feature):
    """Entrainer régression linéaire et prédire
    Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter
    Returns:
        tuple: coeffs,y_pred, mse
    """
    X, y, = découpage_train_test(data,target,feature)[0], découpage_train_test(data,target,feature)[2]
    coeffs = np.polyfit(X, y, 1)
    y_pred = np.polyval(coeffs,X)
    y_pred = pd.Series(y_pred)
    mse = np.mean(y - y_pred)**2
    fig = px.scatter(
    x=X, y=y_pred, opacity=0.65,
    trendline='ols', trendline_color_override='darkblue'
    )
    fig.show()
    return coeffs,y_pred, mse

# %%
def tester_régression_linéaire_et_prédire(data,target,feature,coeffs):
    """Tester régression linéaire et prédire
      Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter
    Returns:
        tuple: y_pred, mse
    """
    X, y, = découpage_train_test(data,target,feature)[1], découpage_train_test(data,target,feature)[3]
    y_pred = np.polyval(coeffs,X)
    y_pred = pd.Series(y_pred)
    mse = np.mean(y - y_pred)**2
    fig = px.scatter(
    x=X, y=y_pred, opacity=0.65,
    trendline='ols', trendline_color_override='darkblue'
    )
    fig.show()
    return y_pred, mse

# %%
def remplacer_les_NaN_par_des_prédictions(data,target,feature,coeffs):
    """remplacer les NaN par des prédictions
      Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter
        feature (str): colonne à traiter
        coeffs (ndarray): coefficients a et b
    """
    predictions = np.polyval(coeffs, data[feature])
    predictions = pd.Series(data=predictions)
    data.fillna({target: predictions}, inplace=True)

# %%
def afficher_graphique_corrélation(data):
    """afficher graphique corrélation
      Args:
        data (Dataframe): dataset à traiter
    """
    fig = px.imshow(data.corr(), text_auto=True)
    fig.show()

# %%
ensemble_clients_olist.isna().sum()

# %%
ensemble_geolocalisation_olist.isna().sum()

# %%
ensemble_articles_commandes_olist.isna().sum()

# %%
ensemble_paiements_commandes_olist.isna().sum()

# %%
ensemble_avis_commandes_olist.fillna({'titre_commentaire_avis': 'N/A'}, inplace=True)
ensemble_avis_commandes_olist.fillna({'message_commentaire_avis': 'N/A'}, inplace=True)

# %%
ensemble_avis_commandes_olist.isna().sum()

# %%
ensemble_commandes_olist.fillna({'commande_approuvee_a': 'N/A'}, inplace=True)
ensemble_commandes_olist.fillna({'date_livraison_transporteur_commande': 'N/A'}, inplace=True)
ensemble_commandes_olist.fillna({'date_livraison_client_commande': 'N/A'}, inplace=True)

# %%
ensemble_commandes_olist.isna().sum()

# %%
ensemble_produits_olist = ensemble_produits_olist.dropna()

# %%
ensemble_produits_olist.isna().sum()

# %%
ensemble_vendeurs_olist.isna().sum()

# %%
traduction_nom_categorie_produit.isna().sum()


