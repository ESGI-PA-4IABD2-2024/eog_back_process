import argparse
import json
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.call_api import get_today_route
from dotenv import load_dotenv
from db.mysql_requests import get_max_id_circulation, get_existing_stations_and_platforms, insert_new_stations, \
    insert_new_platforms, insert_new_circulations, insert_new_routes
from transform.etl import etl_rer
from transform.prepare_query import prepare_insert_query

load_dotenv()
pd.set_option("display.max_columns", None)  # Afficher toutes les colonnes d'un dataframe


def fetch_and_insert(ligne: str, DEBUG: bool = False):
    navitia_token = os.environ.get("NAVITIA_TOKEN")
    rer_url = "https://api.navitia.io/v1/"

    # Récupération des données de circulation
    if not DEBUG:
        api_result = get_today_route(ligne=ligne, url=rer_url, user=navitia_token)
    else:
        f = open("test_dataset/rer_a.txt", "r", encoding="utf-8")
        api_result = f.read()
        f.close()
    # print(api_result) # DEBUG
    data = json.loads(api_result)

    # Mise en forme
    dic_circulations, gares = etl_rer(data)

    # Initialisations des variables servant à préparer l'insertion en base
    next_sql_id_circulation = get_max_id_circulation()
    df_platforms_station = get_existing_stations_and_platforms()

    stations_waiting_to_be_inserted = {}  # key = station, value = sql_id
    plateform_waiting_to_be_inserted = {}  # key = station, value = sql_id
    next_sql_id_for_station = (
        0
        if pd.isna(df_platforms_station["ID_GARE"].max())
        else (df_platforms_station["ID_GARE"].max() + 1)
    )
    next_sql_id_for_platform = (
        0
        if pd.isna(df_platforms_station["ID_PLATFORM"].max())
        else (df_platforms_station["ID_PLATFORM"].max() + 1)
    )
    all_station_to_add = []
    all_plateform_to_add = []
    all_route_to_add = []
    all_circulation_to_add = []

    # Check de ce qu'il faut insérer et préparation du format d'insertion
    for circulation in dic_circulations:
        next_sql_id_circulation += 1
        (
            stations_values,
            platforms_values,
            routes_values,
            circulation_values,
            next_sql_id_for_station,
            next_sql_id_for_platform,
        ) = prepare_insert_query(
            dic_circulations[circulation],
            df_platforms_station,
            stations_waiting_to_be_inserted,
            plateform_waiting_to_be_inserted,
            next_sql_id_circulation,
            next_sql_id_for_station,
            next_sql_id_for_platform,
        )

        all_station_to_add.extend(stations_values)
        all_plateform_to_add.extend(platforms_values)
        all_route_to_add.extend(routes_values)
        all_circulation_to_add.extend(circulation_values)

    # Insertion en BDD si des changements sont repérés
    result_stations = True
    result_plateforms = True
    result_circulations = True
    result_routes = True

    if all_station_to_add:
        result_stations = insert_new_stations(all_station_to_add)
    if all_plateform_to_add:
        result_plateforms = insert_new_platforms(all_plateform_to_add)
    if all_circulation_to_add:
        result_circulations = insert_new_circulations(all_circulation_to_add)
    if all_route_to_add:
        result_routes = insert_new_routes(all_route_to_add)

    if result_stations and result_plateforms and result_circulations and result_routes:
        print("Data inserted into db")


"""
    # Afficher les données
    gares.display()
    # print(f"Nombre de circulations récupérées : {len(dic_circulations)}")     # DEBUG
    for circulation in dic_circulations:
        print("\n\n")
        dic_circulations[circulation].trajet.display()

    print("DEBUG")
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choix des lignes")
    parser.add_argument("-ligne", type=str, help="", required=True)
    args = parser.parse_args()

    fetch_and_insert(args.ligne)
