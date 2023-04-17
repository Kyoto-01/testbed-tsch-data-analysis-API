#!/usr/bin/env python3

def test():
    from database.db_connection import InfluxDBConnection

    db = InfluxDBConnection('../config.ini')

    bucket = "testbed-3b2970fd-3629-46dd-b536-691a8c83cd73"
    measurement = "client"
    field = "ch"
    tags = {
        'addrrecv': "fd0000000000000002124b0018e0b9f2"
    }

    select = db.select(
        bucket=bucket,
        measurement=measurement,
        field=field,
        tags=tags,
        unique=True
    )

    secs = (select[len(select) - 1]['time'] - select[0]['time']).total_seconds()

    print('SECS:', secs)
    print('SELECT:', select)

    # count = db.count(
    #     bucket=bucket,
    #     measurement=measurement,
    #     field=field,
    #     tags=tags,
    #     unique=True
    # )

    # print('COUNT:', count)