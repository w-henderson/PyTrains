from datetime import datetime, timedelta
from .station import Station
from .data import getName, getCRS
import argparse
import colorama
colorama.init()

parser = argparse.ArgumentParser(description="Get realtime UK train information through a simple Python API.")
parser.add_argument("station", help="Name or CRS code for the station.", nargs="+")
args = parser.parse_args()
command = " ".join(args.station)

def addMins(tm, mins):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(minutes=mins)
    return fulldate.time()

def main():
    try:
        crs = getCRS(command)
    except:
        try:
            valid = getName(command.upper())
            crs = command.upper()
        except:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "[ERROR]: CRS code invalid." + colorama.Style.RESET_ALL)
            return

    station = Station(crs)

    print(colorama.Style.BRIGHT + colorama.Fore.CYAN, end="")

    print("\n  == Departures from {} ==\n".format(station.name))

    for i in range(len(station.services)):
        departure = station.services[i]

        delayString = "On time"
        delayColor = colorama.Fore.GREEN
        if departure.delayed:
            delayColor = colorama.Fore.RED
            delayString = "Ex. {}".format(departure.expectedDepartureTime.strftime("%H:%M"))
        print(colorama.Fore.RESET, end="")

        print(
            "  " + str(i+1).ljust(3),
            departure.scheduledDepartureTime.strftime("%H:%M").ljust(6),
            delayColor + delayString.ljust(10) + colorama.Fore.WHITE,
            ("Platform " + departure.platform).ljust(13) + colorama.Fore.YELLOW,
            departure.destination
        )

    print(colorama.Fore.WHITE, end="")
    more = input("\n  Enter service ID for more information or press ENTER to quit : ")

    if more.isnumeric():
        service = station.services[int(more) - 1]

        print(colorama.Style.BRIGHT + colorama.Fore.CYAN, end="")
        print("\n  == {} to {} {}==\n".format(
            service.expectedDepartureTime.strftime("%H:%M"),
            service.destination,
            "" if service.carriageCount == "?" else "(" + service.carriageCount + " carriages) "
        ))
        print(colorama.Fore.RESET, end="")
        
        if service.delayCause != "":
            print("  Delayed due to {}.".format(service.delayCause))

        for note in [service.trainComment, service.platformComment]:
            if note != "":
                print("  " + note+"\n")

        print("  Calling at:")
        for callingPoint in service.callingPoints:
            print(
                "  " + callingPoint.estimatedArrival.strftime("%H:%M").ljust(6) + colorama.Fore.YELLOW,
                callingPoint.name + colorama.Fore.RESET
            )
    
    print(colorama.Style.RESET_ALL, end="")