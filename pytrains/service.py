from .data import timeParse

class Service:
    def __init__(self, untangledObject):
        # Timings
        self.departureTime = timeParse(untangledObject.DepartTime["time"])
        self.delay = untangledObject.Delay["Minutes"]
        self.delayCause = untangledObject.DelayCause.cdata

        # Station information
        self.platform = untangledObject.Platform["Number"]
        self.platformComment = (untangledObject.PlatformComment1.cdata.strip() + " " + untangledObject.PlatformComment2.cdata.strip()).strip()

        # Train information
        self.origin = untangledObject.Origin1["name"]
        self.destination = untangledObject.Destination1["name"]
        self.via = untangledObject.Via.cdata
        self.operator = untangledObject.Operator["name"]
        self.trainComment = untangledObject.AssociatedPageNotices.cdata

        # Calling points information
        self.callingPoints = []
        if untangledObject.Dest1CallingPoints["NumCallingPoints"] != "0":
            for callingPoint in untangledObject.Dest1CallingPoints.CallingPoint:
                self.callingPoints.append(StaticStation(
                    callingPoint["Name"],
                    callingPoint["crs"],
                    callingPoint["ttarr"],
                    callingPoint["ttdep"],
                    callingPoint["etarr"],
                    callingPoint["etdep"]
                ))
        self.callingPoints.append(StaticStation(
            untangledObject.Destination1["name"],
            untangledObject.Destination1["crs"],
            untangledObject.Destination1["ttarr"],
            untangledObject.Destination1["ttarr"],
            untangledObject.Destination1["etarr"],
            untangledObject.Destination1["etarr"]
        ))

        # Carriage information
        self.carriageCount = untangledObject.Coaches1.cdata
        try:
            if untangledObject.CoachesList.cdata == "":
                self.additionalCarriageData = None
            else:
                self.additionalCarriageData = []
                for coach in untangledObject.CoachesList.Coach:
                    self.additionalCarriageData.append(Carriage(
                        coach["CoachNumber"],
                        coach["Catering"],
                        coach["BikeStorage"],
                        coach["Wheelchairs"],
                        coach["FirstClass"]
                    ))
                self.additionalCarriageData.sort(key=lambda x: x.number)
        except AttributeError:
            self.additionalCarriageData = None

class StaticStation:
    def __init__(self, name, crs, timetabledArrival, timetabledDeparture, estimatedArrival, estimatedDeparture):
        self.name = name
        self.crs = crs
        self.timetabledArrival = timeParse(timetabledArrival)
        self.timetabledDeparture = timeParse(timetabledDeparture)
        self.estimatedArrival = timeParse(estimatedArrival)
        self.estimatedDeparture = timeParse(estimatedDeparture)
        self.delayed = self.timetabledDeparture == self.estimatedDeparture

class Carriage:
    def __init__(self, number, catering, bikes, wheelchairs, firstClass):
        self.number = int(number)
        self.catering = catering == "Y"
        self.bikes = bikes == "Y"
        self.wheelchairs = wheelchairs == "Y"
        self.firstClass = firstClass == "Y"