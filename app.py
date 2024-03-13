import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_preprocessing import df_sorted_customers

"""
Visualisation des données sur Dash/Plotly
"""

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Supposons que vous ayez une colonne 'valeur_fret' dans votre dataframe 'df_sorted_customers'

# Mise en forme de l'application Dash
app.layout = html.Div([
    html.H1("Visualisation graphique sur le profil des clients"),
    
    # Case à cocher pour filtrer les années
    html.Div([
        html.H3("Filtrer par année:"),
        dcc.Checklist(
            id='year-filter',
            options=[
                {'label': '2016', 'value': 2016},
                {'label': '2017', 'value': 2017},
                {'label': '2018', 'value': 2018}
            ],
            value=[2016, 2017, 2018],  # Sélectionner toutes les années par défaut
            labelStyle={'display': 'inline-block'}
        ),
    ]),
    

    # Case à cocher pour filtrer par mois
    html.Div([
        html.H3("Filtrer par mois:"),
        dcc.Checklist(
            id='month-filter',
            options=[
                {'label': 'Janvier', 'value': 'Janvier'},
                {'label': 'Février', 'value': 'Février'},
                {'label': 'Mars', 'value': 'Mars'},
                {'label': 'Avril', 'value': 'Avril'},
                {'label': 'Mai', 'value': 'Mai'},
                {'label': 'Juin', 'value': 'Juin'},
                {'label': 'Juillet', 'value': 'Juillet'},
                {'label': 'Août', 'value': 'Août'},
                {'label': 'Septembre', 'value': 'Septembre'},
                {'label': 'Octobre', 'value': 'Octobre'},
                {'label': 'Novembre', 'value': 'Novembre'},
                {'label': 'Décembre', 'value': 'Décembre'},
                # Ajoutez les autres mois ici
            ],
            value=[],  # Sélectionner aucun mois par défaut
            labelStyle={'display': 'inline-block'}
        ),
    ]),
    
    dcc.Graph(id='segmentation-graph'),
    dcc.Graph(id='second-graph')
])

# Callback pour mettre à jour le graphique en fonction des années, mois et jours sélectionnés
@app.callback(
    Output('segmentation-graph', 'figure'),
    [Input('year-filter', 'value'),
     Input('month-filter', 'value')
    ]
)
def update_graph(selected_years, selected_months):
    # Filtrer le DataFrame en fonction des années sélectionnées
    filtered_df = df_sorted_customers[df_sorted_customers['annee_livraison_client'].isin(selected_years)]

    # Filtrer le DataFrame en fonction des mois sélectionnés
    if selected_months:
        filtered_df = filtered_df[filtered_df['mois_livraison_client'].isin(selected_months)]

        
    # Compter le nombre de clients dans chaque catégorie de frais
    repartition_frais = filtered_df['categorie_frais'].value_counts()

    # Calculer les pourcentages des frais
    pourcentage_bas = (repartition_frais['bas'] / len(filtered_df)) * 100
    pourcentage_milieu = (repartition_frais['milieu'] / len(filtered_df)) * 100
    pourcentage_eleves = (repartition_frais['élevés'] / len(filtered_df)) * 100

    # Créer une nouvelle visualisation pour afficher les pourcentages
    fig_pourcentage = px.pie(filtered_df,
                             names=['bas', 'milieu', 'élevés'],
                             values=[pourcentage_bas, pourcentage_milieu, pourcentage_eleves], 
                             title="Répartition des niveaux de frais de livraison sur Olist",
                             labels={'value': 'Pourcentage', 'names': 'Catégorie de frais'},
                             color_discrete_map={'bas': 'darkblue', 'milieu': 'darkred', 'élevés': 'darkgreen'}
                             )
    
    fig_pourcentage.update_layout(
        width=500, height=400  # Taille de la figure
    )
    
    return fig_pourcentage


# Callback pour mettre à jour le deuxième graphique
@app.callback(
    Output('second-graph', 'figure'),
    [Input('year-filter', 'value'),
     Input('month-filter', 'value')
    ]  # Entrée factice
)
def update_second_graph(selected_years, selected_months):

    # Filtrer le DataFrame en fonction des années sélectionnées
    filtered_df = df_sorted_customers[df_sorted_customers['annee_livraison_client'].isin(selected_years)]

    # Filtrer le DataFrame en fonction des mois sélectionnés
    if selected_months:
        filtered_df = filtered_df[filtered_df['mois_livraison_client'].isin(selected_months)]

    # Création de la visualisation avec un diagramme à barres empilées
    fig = px.histogram(filtered_df, x='categorie_frais', 
                       color='categorie_frais',
                       color_discrete_map={'bas': 'darkblue', 'milieu': 'darkred', 'élevés': 'darkgreen'},
                       labels={'categorie_frais': 'Catégorie de frais', 'count': 'Nombre de clients'},
                       title="Segmentation des clients par frais de livraison",
                       )  # Empilement des barres

    fig.update_layout(
        xaxis=dict(title='Identifiant du client',showline=True, showticklabels=False, showgrid=False,title_standoff=80),
        yaxis=dict(title="Montant total des frais de livraison en Reais (RIs)"),
        width=800, height=600,  # Taille de la figure
    )

    return fig

# Exécution de l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)