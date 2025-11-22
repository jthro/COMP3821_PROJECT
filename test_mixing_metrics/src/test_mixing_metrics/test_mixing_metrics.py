from argparse import ArgumentParser
import jsonlines

from .data_processing import process_file_earliest_mixing_time, process_file_mvprsf
from .metrics import aggregate_metric, plot_metric

def main():
    parser = ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-s", "--statistic", help="valid: mean time to first valid colouring; rhat: multivariate PSRF")
    args = parser.parse_args()

    reader = jsonlines.open(args.filename, mode="r")

    if (args.statistic == "valid"):
        results = process_file_earliest_mixing_time(reader)
        stats = aggregate_metric(results, metric_key="mixing_time")
        plot_metric(stats, metric_name="mixing_time")
        
    else:
        results = process_file_mvprsf(reader)
        stats = aggregate_metric(results, metric_key="r_hat")
        plot_metric(stats, metric_name="r_hat")
