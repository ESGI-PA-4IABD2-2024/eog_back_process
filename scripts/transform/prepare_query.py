import pandas as pd

from scripts.item.objets import Circulation
from scripts.str.formatage import date_rer_to_date_sql


def prepare_insert_query(circulation: Circulation,
                         df_platforms_station: pd.DataFrame,
                         stations_waiting_to_be_inserted: dict,
                         plateform_waiting_to_be_inserted: dict,
                         next_sql_id_circulation: int,
                         next_sql_id_for_station: int,
                         next_sql_id_for_platform: int):
        current_station = circulation.trajet.head
        true_id_circulation = circulation.id_circulation
        query_station = ""
        query_platform = ""
        query_route = ""

        while True:
            departure = current_station
            arrival = current_station.next_gare
            if arrival is None:
                break   # Fin du trajet, on peut renvoyer les listes

            departure_station_name = departure.name_gare
            arrival_station_name = arrival.name_gare

            ligne = departure.ligne     # Pas besoin de faire depuis arrival vu que c'est forcément sur la même ligne
            # circulation_true_id = departure.id_circulation

            platforms_of_departure_station = df_platforms_station.loc[(df_platforms_station["NAME_STATION"] == departure_station_name)]
            platforms_of_arrival_station = df_platforms_station.loc[(df_platforms_station["NAME_STATION"] == arrival_station_name)]


            # Vérification de la présence des gares en bdd
            if platforms_of_departure_station.empty:    # N'est pas dans bdd
                if departure_station_name not in stations_waiting_to_be_inserted:   # N'a pas encore été vu dans une circulation
                    stations_waiting_to_be_inserted[departure_station_name] = next_sql_id_for_station
                    sql_id_departure_station = next_sql_id_circulation
                    query_station += f"({sql_id_departure_station}, {departure_station_name}),"
                    next_sql_id_for_station += 1
                else:   # A déjà été vu dans une circulation
                    sql_id_departure_station = stations_waiting_to_be_inserted[departure_station_name]
            else:   # Est déjà en bdd
                sql_id_departure_station = platforms_of_departure_station.iloc[0]["ID_GARE"]

            if platforms_of_arrival_station.empty:
                if arrival_station_name not in stations_waiting_to_be_inserted:
                    stations_waiting_to_be_inserted[arrival_station_name] = next_sql_id_for_station
                    sql_id_arrival_station = next_sql_id_circulation
                    query_station += f"({sql_id_arrival_station}, {arrival_station_name}),"
                    next_sql_id_for_station += 1
                else:
                    sql_id_arrival_station = stations_waiting_to_be_inserted[arrival_station_name]
            else:
                sql_id_arrival_station = platforms_of_arrival_station.iloc[0]["ID_GARE"]


            # Vérification de la présence des quais en bdd
            platform_of_departure = platforms_of_departure_station.loc[(platforms_of_departure_station["LIGNE_PLATFORM"] == ligne)]
            platform_of_arrival = platforms_of_departure_station.loc[(platforms_of_departure_station["LIGNE_PLATFORM"] == ligne)]

            if platform_of_departure.empty:
                key = departure_station_name + "$$" + ligne    # Génération d'une clé unique
                if key not in plateform_waiting_to_be_inserted:
                    plateform_waiting_to_be_inserted[key] = next_sql_id_for_platform
                    sql_id_departure_platform = next_sql_id_for_platform
                    query_platform += f"({sql_id_departure_platform}, {sql_id_departure_station}, {ligne}, {circulation.circulation_type}),"
                    next_sql_id_for_platform += 1
                else:
                    sql_id_departure_platform = plateform_waiting_to_be_inserted[key]
            else:
                sql_id_departure_platform = platform_of_departure.iloc[0]["ID_PLATFORM"]

            if platform_of_arrival.empty:
                key = arrival_station_name + "$$" + ligne    # Génération d'une clé unique
                if key not in plateform_waiting_to_be_inserted:
                    plateform_waiting_to_be_inserted[key] = next_sql_id_for_platform
                    sql_id_arrival_platform = next_sql_id_for_platform
                    query_platform += f"({sql_id_arrival_platform}, {sql_id_arrival_station}, {ligne}, {circulation.circulation_type}),"
                    next_sql_id_for_platform += 1
                else:
                    sql_id_arrival_platform = plateform_waiting_to_be_inserted[key]
            else:
                sql_id_arrival_platform = platform_of_arrival.iloc[0]["ID_PLATFORM"]


            departure_hour = date_rer_to_date_sql(departure.h_stop)
            arrival_hour = date_rer_to_date_sql(arrival.h_stop)
            query_route += f"({sql_id_departure_platform}, {sql_id_arrival_platform}, {departure_hour}, {arrival_hour}, {next_sql_id_circulation}),"

            current_station = arrival   # loop incrementation

        query_circulation = f"({next_sql_id_circulation}, {circulation.name_train}, {true_id_circulation}),"

        return query_station, query_platform, query_route, query_circulation, next_sql_id_for_station, next_sql_id_for_platform
