from datetime import datetime
from datetime import timedelta

from db.database_connection import get_db_connection


def insert_route_into_db(dataset, line_short_name, start_id):
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
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
        for i, (timestamp, departure_station, arrival_station) in enumerate(dataset):
            departure_hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(
                hours=2
            )
            arrival_hour = departure_hour
            # On suppose que l'heure d'arrivée est la même que l'heure de départ
            routes_values.append((1, 1, departure_hour, arrival_hour, start_id + i))
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


def select_max_id_circulation():
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


def delete_old_data():
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query_delete_routes = (
            "DELETE FROM routes "
            "WHERE id_circulation in ("
            "    SELECT id_circulation "
            "    FROM ("
            "        SELECT id_circulation "
            "        FROM circulation "
            "        WHERE insertion_date = DATE_SUB(CURDATE(), INTERVAL 7 DAY"
            "        ) as subquery"
            "    );"
        )
        query_delete_circulation = (
            "DELETE FROM circulation "
            "WHERE insertion_date = DATE_SUB(CURDATE(), INTERVAL 7 DAY);"
        )
        cursor.executemany(query_delete_routes)
        cursor.executemany(query_delete_circulation)
        connection.close()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection:
            connection.close()
