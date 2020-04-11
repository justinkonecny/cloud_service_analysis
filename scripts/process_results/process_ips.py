import pprint
import json
import os

INPUT_KUBE_DIR = "../../results/kubernetes/"
INPUT_ETCD_DIR = "../../results/etcd/"

OUT_DIR = "../../results/ip/"
OUT_FILE = "total_ip_results.json"

LOG_SUFFIX = ".json"

RESP_STATUS = "responseStatus"
USER_AGENT = "userAgent"
SOURCE_IPS = "sourceIPs"
CODE = "code"

PRE = "rejected connection from \""
MID = "\" (error \""
POST = "\""

PRINT_WIDTH = 120


def increment(key: str, dictionary: dict) -> None:
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def run_kube():
    kube_non_ignore_count = 0
    kube_event_count = {}
    kube_events = {}
    kube_ip_count = {}

    print("#####" * 20)
    print("PROCESSING KUBERNETES RESULTS")
    print("#####" * 20)

    for file_name in os.listdir(INPUT_KUBE_DIR):
        if file_name[(-1) * len(LOG_SUFFIX):] != LOG_SUFFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(INPUT_KUBE_DIR + file_name, "r") as results_file:
            print("processing '{}'".format(file_name))

            kube_event_list = json.loads(results_file.read())
            for kube_event in kube_event_list:
                response_code = str(kube_event[RESP_STATUS][CODE])
                increment(response_code, kube_event_count)

                for kube_source_ip in kube_event[SOURCE_IPS]:
                    increment(kube_source_ip, kube_ip_count)

                kube_non_ignore_count += 1
                if response_code in kube_events:
                    kube_events[response_code].append(kube_event)
                else:
                    kube_events[response_code] = [kube_event]

    total_count = 0
    for count in kube_event_count.values():
        total_count += count

    print("\nKube Total Count: [{}]".format(total_count))
    print("Kube Non-Ignore Count: [{}]\n".format(kube_non_ignore_count))
    print("Kube Count-Per-IP:")
    pprint.pprint(kube_ip_count, width=PRINT_WIDTH)

    print("\nKube Total:")
    pprint.pprint(kube_event_count, width=PRINT_WIDTH)

    return kube_ip_count


def run_etcd():
    etcd_non_ignore_count = 0
    ectd_total_count = 0
    etcd_events = {}
    etcd_ip_count = {}

    print("#####" * 20)
    print("PROCESSING ETCD RESULTS")
    print("#####" * 20)

    for file_name in os.listdir(INPUT_ETCD_DIR):
        if file_name[(-1) * len(LOG_SUFFIX):] != LOG_SUFFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(INPUT_ETCD_DIR + file_name, "r") as results_file:
            print("processing '{}'".format(file_name))

            etcd_event_list = json.loads(results_file.read())
            for event in etcd_event_list:
                ectd_total_count += 1

                if PRE in event:
                    event_rest = event.split(PRE, 1)[1]

                    if MID in event_rest:
                        rest_split = event_rest.split(MID, 1)
                        ip = rest_split[0].split(":")[0]
                        rest = rest_split[1]
                        increment(ip, etcd_ip_count)

                        if POST in rest:
                            final = rest.split(POST, 1)
                            error = final[0]
                            etcd_non_ignore_count += 1

                            if ip in etcd_events:
                                etcd_events[ip].append(error)
                            else:
                                etcd_events[ip] = [error]

    print("\nEtcd Total Count: [{}]".format(ectd_total_count))
    print("Etcd Non-Ignore Count: [{}]\n".format(etcd_non_ignore_count))

    print("Etcd Errors:")
    pprint.pprint(etcd_events, width=PRINT_WIDTH)

    print("\nEtcd Count-Per-IP:")
    pprint.pprint(etcd_ip_count, width=PRINT_WIDTH)
    return etcd_ip_count


def compare_both(kube_ip_dict, etcd_ip_dict):
    common_ip_dict = {}
    for kube_ip, kube_count in kube_ip_dict.items():
        if kube_ip in etcd_ip_dict:
            common_ip_dict[kube_ip] = kube_count + etcd_ip_dict[kube_ip]
    return common_ip_dict


def main():
    kube_ip_dict = run_kube()
    print()
    etcd_ip_dict = run_etcd()
    print()

    common_ip_dict = compare_both(kube_ip_dict, etcd_ip_dict)
    print("#####" * 20)
    print("COMMON Results")
    print("#####" * 20)
    pprint.pprint(common_ip_dict, width=PRINT_WIDTH)

    print("#####" * 20)
    print("TOTAL Results")
    print("#####" * 20)
    total = {
        "kubernetes": kube_ip_dict,
        "etcd": etcd_ip_dict
    }

    pprint.pprint(total, width=PRINT_WIDTH)
    print()
    with open(OUT_DIR + OUT_FILE, "w") as out_file:
        print("writing '{}'".format(OUT_DIR + OUT_FILE))
        out_file.write(json.dumps(total))


main()
