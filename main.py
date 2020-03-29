import pprint
import json
import os


LOG_DIR = "logs/audit_logs/"
OUT_DIR = "results/"
PRIV_IP = "10"

RESP_STATUS = "responseStatus"
USER_AGENT = "userAgent"
SOURCE_IPS = "sourceIPs"
CODE = "code"


def main():
    total_count = 0
    non_ignore_count = 0
    event_count = {}
    events = {}

    for file_name in os.listdir(LOG_DIR):
        if file_name == ".DS_Store":
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

                        total_count += 1
                        if response_code in event_count:
                            event_count[response_code] += 1
                        else:
                            event_count[response_code] = 1

                        if SOURCE_IPS in event:
                            for ip in event[SOURCE_IPS]:
                                if ip != "::1" and ip.split(".")[0] != PRIV_IP:
                                    non_ignore_count += 1
                                    if response_code in events:
                                        events[response_code].append(event)
                                    else:
                                        events[response_code] = [event]

                event_raw = log_file.readline()

    print("\nTotal Count: [{}]".format(total_count))
    print("Non-Ignore Count: [{}]".format(non_ignore_count))

    for code, event_list in events.items():
        with open(OUT_DIR + "results_{}.json".format(code), "w") as out_file:
            out_file.write(json.dumps(event_list))

    print("\nTOTAL:")
    pprint.pprint(event_count)


main()
