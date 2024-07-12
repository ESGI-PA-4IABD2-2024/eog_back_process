import json
import os
import pandas as pd

from api.call_api import get_today_route
from dotenv import load_dotenv
from scripts.db.mysql_requests import insert_route_into_db, get_max_id_circulation, get_existing_stations_and_platforms
from scripts.transform.prepare_query import prepare_insert_query
from transform.etl import etl_rer

load_dotenv()
pd.set_option("display.max_columns", None)  # Afficher toutes les colonnes d'un dataframe



if __name__ == "__main__":
    navitia_token = os.environ.get("NAVITIA_TOKEN")

    DEBUG = True

    rer_url = "https://api.navitia.io/v1/"

    rer = "A"
    # Récupération des données de circulation
    if not DEBUG:
        api_result = get_today_route(ligne=rer, url=rer_url, user=navitia_token)
    else:
        f = open("test_dataset/rer_a.txt", "r", encoding="utf-8")
        api_result = f.read()
        f.close()
    # print(api_result) # DEBUGx
    data = json.loads(api_result)

    # Mise en forme
    dic_circulations, gares = etl_rer(data)

    # Données pour l'insertion en base
    next_sql_id_circulation = get_max_id_circulation()
    df_platforms_station = get_existing_stations_and_platforms()


    insert_query = ""
    stations_waiting_to_be_inserted = {}     # key = station, value = sql_id
    plateform_waiting_to_be_inserted = {}   # key = station, value = sql_id
    next_sql_id_for_station = 0 if pd.isna(df_platforms_station['ID_GARE'].max()) else (
            df_platforms_station['ID_GARE'].max() + 1)
    next_sql_id_for_platform = 0 if pd.isna(df_platforms_station['ID_PLATFORM'].max()) else (
            df_platforms_station['ID_PLATFORM'].max() + 1)
    all_station_to_add = ""
    all_plateform_to_add = ""
    all_route_to_add = ""
    all_circulation_to_add = ""

    for circulation in dic_circulations:
        next_sql_id_circulation += 1
        query_station, query_platform, query_route, query_circulation, next_sql_id_for_station, next_sql_id_for_platform = prepare_insert_query(dic_circulations[circulation],
                                                                                                                             df_platforms_station,
                                                                                                                             stations_waiting_to_be_inserted,
                                                                                                                             plateform_waiting_to_be_inserted,
                                                                                                                             next_sql_id_circulation,
                                                                                                                             next_sql_id_for_station,
                                                                                                                             next_sql_id_for_platform)

        all_station_to_add += query_station
        all_plateform_to_add += query_platform
        all_route_to_add += query_route
        all_circulation_to_add += query_circulation







    """
    # TODO : màj sql des gares, puis des platerformes (quai), puis des circulations, et enfin des trajets
    result = insert_route_into_db(next_stops, circu_train_name, next_sql_id_circulation)
    if result:
        print("Data inserted into db")

    
    # Afficher les données
    gares.display()
    # print(f"Nombre de circulations récupérées : {len(dic_circulations)}")     # DEBUG
    for circulation in dic_circulations:
        print("\n\n")
        dic_circulations[circulation].trajet.display()

    print("DEBUG")
"""

