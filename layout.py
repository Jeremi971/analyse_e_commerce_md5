from dash import html
from dash import dcc 

layout = html.Div([
    html.H1("Visualisation graphique sur le profil des clients"),
    
    # Case à cocher pour filtrer par mois
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
    dcc.Graph(id='CA-graph'),
    dcc.Graph(id='segmentation-graph'),
    dcc.Graph(id='second-graph'),
    dcc.Graph(id='villes-graph')
])