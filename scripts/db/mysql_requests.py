from datetime import datetime
from datetime import timedelta

from db.database_connection import get_db_connection


def insert_route_into_db(dataset, line_short_name, start_id):
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()

        platform_names = list(set([data[1] for data in dataset] + [data[2] for data in dataset]))
        station_ids = get_station_ids(platform_names)

        circulation_values = [
            (start_id + i, line_short_name, str(data)) for i, data in enumerate(dataset)
        ]
        query = (
            "INSERT INTO circulation (id_circulation, insertion_date, train_name, official_id) "
            "VALUES (%s, NOW(), %s, %s)"
        )
        cursor.executemany(query, circulation_values)
        connection.commit()

        routes_values = []
        for i, (timestamp, departure_platform, arrival_platform, direction) in enumerate(dataset):
            arrival_hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(
                hours=2
            )
            departure_platform_id = station_ids.get(departure_platform)
            arrival_platform_id = station_ids.get(arrival_platform)
            if departure_platform_id is None or arrival_platform_id is None:
                print(f"Error: unknown platform {departure_platform} or {arrival_platform}")
                return False
            routes_values.append(
                (departure_platform_id, arrival_platform_id, arrival_hour, start_id + i)
            )
        query = (
            "INSERT INTO routes (id_departure_platform, id_arrival_platform, "
            "arrival_hour, id_circulation) "
            "VALUES (%s, %s, %s, %s)"
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


def get_max_id_circulation():
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query = "SELECT MAX(id_circulation) as id_circulation FROM circulation"
        cursor.execute(query)
        max_id_circulation = cursor.fetchone()[0]
        cursor.close()
        return max_id_circulation
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_id_gare(platform_name):
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query = f"SELECT id_gare FROM stations WHERE name_station = '{platform_name}'"
        cursor.execute(query)
        id_gare = cursor.fetchone()[0]
        cursor.close()
        return id_gare
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_station_ids(platform_names):
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query = "SELECT name_station, id_gare FROM stations WHERE name_station IN ({})".format(
            ",".join(["%s"] * len(platform_names))
        )
        cursor.execute(query, platform_names)
        station_ids = {row[0]: row[1] for row in cursor.fetchall()}
        return station_ids
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()


def delete_old_data():
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query_delete_circulation = (
            "DELETE FROM circulation " "WHERE insertion_date = DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
        )
        cursor.execute(query_delete_circulation)
        connection.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
