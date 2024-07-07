import os
import json
import argparse
from dotenv import load_dotenv
from api.call_api import get_hourly_route, get_stop_point_name

load_dotenv()


def get_metro_route(metro, token):
    api_result = get_hourly_route(ligne=metro, token=token)
    data = json.loads(api_result)
    return data


def etl_metro_route(dataset, token):
    next_metro_stops = []
    estimated_calls = \
        dataset['Siri']['ServiceDelivery']['EstimatedTimetableDelivery']
    for estimated_timetable_delivery in estimated_calls:
        for estimated_journey_version_frame in estimated_timetable_delivery['EstimatedJourneyVersionFrame']:
            for estimated_vehicle_journey in estimated_journey_version_frame['EstimatedVehicleJourney']:
                for estimated_call in estimated_vehicle_journey['EstimatedCalls']['EstimatedCall']:
                    metro_stop_id = estimated_call['StopPointRef']['value']
                    metro_stop_point = get_stop_point_name(metro_stop_id)
                    metro_timestamp = estimated_call['ExpectedDepartureTime']
                    next_metro_stops.append((metro_timestamp, metro_stop_point))
    return next_metro_stops


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Choix des lignes")
    parser.add_argument(
        "-ligne",
        type=str,
        help="",
        required=True
    )
    args = parser.parse_args()

    prim_token = os.environ.get('PRIM_TOKEN')
    data_metro = get_metro_route(metro=args.ligne, token=prim_token)
    next_stops = etl_metro_route(dataset=data_metro, token=prim_token)
    for timestamp, stop_point in next_stops:
        print(f"Next stop: {stop_point} at {timestamp}")
