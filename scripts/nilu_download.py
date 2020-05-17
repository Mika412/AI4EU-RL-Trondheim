import niluclient as nilu

client = nilu.create_location_client(63.4305, 10.3951)

# name of all stations found.
station_names = client.station_names

# dict of all stations with readings.
stations = client.station_data

print(stations)
# all stations NO2 readings
for station in stations.values():
    # print(station)
    # no2_value = station.sensors[nilu.NO2].value
    print(station.sensors)