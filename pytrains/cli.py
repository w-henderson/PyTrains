from datetime import datetime, timedelta
from .station import Station
from .data import getName, getCRS
import argparse
import colorama
import sys

colorama.init()

if len(sys.argv) == 1:
    print("\n{}  == Welcome to PyTrains! ==\n".format(colorama.Style.BRIGHT + colorama.Fore.CYAN))
    print("  {}Welcome to PyTrains, a simple Python library and command-line interface to\n  obtain realtime UK train information from Worldline's Tiger API.\n".format(
        colorama.Fore.RESET
    ))
    print("  To get basic departure information for a station:\n    - {}pytrains <station name or CRS code>{}\n".format(
        colorama.Fore.YELLOW,
        colorama.Fore.RESET
    ))
    print("  To get information about a specific service:\n    - {}pytrains <station> [-i, --id] <service ID>{}\n".format(
        colorama.Fore.YELLOW,
        colorama.Fore.RESET
    ))
    print("  To get the next service to a destination:\n    - {}pytrains <origin station> [-d, --dest] <destination station>{}\n".format(
        colorama.Fore.YELLOW,
        colorama.Fore.RESET
    ))
    sys.exit(1)

parser = argparse.ArgumentParser(description="Get realtime UK train information through a simple Python API.")
parser.add_argument("station", help="Name or CRS code for the station.", nargs="+")
parser.add_argument("-i", "--id", type=int, help="service ID to get more information about")
parser.add_argument("-d", "--dest", type=str, help="destination to find the next train to", nargs="+")
args = parser.parse_args()
command = " ".join(args.station)
destination = None if args.dest == None else " ".join(args.dest)

def showServiceInfo(service, highlight=None):
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN, end="")
    print("\n  == {} to {} ({} carriages, platform {})==\n".format(
        service.expectedDepartureTime.strftime("%H:%M"),
        service.destination,
        service.carriageCount,
        service.platform        
    ))
    print(colorama.Fore.RESET, end="")
    
    if service.delayCause != "":
        print("  Delayed due to {}.".format(service.delayCause))

    for note in [service.lastReport, service.trainComment, service.platformComment]:
        if note != "":
            print("  " + note+"\n")

    print("  Calling at:")
    for callingPoint in service.callingPoints:
        mainColor = colorama.Fore.YELLOW
        if highlight != None:
            if callingPoint.name.lower() == highlight.lower() or callingPoint.crs.upper() == highlight.upper():
                mainColor = colorama.Fore.GREEN

        print(
            "  " + callingPoint.estimatedArrival.strftime("%H:%M").ljust(6) + mainColor,
            callingPoint.name + colorama.Fore.RESET
        )

def main():
    try:
        crs = getCRS(command)
    except:
        try:
            valid = getName(command.upper())
            crs = command.upper()
        except:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "[ERROR]: Station could not be found." + colorama.Style.RESET_ALL)
            return

    station = Station(crs)

    if station.specialNotice != "":
        print(colorama.Style.BRIGHT + colorama.Fore.RED + "SPECIAL NOTICE: " + colorama.Style.RESET_ALL + station.specialNotice)
        return

    print(colorama.Style.BRIGHT + colorama.Fore.CYAN, end="")

    if args.id == args.dest == None:
        print("\n  == Departures from {} ==\n".format(station.name))

        if (len(station.services)) == 0:
            print(colorama.Fore.RED + "  No services found.")

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
    
    elif args.id != None:
        try:
            service = station.services[args.id - 1]
        except:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "[ERROR]: Invalid train ID." + colorama.Style.RESET_ALL)
            return
        showServiceInfo(service)
    
    elif args.dest != None:
        service = None
        for serv in station.services:
            if serv.destinationCRS == destination.upper() or serv.destination.lower() == destination.lower():
                service = serv
                break
            for callingPoint in serv.callingPoints:
                if callingPoint.crs == destination.upper() or callingPoint.name.lower() == destination.lower():
                    service = serv
                    break
            if service != None: break
        if service == None:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "[ERROR]: No services found to specified destination." + colorama.Style.RESET_ALL)
        else:
            showServiceInfo(service, highlight=destination)

    print(colorama.Style.RESET_ALL, end="")