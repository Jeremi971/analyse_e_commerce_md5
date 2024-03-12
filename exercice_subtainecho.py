import pandas as pd
from ucimlrepo import fetch_ucirepo 
from dash import Dash, html , dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# fetch dataset 
iris = fetch_ucirepo(id=53) 
  
# Import dataset X et y en dictionnaire 
iris_features = iris.data.features 
iris_targets = iris.data.targets 

# Convertir le dictionnaire en dataframe
df_X = pd.DataFrame.from_dict(iris_features)
df_y = pd.DataFrame.from_dict(iris_targets)

#Jointure Dataframe
df = df_X.join(df_y)

X = df.drop('class', axis=1)
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Fix Convergence warning specify max_iter in the LogisticRegression to a higher value:

model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

#Accuracy classification score

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test,y_test_pred)

# Créer une application Dash
app = Dash(__name__)

features = ['sepal length','sepal width','petal length','petal width']

# Définir la mise en page de l'application
app.layout = html.Div([
    html.H1(children='Visualisation de données sur Iris', style={'textAlign':'center'}),
    html.H2(children='Structure Dataset',style={'textAlign':'center'}),

    #Structure de données du dataset
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),

    #Data manipulation
    html.H3('Data Manipulation'),
    html.Div([
        html.Label('Select feature'),
        dcc.Dropdown(features,'sepal length',id='dropdown-selection'), #Menu déroulant  
        html.Label('Normalisation'),  
        dcc.Checklist(features,value=[],id='data-normalization'),
        html.Label('Suppression des valeurs aberrantes (seuil):'),
        dcc.Input(id='outlier-threshold', type='number', value=1),
        dcc.Graph(id='graph-content'), #Graphique pour afficher l'histogramme
    ]),
 
    #Machine Learning Integration
    html.H3('Machine Learning Integration'),
    html.Div([
        dcc.Input(id='sepal-length', type='number', placeholder='Sepal Length'),
        dcc.Input(id='sepal-width', type='number', placeholder='Sepal Width'),
        dcc.Input(id='petal-length', type='number', placeholder='Petal Length'),
        dcc.Input(id='petal-width', type='number', placeholder='Petal Width'),
        html.Button('Predict', id='predict-button'),
        html.Div(id='prediction-output')
    ]),

    #Display the average accuracy
    html.H3('Model Accuracy'),
    html.Div([
        html.P(f'Training Accuracy: {train_accuracy:.2f}'),
        html.P(f'Test Accuracy: {test_accuracy:.2f}')
    ]),
   
])

# Callback pour mettre à jour l'histogramme en fonction de la sélection de l'utilisateur
@app.callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('data-normalization', 'value'),
    Input('outlier-threshold', 'value'),
)

def update_histogram(selected_column,normalize_columns,  outlier_threshold):

    #Data Mapping 
    column_mapping = {
        'sepal length': ['sepal length', 'class'],
        'sepal width': ['sepal width', 'class'],
        'petal length': ['petal length', 'class'],
        'petal width': ['petal width', 'class']
    }

    if selected_column in column_mapping:
        columns_to_select = column_mapping[selected_column]
        df_selected = df[columns_to_select]

        #Normalisation des données sélectionnées
        if selected_column in normalize_columns:
            #Formule de la normalisation (Permet de mettre à l'échelle les valeurs entre 0 à 1)
            df_selected[selected_column] = (abs(df_selected[selected_column] - df_selected[selected_column].min())) / abs(df_selected[selected_column].max()- df_selected[selected_column].min())

        if selected_column:
            #Formule de la standardisation
            z_scores = (df_selected[selected_column] - df_selected[selected_column].mean()) / df_selected[selected_column].std()
            df_selected = df_selected[abs(z_scores) <= outlier_threshold]

        fig = px.histogram(df_selected, x=selected_column, color='class', title=f'Histogramme de {selected_column}')


    # Ajouter une fonctionnalité de survol pour afficher les valeurs exactes des données
    fig.update_traces(hovertemplate='X: %{x},Y: %{y}') 
    return fig


#Callback pour prédire le nom de l'espèce 
@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks'),
    Input('sepal-length', 'value'),
    Input('sepal-width', 'value'),
    Input('petal-length', 'value'),
    Input('petal-width', 'value')
)
def predict_class(n_clicks, sepal_length, sepal_width, petal_length, petal_width):
    if n_clicks:
        try:
            input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
            predicted_class= model.predict(input_data)[0]
            return f'Predicted specifie: {predicted_class}'
        except:
            return 'Prediction Error'
    return ''

# Lancer l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
