
import pandas as pd
import numpy as np

dossier = "data"


customers = pd.read_csv(f"{dossier}/olist_customers_dataset.csv")
geolocation = pd.read_csv(f"{dossier}/olist_geolocation_dataset.csv")
#analyse_comments = pd.read_csv(f"{dossier}/translated_comments.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 30)

traduction_colonnes = {
    'customer_id': 'identifiant_client',
    'customer_unique_id': 'identifiant_unique_client',
    'customer_zip_code_prefix': 'code_postal_client',
    'customer_city': 'ville_client',
    'customer_state': 'etat_client',
    'geolocation_zip_code_prefix': 'code_postal_geolocalisation',
    'geolocation_lat': 'latitude_geolocalisation',
    'geolocation_lng': 'longitude_geolocalisation',
    'geolocation_city': 'ville_geolocalisation',
    'geolocation_state': 'etat_geolocalisation',
    'order_id': 'identifiant_commande',
    'order_status': 'statut_commande',
    'order_purchase_timestamp': 'horodatage_achat_commande',
    'order_approved_at': 'date_approbation_commande',
    'order_delivered_carrier_date': 'date_livraison_transporteur_commande',
    'order_delivered_customer_date': 'date_livraison_client_commande',
    'order_estimated_delivery_date': 'date_livraison_estimee_commande',
    'order_item_id': 'identifiant_element_commande',
    'product_id': 'identifiant_produit',
    'seller_id': 'identifiant_vendeur',
    'shipping_limit_date': 'date_limite_expedition',
    'price': 'prix',
    'freight_value': 'frais_port',
    'payment_sequential': 'sequence_paiement',
    'payment_type': 'type_paiement',
    'payment_installments': 'versements_paiement',
    'payment_value': 'valeur_paiement',
    'review_id': 'identifiant_evaluation',
    'review_score': 'score_evaluation',
    'review_comment_title': 'titre_commentaire_evaluation',
    'review_comment_message': 'message_commentaire_evaluation',
    'review_creation_date': 'date_creation_evaluation',
    'review_answer_timestamp': 'horodatage_reponse_evaluation',
    'product_category_name': 'nom_categorie_produit',
    'product_name_lenght': 'longueur_nom_produit',
    'product_description_lenght': 'longueur_description_produit',
    'product_photos_qty': 'quantite_photos_produit',
    'product_weight_g': 'poids_produit_g',
    'product_length_cm': 'longueur_produit_cm',
    'product_height_cm': 'hauteur_produit_cm',
    'product_width_cm': 'largeur_produit_cm',
    'seller_zip_code_prefix': 'code_postal_vendeur',
    'seller_city': 'ville_vendeur',
    'seller_state': 'etat_vendeur',
    'product_category_name_english': 'nom_categorie_produit_anglais'
}

customer_geolocation = pd.merge(customers, geolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
customer_geolocation = customer_geolocation.loc[:, ~customer_geolocation.columns.duplicated()]
customer_geolocation = customer_geolocation.rename(columns=traduction_colonnes)
del customers
del geolocation

customer_geolocation.replace({np.nan: None}, inplace=True)
customer_geolocation['code_postal_geolocalisation'] = customer_geolocation['code_postal_geolocalisation'].astype('Int64')


## Compter le nombre de clients pour chaque ville
city_counts = customer_geolocation['ville_client'].value_counts()

# Trier les villes par ordre décroissant du nombre de clients
city_counts = city_counts.sort_values(ascending=False)

# Extraire les noms des villes et les nombres de clients
cities = city_counts.index
num_clients = city_counts.values




