import argparse
import json
import os
from datetime import datetime
from datetime import timedelta

import pytz
from api.call_api import get_hourly_route
from api.call_api import get_line_short_name
from api.call_api import get_stop_point_name
from db.database_connection import get_db_connection
from dotenv import load_dotenv

load_dotenv()


def get_metro_route(metro, token):
    api_result = get_hourly_route(ligne=metro, token=token)
    data = json.loads(api_result)
    return data


def etl_metro_route(dataset):
    next_metro_stops = []
    estimated_calls = dataset["Siri"]["ServiceDelivery"]["EstimatedTimetableDelivery"]
    for estimated_timetable_delivery in estimated_calls:
        for estimated_journey_version_frame in estimated_timetable_delivery[
            "EstimatedJourneyVersionFrame"
        ]:
            for estimated_vehicle_journey in estimated_journey_version_frame[
                "EstimatedVehicleJourney"
            ]:
                metro_direction_name = estimated_vehicle_journey["DirectionName"][0]["value"]
                for estimated_call in estimated_vehicle_journey["EstimatedCalls"]["EstimatedCall"]:
                    metro_stop_id = estimated_call["StopPointRef"]["value"]
                    metro_stop_point = get_stop_point_name(metro_stop_id)
                    metro_timestamp = estimated_call["ExpectedDepartureTime"]
                    next_metro_stops.append(
                        (metro_timestamp, metro_stop_point, metro_direction_name)
                    )
    return next_metro_stops


def change_date_format(timestamp):
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_utc = dt.replace(tzinfo=pytz.UTC)
    dt_utc_plus_2 = dt_utc.astimezone(pytz.timezone("Europe/Paris"))
    sql_datetime = dt_utc_plus_2.strftime("%Y-%m-%d %H:%M:%S.%f")
    return sql_datetime


def insert_route_into_db(dataset, line_short_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Insertion des données dans la table circulation
        circulation_values = [
            (i + 1, line_short_name, str(data)) for i, data in enumerate(dataset)
        ]
        query = (
            "INSERT INTO circulation (id_circulation, insertion_date, train_name, official_id) "
            "VALUES (%s, NOW(), %s, %s)"
        )
        cursor.executemany(query, circulation_values)
        connection.commit()

        routes_values = []
        for i, (timestamp, departure_station, arrival_station) in enumerate(dataset):
            departure_hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(
                hours=2
            )
            arrival_hour = departure_hour
            # On suppose que l'heure d'arrivée  est la même que l'heure de départ
            routes_values.append((1, 1, departure_hour, arrival_hour, i + 1))
        query = (
            "INSERT INTO routes (id_departure_platform, id_arrival_platform, "
            "departure_hour, arrival_hour, id_circulation) VALUES (%s, %s, %s, %s, %s)"
        )
        cursor.executemany(query, routes_values)
        connection.commit()

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choix des lignes")
    parser.add_argument("-ligne", type=str, help="", required=True)
    args = parser.parse_args()
    circu_train_name = get_line_short_name(args.ligne)

    prim_token = os.environ.get("PRIM_TOKEN")
    data_metro = get_metro_route(metro=args.ligne, token=prim_token)
    next_stops = etl_metro_route(dataset=data_metro)
    result = insert_route_into_db(next_stops, circu_train_name)
    if result:
        print("Data inserted into db")
