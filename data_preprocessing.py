import pandas as pd 
import calendar
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

"""
Importation des données
"""

dossier = "data"

df_items = pd.read_csv(f"{dossier}/olist_order_items_dataset.csv")
df_orders = pd.read_csv(f"{dossier}/olist_orders_dataset.csv")

# Renommer les colonnes
df_items = df_items.rename(columns={
    'order_id': 'identifiant_commande',
    'order_item_id': 'identifiant_article_commande',
    'product_id': 'identifiant_produit',
    'seller_id': 'identifiant_vendeur',
    'shipping_limit_date': 'date_limite_expedition',
    'price': 'prix',
    'freight_value': 'valeur_fret'
})

df_orders = df_orders.rename(columns={
    'order_id': 'identifiant_commande',
    'customer_id': 'identifiant_client',
    'order_status': 'statut_commande',
    'order_purchase_timestamp': 'timestamp_achat_commande',
    'order_approved_at': 'commande_approuvee_a',
    'order_delivered_carrier_date': 'date_livraison_transporteur_commande',
    'order_delivered_customer_date': 'date_livraison_client_commande',
    'order_estimated_delivery_date': 'date_livraison_estimee_commande'
})


"""
Nettoyage des données
"""

# Suppression des doublons dans order_items
df_items = df_items.drop_duplicates()

# Suppression des doublons dans orders
df_orders = df_orders.drop_duplicates()

df_delivered_orders = df_orders.loc[df_orders["statut_commande"] == "delivered"]

# Jointure INNER JOIN à partir de la table order_id
merged_data = pd.merge(df_items, df_delivered_orders, on='identifiant_commande')

#Conversion des dates en datetime
merged_data['date_livraison_client_commande'] = pd.to_datetime(merged_data['date_livraison_client_commande'])

# Séparer les données sur les années, mois et jours
merged_data['annee_livraison_client'] = merged_data['date_livraison_client_commande'].dt.year.fillna(0).astype(int)
merged_data['mois_livraison_client'] = merged_data['date_livraison_client_commande'].dt.month.fillna(0).astype(int)
merged_data['jour_livraison_client'] = merged_data['date_livraison_client_commande'].dt.day.fillna(0).astype(int)

#Convertir les numéros de mois en nom de mois
calendar.month_name = [
    "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

# Fonction pour convertir le numéro de mois en nom de mois
def num_to_month(num):
    return calendar.month_name[num]

# Appliquer la fonction à la colonne 'mois' du DataFrame
merged_data['mois_livraison_client'] = merged_data['mois_livraison_client'].apply(num_to_month)


""""
Calcul sur le montant total des frais de livraison et normaliser sur les frais de livraison 
"""

# Calcul du montant total des frais de transport pour chaque client
total_freight_per_customer = merged_data.groupby('identifiant_client')['valeur_fret'].sum()

# Créer un DataFrame pour les identifiants des clients et les frais de livraison
df_sorted_customers = pd.DataFrame({'identifiant_client': total_freight_per_customer.index,
                                    'valeur_fret': total_freight_per_customer.values})

# Trier les clients par montant total des frais de livraison
df_sorted_customers = df_sorted_customers.sort_values(by='valeur_fret', ascending=False)


#Normalisation des données
scaler = StandardScaler()
X = scaler.fit_transform(df_sorted_customers[['valeur_fret']]) 

# Clustering des clients en 20 segments
kmeans = KMeans(n_clusters=3, random_state=42)
df_sorted_customers['segment'] = kmeans.fit_predict(X)


# On définit les plages de valeurs de frais entre 100 à 250  
seuils = [100,150,200,250] 

# Définition des catégories de frais en fonction des plages
categories = ['bas', 'milieu', 'élevés']

# Assigner une catégorie à chaque ligne en fonction de la valeur de 'valeur_fret'
df_sorted_customers['categorie_frais'] = pd.cut(df_sorted_customers['valeur_fret'], bins=seuils, labels=categories, right=False)

#On doit nettoyer les données sur Categorie_frais pour retirer tout les données manquantes qui ne trouve pas dans le sueil 
df_sorted_customers= df_sorted_customers.dropna()

#Jointure entre le dataframe df_sorted_customers et merged_data à partir de l'identifiant du client 
df_sorted_customers = pd.merge(df_sorted_customers, merged_data[['identifiant_client', 'annee_livraison_client','mois_livraison_client','jour_livraison_client']], 
                               on='identifiant_client')