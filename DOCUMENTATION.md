# PyTrains Documentation

# Command-Line Interface
```
usage: pytrains station [-h] [-i ID] [-d DEST]

Get realtime UK train information through a simple Python API.

positional arguments:
  station               Name or CRS code for the station.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         see the version and check for updates
  -i ID, --id ID        service ID to get more information about
  -d DEST, --dest DEST  destination to find the next train to
```

# Classes from file `station.py`

## `Station` class
This represents a station and is the class used to make the request to the API. It is passed a CRS code as its only parameter when created, e.g. `station = pytrains.Station("BHM")`.

Attributes:
- `crs`: CRS code of the station, e.g. "BHM"
- `name`: Full name of the station, e.g. "Birmingham New Street"
- `services`: List of `Service` objects representing departures from this station
- `specialNotice`: If services weren't obtained, this message tries to give a reason

Methods:
- `updateServices()`: Update services from this station.

# Classes from file `service.py`

## `Service` class
This represents a train service from the station.

Timing-related Attributes:
- `scheduledDepartureTime`: Time of the train's scheduled departure from the station as a datetime.time object
- `expectedDepartureTime`: Time of the train's expected departure from the station as a datetime.time object
- `delay`: Delay of the train in minutes as a string, equal to "0" if none or unknown
- `delayCause`: Reason for the delay, equal to "" if unknown or on time
- `delayed`: Whether the train is delayed or not (boolean)
- `lastReport`: The train's last reported location, equal to "No report." if unknown

Station-related Attributes:
- `platform`: The platform the train will stop at as a string, equal to "?" if unknown
- `platformComment`: Comment displayed on the platform screens, equal to "" if unavailable

Journey-related Attributes:
- `origin`: The name of the station from which the train originated
- `destination`: The name of the station the train will terminate at
- `destinationCRS`: The CRS code of the station the train will terminate at
- `via`: The name of a station that the train goes via, equal to "" if unavailable
- `callingPoints`: List of `CallingPoint` objects representing the stations the train stops at

Train-related Attributes:
- `operator`: The operator of the train, e.g. "GWR"
- `trainComment`: Comment displayed about the train, equal to "" if unavailable
- `carriageCount`: The number of the carriages on the train as a string, equal to "?" if unavailable
- `additionalCarriageData`: list of `Carriage` objects representing the carriages of the train, equal to None if unavailable

## `CallingPoint` class
This represents a calling point of the train.

Attributes:
- `name`: The name of the station
- `crs`: The CRS code of the station
- `timetabledArrival`: The timetabled arrival of the train as a datetime.time object
- `timetabledDepartire`: The timetabled departure of the train as a datetime.time object
- `estimatedArrival`: The estimated arrival of the train as a datetime.time object
- `estimatedDeparture`: The estimated departure of the train as a datetime.time object
- `delayed`: Whether the train will be delayed when it leaves this station (boolean)

## `Carriage` class
This represents a carriage of the train. Not all services have information about this.
- `number`: The number of the carriage (1 being the front) as an integer
- `catering`: Whether the carriage has catering (boolean)
- `bikes`: Whether the carriage has room for bikes (boolean)
- `wheelchairs`: Whether the carriage has room for wheelchairs (boolean)
- `firstClass`: Whether the carriage is first class (boolean)

# Functions from file `data.py`

## `getCRS()` function
Usage: `getCRS(stationName)`

Returns the CRS code of the specified station, raises Exception if not found.

## `getName()` function
Usage: `getName(crsCode)`

Returns the name of the specified station, raises Exception if not found.

## `getLink()` function
Usage: `getLink(crsCode)`

Returns the XML filename the API uses for the specified station.

## `timeParse()` function
Usage: `timeParse(time)`

Parses time as a string in the format "HHMM" to a datetime.time object.

## `search()` function
Usage: `search(query)`

Returns a list of station names matching the search query.