FROM apache/airflow:2.8.1-python3.11
USER airflow
RUN pip install --upgrade pip
RUN pip install --upgrade SQLAlchemy==1.4.52 \
    pandas==2.1.4 \
    mysql-connector-python \
    python-dotenv \
    datetime
