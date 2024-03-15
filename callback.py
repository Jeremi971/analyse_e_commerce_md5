from dash.dependencies import Input, Output
from data_preprocessing import *
from data_preprocessing_2 import *
import plotly.express as px
import plotly.colors as pc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Définir une fonction pour filtrer le DataFrame en fonction des années et des mois sélectionnés
def filter_dataframe(df, selected_years, selected_months):
    filtered_df = df[df['annee_livraison_client'].isin(selected_years)]
    if selected_months:
        filtered_df = filtered_df[filtered_df['mois_livraison_client'].isin(selected_months)]
    return filtered_df

# Calculer les pourcentages des frais
def calculate_percentages(filtered_df):
    total_clients = len(filtered_df)
    repartition_frais = filtered_df['categorie_frais'].value_counts()
    return {
        'bas': (repartition_frais.get('bas', 0) / total_clients) * 100,
        'milieu': (repartition_frais.get('milieu', 0) / total_clients) * 100,
        'élevés': (repartition_frais.get('élevés', 0) / total_clients) * 100
    }

# Mettre à jour le graphique de répartition des frais
def update_first_graph(filtered_df):
    percentages = calculate_percentages(filtered_df)
    fig = px.pie(names=['Bas', 'Milieu', 'Élevés'], values=list(percentages.values()), 
                 title="Répartition pour les clients ayant réglé les divers frais de livraison sur Olist",
                 labels={'value': 'Pourcentage', 'names': 'Catégorie de frais'})
    fig.update_layout(width=500, height=400)
    return fig

# Mettre à jour le deuxième graphique
def update_second_graph(filtered_df):
    fig = px.scatter(filtered_df, x='identifiant_client', y='valeur_fret', color='categorie_frais', 
                     color_discrete_map={'bas': 'darkgreen', 'milieu': 'darkblue', 'élevés': 'darkred'},
                     title="Segmentation des clients par frais de livraison")
    fig.update_layout(xaxis=dict(title='Identifiant du client', showline=True, showticklabels=False, showgrid=False, title_standoff=80),
                      yaxis=dict(title="Montant total des frais de livraison en Reais (RIs)"),
                      width=800, height=600)
    return fig

# Mettre à jour le troisième graphique
def update_third_graph(filtered_df):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Indicator(
        mode="number",
        value=ca_total,  # Vous devez calculer ca_total en fonction des données filtrées
        title={"text": "Total Chiffre d'affaires"},
    ))
    fig.update_layout(height=400, width=800)
    return fig

def update_fouth_graph(filtered_df):
    # Créer une palette de couleurs unique pour chaque ville
    colors = pc.DEFAULT_PLOTLY_COLORS[:len(cities)]

    trace = go.Bar(
        x=cities,
        y=num_clients,
        marker=dict(color=colors)  # Couleur des barres pour chaque ville
    )

    # Créer la mise en page de la figure
    layout = go.Layout(
        title='Nombre de clients par ville',
        xaxis=dict(title='Villes'),
        yaxis=dict(title='Nombre de clients')
    )

    # Créer la figure
    fig_client_ville_diag = go.Figure(data=[trace], layout=layout)
    return fig_client_ville_diag



# Enregistrement des callbacks
def register_callbacks(app):
    @app.callback(
        Output('segmentation-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value')]
    )
    def update_first(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)
        return update_first_graph(filtered_df)

    @app.callback(
        Output('second-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value')]
    )
    def update_second(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)
        return update_second_graph(filtered_df)

    @app.callback(
        Output('CA-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value')]
    )
    def update_third(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)
        return update_third_graph(filtered_df)
    
    @app.callback(
        Output('villes-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value')]
    )
    def update_fourth(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)
        return update_fouth_graph(filtered_df)