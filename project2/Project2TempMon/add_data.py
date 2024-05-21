from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('temperature_db')

json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "location": "office"
        },
        "fields": {
            "value": 23.5
        }
    },
    {
        "measurement": "temperature",
        "tags": {
            "location": "lab"
        },
        "fields": {
            "value": 24.1
        }
    },
    {
        "measurement": "temperature",
        "tags": {
            "location": "warehouse"
        },
        "fields": {
            "value": 22.8
        }
    }
]

client.write_points(json_body)

# إغلاق الاتصال
client.close()
