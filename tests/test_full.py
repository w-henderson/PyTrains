import pytrains
import random
from datetime import time as dt

stations = [
    pytrains.Station("LYM"), # Lympstone Village (very small station)
    pytrains.Station("PAD"), # London Paddington (big station which doesn't release platform numbers)
    pytrains.Station("BRI"), # Bristol Temple Meads (medium/large station)
    pytrains.Station("BHM"), # Birmingham New Street (massive station with lots of weird edge cases)
    pytrains.Station(random.choice(list(pytrains.rawData.data.keys()))) # Randomly chosen station because why not
]

def test_service():
    for station in stations:
        for service in station.services:
            # Ensure types are correct
            assert type(service.scheduledDepartureTime) == dt
            assert type(service.expectedDepartureTime) == dt
            assert type(service.callingPoints) == list
            assert type(service.additionalCarriageData) == list or service.additionalCarriageData == None
            assert service.carriageCount.isnumeric() or service.carriageCount == "?"
            assert service.delay.isnumeric()

            # Ensure vital data has been obtained
            assert service.origin != ""
            assert service.destination != ""
            assert service.operator != ""

            # Check calling points
            for callingPoint in service.callingPoints:
                assert callingPoint.name != ""
                assert callingPoint.crs != ""

                assert type(callingPoint.timetabledArrival) == dt
                assert type(callingPoint.timetabledDeparture) == dt
                assert type(callingPoint.estimatedArrival) == dt
                assert type(callingPoint.estimatedDeparture) == dt