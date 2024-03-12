import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

dossier = "datasets"
df_orders = pd.read_csv(f"{dossier}/olist_orders_dataset.csv")
df_items = pd.read_csv(f"{dossier}/olist_order_items_dataset.csv")


df_items = df_items.rename(columns={
    'order_id': 'id_commande',
    'order_item_id': 'id_article_commande',
    'product_id': 'id_produit',
    'seller_id': 'id_vendeur',
    'shipping_limit_date': 'date_limite_expedition',
    'price': 'prix',
    'freight_value': 'frais_livraison'
})

# Renommer les colonnes
df_orders = df_orders.rename(columns={
    'order_id': 'id_commande',
    'customer_id': 'identifiant_client',
    'order_status': 'statut_commande',
    'order_purchase_timestamp': 'timestamp_achat',
    'order_approved_at': 'timestamp_validation',
    'order_delivered_carrier_date': 'date_livraison_transporteur',
    'order_delivered_customer_date': 'date_livraison_client',
    'order_estimated_delivery_date': 'date_livraison_estimee'
})

# Suppression des doublons dans order_items
df_items = df_items.drop_duplicates()

# Suppression des doublons dans orders
df_orders = df_orders.drop_duplicates()

# Filtrer les livraisons qui ont étaient déjà livrés
df_delivered_orders = df_orders.loc[df_orders["statut_commande"] == "delivered"]

# Jointure INNER JOIN à partir de la table order_id
merged_data = pd.merge(df_items, df_delivered_orders, on='id_commande')

# Calcul du montant total des frais de transport pour chaque client
total_freight_per_customer = merged_data.groupby('identifiant_client')['frais_livraison'].sum()

# Créer un DataFrame pour les identifiants des clients et les frais de livraison
df_sorted_customers = pd.DataFrame({'identifiant_client': total_freight_per_customer.index,
                                    'frais_livraison': total_freight_per_customer.values})

# Trier les clients par montant total des frais de livraison
df_sorted_customers = df_sorted_customers.sort_values(by='frais_livraison', ascending=False)

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Créer une figure Plotly Express
fig = px.bar(df_sorted_customers.head(10), x=df_sorted_customers['identifiant_client'], y=df_sorted_customers['frais_livraison'], labels={'identifiant_client': 'Identifiant du client', 'frais_livraison': 'Montant total des frais de livraison'})

# Mise en forme de l'application Dash
app.layout = html.Div([
    html.H1("Clients payant le plus de frais de livraison"),
    dcc.Graph(id='freight-graph', figure=fig)
])

# Exécuter l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)