![PyTrains banner](https://raw.githubusercontent.com/w-henderson/PyTrains/master/assets/banner.png)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/w-henderson/PyTrains/PyTrains-Tests) [![GitHub license](https://img.shields.io/github/license/w-henderson/PyTrains)](https://github.com/w-henderson/PyTrains/blob/master/LICENSE) ![PyPI - Downloads](https://img.shields.io/pypi/dm/PyTrains) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PyTrains) ![GitHub Repo stars](https://img.shields.io/github/stars/w-henderson/PyTrains)

# PyTrains

PyTrains is a simple Python library and command-line interface to obtain realtime UK train information through [Worldline's "Tiger" train API](http://iris2.rail.co.uk/tiger/), which is unfortunately undocumented, making this library very difficult to create and maintain!

## Command Line Interface
<img src="https://raw.githubusercontent.com/w-henderson/PyTrains/master/assets/example_cli_output.png" align="left" width="250">

The command line interface is very simple and easy to use. You can do three things with it, the first of which is simply viewing the departure board for a certain station by running `pytrains <crs code or station name>`. For example, if I wanted departures from Birmingham New Street, I could type `pytrains brs` or `pytrains birmingham new street` (both case-insensitive). The second usage is to find more information about a service. When you run the first command, each service has an ID on the left. To get more information about a service with a specific ID, you can run `pytrains -i <id>` or `pytrains --id <id>`. The final usage is to find the first train calling at a certain destination from a given station, which can be done by running `pytrains <origin> -d <destination>` or `pytrains <origin> --dest <destination>`. For example, if I want to know the next train from London Paddington which stops at Exeter St Davids, I could type `pytrains pad -d exd` or `pytrains london paddington --dest exeter st davids`.

## Use as a Python Module [(Full Documentation)](https://github.com/w-henderson/PyTrains/blob/master/DOCUMENTATION.md)
PyTrains can also be imported and used as a Python module with easy-to-understand syntax. Here's a very simple example program to get you going:
```py
import pytrains

station = pytrains.Station("BHM")

print("The next train from {} is the {} to {}.".format(
    station.name,
    station.services[0].departureTime.strftime("%H:%M"),
    station.services[0].destination
))
# Sample output: The next train from Birmingham New Street is the 16:45 to Four Oaks.

print("It has {} carriages, is delayed by {} minutes, and will be on Platform {}.".format(
    station.services[0].carriageCount,
    station.services[0].delay,
    station.services[0].platform
))
# Sample output: It has 6 carriages, is delayed by 9 minutes, and will be on Platform 8.
```

This is just scratching the surface of what PyTrains is capable of, so make sure to have a browse of the documentation to learn about its full capabilities.

## How to Install

### Install from PyPI:
Just run `pip install pytrains` to install. Dependencies will be automatically installed.

### Install manually
1. Clone the repo: `git clone https://github.com/w-henderson/PyTrains`
2. Navigate to its directory: `cd PyTrains`
3. Install dependencies: `pip install -r requirements.txt`
4. Install the package: `python setup.py install`
