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
    estimated_calls = \
        dataset['Siri']['ServiceDelivery']['EstimatedTimetableDelivery'][0]['EstimatedJourneyVersionFrame'][0][
            'EstimatedVehicleJourney'][0]['EstimatedCalls']['EstimatedCall']
    next_stops = []
    for call in estimated_calls:
        timestamp = call['ExpectedDepartureTime']
        stop_point = get_stop_point_name(call['StopPointRef']['value'], token)
        next_stops.append((timestamp, stop_point))
    return next_stops


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
