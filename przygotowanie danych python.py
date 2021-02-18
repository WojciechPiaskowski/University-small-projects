import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.impute import KNNImputer

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 50)
sns.set_style('whitegrid')

df = pd.read_csv('CommViolPredUnnormalizedData.txt', header=None, na_values='?')

df.head()
df.info()
df.describe()

# braki danych
braki = df.isnull()
braki_series = braki.sum()

plt.plot(braki_series.index, braki_series)
plt.xlabel('Zmienna')
plt.ylabel('Ilość braków')
plt.show()

plt.figure(figsize=(12,6))
sns.barplot(x=braki_series.sort_values(ascending=False)[braki_series.sort_values(ascending=False)>0].index.astype('str'),
            y=braki_series.sort_values(ascending=False)[braki_series.sort_values(ascending=False)>0],
            order=braki_series.sort_values(ascending=False)[braki_series.sort_values(ascending=False)>0].index.astype('str'),
            palette='rocket')
plt.xlabel('zmienna')
plt.ylabel('ilość braków')
plt.title('braki danych')

# braki warte imputowania (odrzocne zmienne z brakami > 500

plt.figure(figsize=(12,6))
sns.barplot(x=braki_series.sort_values(ascending=False)
[(braki_series.sort_values(ascending=False)>0) & (braki_series.sort_values(ascending=False)<500)].index.astype('str'),
            y=braki_series.sort_values(ascending=False)
            [(braki_series.sort_values(ascending=False)>0) & (braki_series.sort_values(ascending=False)<500)],
            order=braki_series.sort_values(ascending=False)
            [(braki_series.sort_values(ascending=False)>0)
             & (braki_series.sort_values(ascending=False)<500)].index.astype('str'),
            palette='rocket')
plt.xlabel('zmienna')
plt.ylabel('ilość braków')
plt.title('zmienne z brakami <500 obserwacji')

# imputacja zmiennej 146 (a wiec 147, indeks zaczyna sie od 0)
# liczba nie-brutalnych przestępstw na 100k mieszkańców
# rozklad zmiennej
sns.distplot(df.loc[:,146], color='red')
# statystyki opisowe zmiennej przed imputacją
df.loc[:,146].describe()
# korelacje
df.corr().loc[:,146].sort_values(ascending=False)
# zmienna bardzo silnie koreluje ze zmienna 140 (P=0,94) -> liczba kradziezy na 100k mieszkańców

# wartosc brakujace dla zmiennej 146 wraz ze zmiennymi 140 dla danych obserwacji
wartosc_bez_null = df[[140,146]][df[[140,146]].notnull()].dropna()

# zmienna 140 takze posiada braki, chociaz sa to pojedyncze jednostki, unimozliwia to estymowania obserwacji zmiennej 146
# zaimputuje braki w zmiennej 140 metoda najblizszych sasiadow

sns.distplot(df.loc[:,140], color='blue')
imputer = KNNImputer(n_neighbors=2, weights='uniform')
df[140] = imputer.fit_transform(df[140].values.reshape(-1,1))

# regresja (bez elementu stochastycznego)

nulle = df[140][df[146].isnull()]
model = LinearRegression()
model = model.fit(X=wartosc_bez_null[140].values.reshape(-1,1), y=wartosc_bez_null[146].values.reshape(-1,1))
yhat = model.predict(nulle.values.reshape(-1,1))
keys = list(df[146][df[146].isnull()].index)
values = list(yhat.flatten())
d = dict(zip(keys, values))

df[146].fillna(value=d, inplace=True)

# rozklad zmiennej
sns.distplot(df.loc[:,146], color='red')
# statystyki opisowe zmiennej po imputacją
df.loc[:,146].describe()

df