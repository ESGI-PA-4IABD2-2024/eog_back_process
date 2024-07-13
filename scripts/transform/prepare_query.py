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
    stations_values = []
    platforms_values = []
    routes_values = []

    while True:
        departure = current_station
        arrival = current_station.next_gare
        if arrival is None:
            break  # Fin du trajet, on peut renvoyer les listes

        departure_station_name = departure.name_gare
        arrival_station_name = arrival.name_gare

        ligne = departure.ligne

        platforms_of_departure_station = df_platforms_station[
            df_platforms_station["NAME_STATION"] == departure_station_name]
        platforms_of_arrival_station = df_platforms_station[
            df_platforms_station["NAME_STATION"] == arrival_station_name]

        # Vérification de la présence des gares en bdd
        if platforms_of_departure_station.empty:
            if departure_station_name not in stations_waiting_to_be_inserted:
                stations_waiting_to_be_inserted[departure_station_name] = next_sql_id_for_station
                sql_id_departure_station = next_sql_id_for_station
                stations_values.append((int(sql_id_departure_station), departure_station_name))  # Conversion en int
                next_sql_id_for_station += 1
            else:
                sql_id_departure_station = stations_waiting_to_be_inserted[departure_station_name]
        else:
            sql_id_departure_station = int(platforms_of_departure_station.iloc[0]["ID_GARE"])  # Conversion en int

        if platforms_of_arrival_station.empty:
            if arrival_station_name not in stations_waiting_to_be_inserted:
                stations_waiting_to_be_inserted[arrival_station_name] = next_sql_id_for_station
                sql_id_arrival_station = next_sql_id_for_station
                stations_values.append((int(sql_id_arrival_station), arrival_station_name))  # Conversion en int
                next_sql_id_for_station += 1
            else:
                sql_id_arrival_station = stations_waiting_to_be_inserted[arrival_station_name]
        else:
            sql_id_arrival_station = int(platforms_of_arrival_station.iloc[0]["ID_GARE"])  # Conversion en int

        # Vérification de la présence des quais en bdd
        platform_of_departure = platforms_of_departure_station[
            platforms_of_departure_station["LIGNE_PLATFORM"] == ligne]
        platform_of_arrival = platforms_of_arrival_station[platforms_of_arrival_station["LIGNE_PLATFORM"] == ligne]

        if platform_of_departure.empty:
            key = f"{departure_station_name}$$${ligne}"
            if key not in plateform_waiting_to_be_inserted:
                plateform_waiting_to_be_inserted[key] = next_sql_id_for_platform
                sql_id_departure_platform = next_sql_id_for_platform
                platforms_values.append((int(sql_id_departure_platform), int(sql_id_departure_station), ligne,
                                         circulation.circulation_type))  # Conversion en int
                next_sql_id_for_platform += 1
            else:
                sql_id_departure_platform = plateform_waiting_to_be_inserted[key]
        else:
            sql_id_departure_platform = int(platform_of_departure.iloc[0]["ID_PLATFORM"])  # Conversion en int

        if platform_of_arrival.empty:
            key = f"{arrival_station_name}$$${ligne}"
            if key not in plateform_waiting_to_be_inserted:
                plateform_waiting_to_be_inserted[key] = next_sql_id_for_platform
                sql_id_arrival_platform = next_sql_id_for_platform
                platforms_values.append((int(sql_id_arrival_platform), int(sql_id_arrival_station), ligne,
                                         circulation.circulation_type))  # Conversion en int
                next_sql_id_for_platform += 1
            else:
                sql_id_arrival_platform = plateform_waiting_to_be_inserted[key]
        else:
            sql_id_arrival_platform = int(platform_of_arrival.iloc[0]["ID_PLATFORM"])  # Conversion en int

        departure_hour = date_rer_to_date_sql(departure.h_stop)
        arrival_hour = date_rer_to_date_sql(arrival.h_stop)
        routes_values.append((
                             int(sql_id_departure_platform), int(sql_id_arrival_platform), departure_hour, arrival_hour,
                             next_sql_id_circulation))  # Conversion en int

        current_station = arrival  # loop incrementation

    circulation_values = [(next_sql_id_circulation, circulation.name_train, true_id_circulation)]

    return stations_values, platforms_values, routes_values, circulation_values, next_sql_id_for_station, next_sql_id_for_platform
