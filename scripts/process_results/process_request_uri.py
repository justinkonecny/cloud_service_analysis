import pprint
import json
import os

LOG_DIR = "../../results/kubernetes/"

LOG_SUFFIX = ".json"  # only parse logs that begin with this

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
        if file_name[(-1) * len(LOG_SUFFIX):] != LOG_SUFFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(LOG_DIR + file_name, "r") as log_file:
            print("processing '{}'".format(file_name))

            event_raw = log_file.read()
            event_list = json.loads(event_raw)
            for event in event_list:
                if RESP_STATUS in event:
                    response_status = event[RESP_STATUS]

                    if CODE in response_status:
                        response_code = str(response_status[CODE])
                        increment(response_code, event_count)  # increment count for this HTTP status code

                        if "requestURI" in event:
                            ip = event["requestURI"]
                            increment(ip, ip_count)

                            non_ignore_count += 1
                            if response_code in events:
                                events[response_code].append(event)
                            else:
                                events[response_code] = [event]

    total_count = 0
    for count in event_count.values():
        total_count += count

    print("\nTotal Count: [{}]".format(total_count))
    print("Non-Ignore Count: [{}]\n".format(non_ignore_count))
    print("IPs:")
    pprint.pprint(ip_count)
    print()


    print("\nTOTAL:")
    pprint.pprint(event_count)


main()
