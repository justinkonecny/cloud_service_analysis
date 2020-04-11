import pprint
import json
import os

FILTER_IP = ""
AWS_PRIVATE_IP = "10.0.0"

LOG_DIR = "../../logs/audit_logs/"
OUT_DIR = "../../results/partial/"

LOG_PREFIX = "audit"

RESP_STATUS = "responseStatus"
USER_AGENT = "userAgent"
SOURCE_IPS = "sourceIPs"
CODE = "code"


def increment(key: str, dictionary: dict) -> None:
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def main():
    non_ignore_count = 0
    event_count = {}
    events = {}
    ip_count = {}

    for file_name in os.listdir(LOG_DIR):
        if file_name[:len(LOG_PREFIX)] != LOG_PREFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(LOG_DIR + file_name, "r") as log_file:
            print("processing '{}'".format(file_name))

            event_raw = log_file.readline()
            while event_raw:
                event = json.loads(event_raw)
                if RESP_STATUS in event:
                    response_status = event[RESP_STATUS]

                    if CODE in response_status:
                        response_code = str(response_status[CODE])
                        increment(response_code, event_count)  # increment count for this HTTP status code

                        if SOURCE_IPS in event:
                            should_log = True

                            for ip in event[SOURCE_IPS]:
                                increment(ip, ip_count)  # increment count for this IP
                                if ip == "::1" or ip[:len(AWS_PRIVATE_IP)] == AWS_PRIVATE_IP or (FILTER_IP != "" and ip == FILTER_IP):
                                    # don't log IPv6 loopback, local traffic, or your traffic
                                    should_log = False

                            if should_log:
                                non_ignore_count += 1
                                if response_code in events:
                                    events[response_code].append(event)
                                else:
                                    events[response_code] = [event]

                event_raw = log_file.readline()

    total_count = 0
    for count in event_count.values():
        total_count += count

    print("\nTotal Count: [{}]".format(total_count))
    print("Non-Ignore Count: [{}]\n".format(non_ignore_count))
    print("IPs:")
    pprint.pprint(ip_count)
    print()

    for code, event_list in events.items():
        with open(OUT_DIR + "kube_results_{}.json".format(code), "w") as out_file:
            print("writing '{}'".format(OUT_DIR + "kube_results_{}.json".format(code)))
            out_file.write(json.dumps(event_list))

    print("\nTOTAL:")
    pprint.pprint(event_count)


main()
