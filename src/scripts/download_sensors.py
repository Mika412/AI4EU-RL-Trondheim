import argparse
import cgi
import datetime
import os
import shutil
import urllib.request

import pandas as pd

url = "https://www.vegvesen.no/trafikkdata/api/export?from={startDate}&resolution=HOUR&to={endDate}&trpIds={id}"


def download_sensors(input_file, output_dir, start_date, end_date):
    sensors_df = pd.read_csv(input_file, sep=";", header=0, encoding="unicode_escape")
    sensor_names = sensors_df["Detector ID"].unique()
    print("test")
    for name in sensor_names:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        sensor_url = url.format(startDate=start_date, endDate=end_date, id=name)
        response = urllib.request.urlopen(sensor_url)

        content_disp = response.info()["Content-Disposition"]
        value, params = cgi.parse_header(content_disp)
        filename = params["filename"]
        with response, open(os.path.join(output_dir, "") + filename, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        print(filename)


def validate_arguments(args):
    if not args.input:
        raise argparse.ArgumentError("--input, Sensor input file is required ")

    if not args.output:
        raise argparse.ArgumentError("--output, Sensor output directory is required ")

    print(args)
    if not args.start:
        raise argparse.ArgumentError("--start, Start date is required ")

    if not args.end:
        raise argparse.ArgumentError(
            "--end, End date is required (it has to be the day after the desired limit)"
        )


def dir_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_file:{path} is not a valid file path"
        )


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def valid_date(date):
    if not date:
        return
    print(date)
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Given Date({date}) not valid")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Download sensor data")
    parser.add_argument("-i", "--input", help="Sensor input file.", type=dir_file)
    parser.add_argument(
        "-o", "--output", help="Sensor data output directory.", type=dir_path
    )
    parser.add_argument(
        "-s", "--start", help='Start date ("2019-12-02").', type=valid_date
    )
    parser.add_argument("-e", "--end", help='End date ("2019-12-02").', type=valid_date)
    args = parser.parse_args()

    validate_arguments(args)

    download_sensors(args.input, args.output, args.start, args.end)
