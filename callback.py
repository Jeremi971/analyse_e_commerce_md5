from dash.dependencies import Input, Output
from data_preprocessing import df_sorted_customers, ca_total
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



# Définir une fonction pour filtrer le DataFrame en fonction des années et des mois sélectionnés
def filter_dataframe(df_sorted_customers , selected_years, selected_months):
    filtered_df = df_sorted_customers[df_sorted_customers ['annee_livraison_client'].isin(selected_years)]
    if selected_months:
        filtered_df = filtered_df[filtered_df['mois_livraison_client'].isin(selected_months)]
    return filtered_df

def register_callbacks(app):
    @app.callback(
        Output('segmentation-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value')
        ]
    )
    def update_graph(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)
        # Compter le nombre de clients dans chaque catégorie de frais
        repartition_frais = filtered_df['categorie_frais'].value_counts()

        # Calculer les pourcentages des frais
        pourcentage_bas = (repartition_frais['bas'] / len(filtered_df)) * 100
        pourcentage_milieu = (repartition_frais['milieu'] / len(filtered_df)) * 100
        pourcentage_eleves = (repartition_frais['élevés'] / len(filtered_df)) * 100

        # Créer une nouvelle visualisation pour afficher les pourcentages
        fig_pourcentage = px.pie(names=['Bas', 'Milieu', 'Élevés'], 
                                values=[pourcentage_bas, pourcentage_milieu, pourcentage_eleves], 
                                title="Réparation pour les clients ayant réglé les divers frais de livraison sur Olist",
                                labels={'value': 'Pourcentage', 'names': 'Catégorie de frais'})
        
        fig_pourcentage.update_layout(
            width=500, height=400  # Taille de la figure
        )
        
        return fig_pourcentage

    @app.callback(
        Output('second-graph', 'figure'),
        [Input('year-filter', 'value'),
         Input('month-filter', 'value')
        ]
    )
    # Callback pour mettre à jour le deuxième graphique
    def update_second_graph(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)

        # Création de la visualisation avec une taille de figure plus grande
        fig = px.scatter(filtered_df,x='identifiant_client', y='valeur_fret', color='categorie_frais', color_discrete_map={'bas': 'darkgreen', 'milieu': 'darkblue', 'élevés': 'darkred'},
                        title="Segmentation des clients par frais de livraison")
        
        fig.update_layout(
            xaxis=dict(title='Identifiant du client',showline=True, showticklabels=False, showgrid=False,title_standoff=80),
            yaxis=dict(title="Montant total des frais de livraison en Reais (RIs)"),
            width=800, height=600,  # Taille de la figure
        )

        return fig

    @app.callback(
        Output('CA-graph', 'figure'),
        [Input('year-filter', 'value'),
        Input('month-filter', 'value')
        ],
        )
    def update_third_graph(selected_years, selected_months):
        filtered_df = filter_dataframe(df_sorted_customers, selected_years, selected_months)
        # Créer un graphique à l'aide de Plotly
        fig = make_subplots(rows=1, cols=1)

        # Ajouter les jauges pour chaque statistique
        fig.add_trace(go.Indicator(
            mode="number",
            value=ca_total,  # Vous devez calculer ca_total en fonction des données filtrées
            title={"text": "Total Chiffre d'affaires"},
        ))

        # Mettre en forme le layout du graphique
        fig.update_layout(height=400, width=800)

        # Afficher le graphique
        return fig
