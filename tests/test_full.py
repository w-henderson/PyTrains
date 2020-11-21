import pytrains
from datetime import time as dt

stations = [pytrains.Station("LYM"), pytrains.Station("PAD"), pytrains.Station("BRI")]

def test_service():
    for station in stations:
        for service in station.services:
            # Ensure types are correct
            assert type(service.departureTime) == dt
            assert type(service.callingPoints) == list
            assert type(service.additionalCarriageData) == list or service.additionalCarriageData == None
            assert service.delay.isnumeric()
            assert service.carriageCount.isnumeric()

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