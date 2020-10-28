import argparse
import configparser
import datetime
import os

from scripts import generate_poly
from scripts.process_sensor_data import processSensorData

# Static vars

map_filename = "osm.net.xml"
sensor_filename = "sensor_location.csv"
sensor_data_dir = "data/"

detectors_filename = "detectors.xml"
detections_filename = "detections.csv"

map_output_directory = "data/"

generated_location = "generated/"
routes_filename = "routes.xml"
flows_filename = "flows.xml"

poly_filename = "polys.add.xml"
districts_filename = "districts.taz.xml"

simulations_directory = "simulations/"


def create_detections(map_location, sensors_directory, hours, percentage, offset):
    print("Creating detections")

    processSensorData(
        map_location + map_filename,
        sensors_directory + sensor_filename,
        sensors_directory + sensor_data_dir,
        map_location + map_output_directory,
        max_steps=hours,
        percentage_to_use=percentage,
        start_offset=offset,
    )


def create_routes(map_location):
    print("Creating routes and flows")
    flowrouterString = (
        "$SUMO_HOME/tools/detector/flowrouter.py -n {map} -d {detector} -f {detections} -o {"
        "routesOutput} -e {"
        "flowOutput} -i 60 -l --random"
    )
    flowrouterCommand = flowrouterString.format(
        map=map_location + map_filename,
        detector=map_location + map_output_directory + detectors_filename,
        detections=map_location + map_output_directory + detections_filename,
        routesOutput=map_location + generated_location + routes_filename,
        flowOutput=map_location + generated_location + flows_filename,
    )
    print(flowrouterCommand)
    if not os.path.exists(map_location + generated_location):
        os.makedirs(map_location + generated_location)

    os.system(flowrouterCommand)


def create_polys(
    map_location, poly_max_width, poly_max_height, poly_width, poly_height
):
    print("Creating polys")
    generate_poly.generatePoly(
        map_location + poly_filename,
        poly_max_width,
        poly_max_height,
        poly_width,
        poly_height,
    )

    print("Finding edges that belong to each poly")
    edgeConvert = (
        "$SUMO_HOME/tools/edgesInDistricts.py -n {map} -t {polyfile} -o {output}"
    )
    edgeCommand = edgeConvert.format(
        map=map_location + map_filename,
        polyfile=map_location + poly_filename,
        output=map_location + districts_filename,
    )
    print(edgeCommand)
    os.system(edgeCommand)

    config = configparser.ConfigParser()
    config.read(map_location + "/config.ini")
    print(config.sections())
    config["DEFAULT"] = {
        "cell_max_height": poly_max_height,
        "cell_max_width": poly_max_width,
        "cell_height": poly_height,
        "cell_width": poly_width,
        "timestep_seconds": 10,
    }
    with open(map_location + "/config.ini", "w") as configfile:
        config.write(configfile)


def validate_arguments(args):
    if args.poly and (not args.poly_max_width or not args.poly_max_height):
        raise argparse.ArgumentError(
            "--poly, requires poly-max-width and poly-max-height to be set "
        )

    if not args.map:
        raise argparse.ArgumentError("--map, Map environment must be set ")
    if args.det and not args.sensors:
        raise argparse.ArgumentError("--sensors, Sensors directory must be set.")


def dir_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_file:{path} is not a valid file path"
        )


def dir_path(path):
    if os.path.isdir(path):
        return os.path.join(path, "")
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def valid_date(date):
    if not date:
        return
    print(date)
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Given Date({date}) not valid")


def validate_percentage(perc):
    perc = float(perc)
    if perc < 0:
        raise argparse.ArgumentTypeError(f"The percentage should be between 0 and 1")
    else:
        return perc


def execute_args(args):
    if args.det:
        create_detections(
            args.map, args.sensors, args.timesteps, args.percentage, args.offset
        )

    if args.routes:
        create_routes(args.map)

    if args.poly:
        print(args)
        create_polys(
            args.map,
            args.poly_max_width,
            args.poly_max_height,
            args.poly_width,
            args.poly_height,
        )


parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument("-m", "--map", help="Map environment directory.", type=dir_path)
parser.add_argument("-s", "--sensors", help="Sensor directory.", type=dir_path)
parser.add_argument(
    "-t",
    "--timesteps",
    help="For how many timesteps in hours to generate data.",
    default=1,
    type=int,
)
parser.add_argument(
    "-pe",
    "--percentage",
    help="For how many hours to generate data.",
    default=1,
    type=validate_percentage,
)

parser.add_argument("-of", "--offset", help="Initial offset.", default=0, type=int)

parser.add_argument("--poly-max-width", help="Polygon map width.", type=int)
parser.add_argument("--poly-max-height", help="Polygon map width.", type=int)
parser.add_argument("--poly-width", help="Polygon width.", default=200, type=int)
parser.add_argument("--poly-height", help="Polygon width.", default=200, type=int)

parser.add_argument("-p", "--poly", help="Create poly files", action="store_true")
parser.add_argument(
    "-r", "--routes", help="Create routes and flows", action="store_true"
)
parser.add_argument("-d", "--det", help="Create detections", action="store_true")

args = parser.parse_args()
execute_args(args)
