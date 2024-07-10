from airflow.exceptions import AirflowException
from db.mysql_requests import delete_old_data


if __name__ == "__main__":
    result = delete_old_data()
    if result:
        print("Old data removed from db")
    if result is None:
        raise AirflowException()
