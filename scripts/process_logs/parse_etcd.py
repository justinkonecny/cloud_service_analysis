import json
import os

FILTER_IP = ""

LOG_DIR = "../../logs/etcd_logs/"
OUT_DIR = "../../results/etcd/"

LOG_SUFFIX = ".log"

REJECTED = "rejected"
ERROR = "error"
TLS = "tls"
LOG = "log"


def increment(key: str, dictionary: dict) -> None:
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def main():
    events = []

    for file_name in os.listdir(LOG_DIR):
        if file_name[(-1) * len(LOG_SUFFIX):] != LOG_SUFFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(LOG_DIR + file_name, "r") as log_file:
            print("processing '{}'".format(file_name))

            event_raw = log_file.readline()
            while event_raw:
                event = json.loads(event_raw)

                log = event[LOG].strip()
                if FILTER_IP not in log:
                    if (REJECTED in log) \
                            or (ERROR in log) \
                            or (TLS in log):
                        events.append(log)

                event_raw = log_file.readline()

    print("\nNon-Ignore Count: [{}]\n".format(len(events)))

    with open(OUT_DIR + "etcd_results.json", "w") as out_file:
        print("writing '{}'".format(OUT_DIR + "etcd_results.json"))
        out_file.write(json.dumps(events))


main()
