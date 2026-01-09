# Azure Train Data Project with iRail.be API

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0089D6?logo=microsoftazure&logoColor=white)
![Azure SQL](https://img.shields.io/badge/Azure_SQL_Database-CC2927?logo=microsoftsqlserver&logoColor=white)

## 1. Project Overview
This project builds a cloud-native data pipeline foundation for monitoring live train operations in Belgium using the iRail public transport API.
The system ingests real-time railway data (departures, delays, cancellations), stores it in an Azure SQL Database, and prepares it for downstream analytics and visualization to answer the following practical questions:

- Which stations experience the most delays?
- Which trains are most frequently canceled?
- Are certain platforms or routes more unreliable?

## 2. Architecture

The project uses a simple serverless setup where an Azure Function, written in Python, calls the iRail API to fetch live train data and stores the results in an Azure SQL Database. The Function is triggered via HTTP, handles the data processing logic, and runs in the cloud without needing dedicated servers, making the system easy to maintain and scale.

## 3. Database Schema

The Azure SQL Database stores normalized operational data.
```
CREATE TABLE DelayTrains (
    id INT IDENTITY PRIMARY KEY,
    snapshot_time DATETIME2 NOT NULL,
    station NVARCHAR(100),
    train_id NVARCHAR(50),
    scheduled_time DATETIME2,
    delay_seconds INT,
    platform NVARCHAR(10),
    canceled BIT
);
```

## 4. Azure Function implementation

**Runtime**
- Python 3.10
- HTTP-triggered Azure Function
- Deployed using the Azure Portal web editor

**Core Responsibilities**
- Fetch live data from the iRail API
- Normalise JSON payloads (Python)
- Insert records into Azure SQL using parameterised queries

**Environment Variables**

Sensitive credentials are stored securely in Function App -> Configuration -> App Settings:
```
SQL_SERVER

SQL_DATABASE

SQL_USERNAME

SQL_PASSWORD
```
No secrets are hardcoded.

## 5. Timeline

This project uses public data from iRail.be and is intended for educational purposes. It took 4 days to be executed. 

