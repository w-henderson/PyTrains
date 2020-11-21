from .data import timeParse

class Service:
    def __init__(self, untangledObject):
        # Timings
        self.scheduledDepartureTime = timeParse(untangledObject.DepartTime["time"])
        self.expectedDepartureTime = timeParse(untangledObject.ExpectedDepartTime["time"]) if len(untangledObject.ExpectedDepartTime["time"]) == 4 else self.scheduledDepartureTime
        self.delay = untangledObject.Delay["Minutes"]
        self.delay = self.delay if self.delay != "" else "0"
        self.delayCause = untangledObject.DelayCause.cdata
        self.delayed = (not self.delay.isnumeric()) or int(self.delay) > 0 or self.scheduledDepartureTime != self.expectedDepartureTime

        # Station information
        self.platform = untangledObject.Platform["Number"]
        if self.platform == "": self.platform = "?"
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
                try:
                    self.callingPoints.append(CallingPoint(
                        callingPoint["Name"],
                        callingPoint["crs"],
                        callingPoint["ttarr"],
                        callingPoint["ttdep"],
                        callingPoint["etarr"],
                        callingPoint["etdep"]
                    ))
                except:
                    continue
        try:
            self.callingPoints.append(CallingPoint(
                untangledObject.Destination1["name"],
                untangledObject.Destination1["crs"],
                untangledObject.Destination1["ttarr"],
                untangledObject.Destination1["ttarr"],
                untangledObject.Destination1["etarr"],
                untangledObject.Destination1["etarr"]
            ))
        except ValueError:
            try:
                self.callingPoints.append(CallingPoint(
                    untangledObject.Destination1["name"],
                    untangledObject.Destination1["crs"],
                    untangledObject.Destination1["ttarr"],
                    untangledObject.Destination1["ttarr"],
                    untangledObject.Destination1["ttarr"],
                    untangledObject.Destination1["ttarr"]
                ))
            except:
                pass

        # Carriage information
        self.carriageCount = untangledObject.Coaches1.cdata
        if self.carriageCount == "": self.carriageCount = "?"
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
    
    def __repr__(self):
        return "<Service {} to {}>".format(
            self.scheduledDepartureTime.strftime("%H:%M"),
            self.destination
        )

class CallingPoint:
    def __init__(self, name, crs, timetabledArrival, timetabledDeparture, estimatedArrival, estimatedDeparture):
        self.name = name
        self.crs = crs
        self.timetabledArrival = timeParse(timetabledArrival)
        self.timetabledDeparture = timeParse(timetabledDeparture)
        self.estimatedArrival = timeParse(estimatedArrival)
        self.estimatedDeparture = timeParse(estimatedDeparture)
        self.delayed = timetabledDeparture == estimatedDeparture
    def __repr__(self):
        return "<CallingPoint {} ({})>".format(
            self.name,
            self.crs
        )

class Carriage:
    def __init__(self, number, catering, bikes, wheelchairs, firstClass):
        self.number = int(number)
        self.catering = catering == "Y"
        self.bikes = bikes == "Y"
        self.wheelchairs = wheelchairs == "Y"
        self.firstClass = firstClass == "Y"
    def __repr__(self):
        return "<Carriage {}>".format(self.number)