import logging
import os
import requests
import pymssql
from datetime import datetime
import azure.functions as func


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="DelayMonitorFunction")
def DelayMonitorFunction(req: func.HttpRequest) -> func.HttpResponse:
    try:
        server = os.environ["SQL_SERVER"]
        database = os.environ["SQL_DB"]
        user = os.environ["SQL_USER"]
        password = os.environ["SQL_PASSWORD"]

        # Connect to SQL
        conn = pymssql.connect(
            server=server,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Call iRail API
        url = "https://api.irail.be/liveboard/?station=Gent-Sint-Pieters&format=json"
        response = requests.get(url)
        data = response.json()

        departures = data.get("departures", {}).get("departure", [])

        # Insert data into the db table in Azure
        for dep in departures:
            cursor.execute("""
                INSERT INTO DelayTrains
                (snapshot_time, station, train_id, scheduled_time, delay_seconds, platform, canceled)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (datetime.now(),
            data.get("station"),
            dep.get("vehicle"),
            datetime.fromtimestamp(int(dep.get("time"))),
            int(dep.get("delay")),
            dep.get("platform"),
            dep.get("canceled"))
            )

        conn.commit()
        cursor.close()
        conn.close()
        return func.HttpResponse(
            f"Inserted {len(departures)} delay records.",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

