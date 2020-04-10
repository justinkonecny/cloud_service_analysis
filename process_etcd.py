import pprint
import json
import os

LOG_DIR = "results/etcd/"

LOG_SUFFIX = ".json"  # only parse logs that begin with this

RESP_STATUS = "responseStatus"
USER_AGENT = "userAgent"
SOURCE_IPS = "sourceIPs"
CODE = "code"

PRE = "rejected connection from \""
MID = "\" (error \""
POST = "\""


def increment(key: str, dictionary: dict) -> None:
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def main():
    non_ignore_count = 0
    total_count = 0
    events = {}
    ip_count = {}

    for file_name in os.listdir(LOG_DIR):
        if file_name[(-1) * len(LOG_SUFFIX):] != LOG_SUFFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(LOG_DIR + file_name, "r") as log_file:
            print("processing '{}'".format(file_name))

            event_raw = log_file.read()
            event_list = json.loads(event_raw)
            for event in event_list:

                total_count += 1

                event = event.replace("\n", "")

                if PRE in event:
                    event_rest = event.split(PRE, 1)[1]

                    if MID in event_rest:
                        rest_split = event_rest.split(MID, 1)
                        ip = rest_split[0].split(":")[0]
                        rest = rest_split[1]
                        increment(ip, ip_count)

                        if POST in rest:
                            final = rest.split(POST, 1)
                            error = final[0]

                            non_ignore_count += 1
                            if ip in events:
                                events[ip].append(error)
                            else:
                                events[ip] = [error]

    print("\nTotal Count: [{}]".format(total_count))
    print("Non-Ignore Count: [{}]\n".format(non_ignore_count))
    print("IPs:")
    pprint.pprint(ip_count)
    print()

    print("\nTOTAL:")
    pprint.pprint(events)


main()
