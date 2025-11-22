from argparse import ArgumentParser
import jsonlines

from .data_processing import process_file_earliest_mixing_time
from .metrics import aggregate_metric, plot_metric

def main():
    parser = ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    reader = jsonlines.open(args.filename, mode="r")
    results = process_file_earliest_mixing_time(reader)
    stats = aggregate_metric(results, metric_key="mixing_time")
    plot_metric(stats, metric_name="mixing_time")
