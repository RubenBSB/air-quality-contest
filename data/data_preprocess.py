import pandas as pd
import datetime

dfs = []

def transform_date(str_date, date_style):
    if str_date == 'NaN':
        return str_date
    else:
        if date_style == 1:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:00:00.000Z').strftime('%d/%m/%Y %H:00')
        elif date_style == 2:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:00+00:00').strftime('%d/%m/%Y %H:%M')
    return date

df_idf_horaire_pm10 = pd.read_csv("csv/idf_horaire_pm10.csv", delimiter=';')[['nom_station','valeur', 'date_debut']]
df_idf_horaire_pm10 = df_idf_horaire_pm10.pivot_table(index = 'date_debut', columns = 'nom_station', values = 'valeur')
df_idf_horaire_pm10.reset_index(inplace=True)
df_idf_horaire_pm10['date_debut'] = df_idf_horaire_pm10['date_debut'].apply(lambda x : transform_date(x,1))
dfs.append(df_idf_horaire_pm10)

df_aura_horaire_pm10 = pd.read_csv("csv/aura_horaire_pm10.csv", delimiter=';')[['nom_station','valeur', 'date_debut']]
df_aura_horaire_pm10 = df_aura_horaire_pm10.pivot_table(index = 'date_debut', columns = 'nom_station', values = 'valeur')
df_aura_horaire_pm10.reset_index(inplace=True)
df_aura_horaire_pm10['date_debut'] = df_aura_horaire_pm10['date_debut'].apply(lambda x : transform_date(x,1))
dfs.append(df_aura_horaire_pm10)

df_bfc_horaire_pm10 = pd.read_csv("csv/bfc_horaire_pm10.csv", delimiter=';')
df_bfc_horaire_pm10.replace('Non disponible', 'NaN')
df_bfc_horaire_pm10.rename(columns={'Date':'date_debut'}, inplace=True)
dfs.append(df_bfc_horaire_pm10)

df_bretagne_horaire_pm10 = pd.read_csv("csv/bretagne_horaire_pm10.csv", delimiter=';')[['nom_station','valeur','date_debut']]
df_bretagne_horaire_pm10 = df_bretagne_horaire_pm10.pivot_table(index = 'date_debut', columns = 'nom_station', values = 'valeur')
df_bretagne_horaire_pm10.reset_index(inplace=True)
dfs.append(df_bretagne_horaire_pm10)

df_naqu_horaire_pm10 = pd.read_csv("csv/naqu_horaire_pm10.csv", delimiter=';')[['nm_sttn','valeur','dat_dbt']]
df_naqu_horaire_pm10.columns = ['nom_station', 'valeur', 'date_debut']
df_naqu_horaire_pm10 = df_naqu_horaire_pm10.pivot_table(index = 'date_debut', columns = 'nom_station', values = 'valeur')
df_naqu_horaire_pm10.reset_index(inplace=True)
dfs.append(df_naqu_horaire_pm10)

df_pl_horaire_pm10 = pd.read_csv("csv/pl_horaire_pm10.csv", delimiter=';')[['nom_station','valeur','date_debut']]
df_pl_horaire_pm10 = df_pl_horaire_pm10.pivot_table(index = 'date_debut', columns = 'nom_station', values = 'valeur')
df_pl_horaire_pm10.reset_index(inplace=True)
df_pl_horaire_pm10['date_debut'] = df_pl_horaire_pm10['date_debut'].apply(lambda x : transform_date(x,2))
dfs.append(df_pl_horaire_pm10)

df_data = dfs[0]
for df_ in dfs[1:]:
    df_data = df_data.merge(df_, on='date_debut', how='outer')

'''========================= Importing localisations of stations ========================'''

import difflib
import folium
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 10)


df_meta = pd.read_csv("csv/meta.csv", delimiter=';', encoding = 'iso-8859-1')[['Name','Longitude','Latitude']]
df_meta['Name'] = df_meta['Name'].str.lower()

meta_stations = df_meta['Name'].values
meta_stations = [string.lower() for string in meta_stations]

localisations = {}

for station in df_data.columns[1:]:
    try:
        meta_name = difflib.get_close_matches(station.lower(),meta_stations,1)[0]
        localisations[station] = list(df_meta[df_meta['Name'] == meta_name][['Longitude', 'Latitude']].values[0])
    except:
        pass

plt.figure()
for station in localisations:
    x,y = localisations[station][0], localisations[station][1]
    plt.scatter(x,y)
    plt.annotate(station+'\n'+'\n', (x,y)).set_fontsize(7)
plt.show()

map_osm = folium.Map(location=[48.85, 2.34])
for station in localisations:
    x,y = localisations[station][0], localisations[station][1]
    map_osm.add_child(folium.RegularPolygonMarker(location=[y,x], popup=station,
                       fill_color='red', radius=5))
map_osm


