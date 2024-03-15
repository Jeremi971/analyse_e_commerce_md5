
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split


def supprimer_les_doublons(liste_datas):
    """supprimer_les_doublons

    Args:
        liste_datas (liste): listes des Dataframes
    """
    for i, data in enumerate(liste_datas):
        liste_datas[i] = data.drop_duplicates(inplace=True)


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

def remplacer_les_valeurs_extrèmes_par_des_NaN(data,target):
    """Remplacer les valeurs extrèmes par des NaN
    Args:
        data (Dataframe): dataset à traiter
        target (str): colonne à traiter
    """
    indice_dispertion_positive,indice_dispertion_négative = calculer_les_indices_de_dispertions(data,target)
    condition = (data[target] > indice_dispertion_positive) | (data[target] < indice_dispertion_négative)
    data.loc[condition, target] = np.nan

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
    
def afficher_graphique_corrélation(data):
    """afficher graphique corrélation
      Args:
        data (Dataframe): dataset à traiter
    """
    fig = px.imshow(data.corr(), text_auto=True)
    fig.show()