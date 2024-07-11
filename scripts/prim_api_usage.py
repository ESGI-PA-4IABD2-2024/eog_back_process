import argparse
import json
import os

from api.call_api import get_hourly_route
from api.call_api import get_line_short_name
from api.call_api import get_stop_point_name
from db.mysql_requests import get_max_id_circulation
from db.mysql_requests import insert_route_into_db
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choix des lignes")
    parser.add_argument("-ligne", type=str, help="", required=True)
    args = parser.parse_args()

    prim_token = os.environ.get("PRIM_TOKEN")
    data_metro = get_metro_route(metro=args.ligne, token=prim_token)
    next_stops = etl_metro_route(dataset=data_metro)
    circulation_train_name = get_line_short_name(args.ligne)
    start_id_circulation = get_max_id_circulation() + 1
    result = insert_route_into_db(next_stops, circulation_train_name, start_id_circulation)
    if result:
        print("Data inserted into db")
