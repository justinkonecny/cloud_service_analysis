import pprint
import json
import os

INPUT_DIR = "../../visuals/partial_ips/"

OUT_DIR = "../../visuals/"
OUT_FILE = "combined_ip_results.json"

LOG_SUFFIX = ".json"

KUBE = "kubernetes"
ETCD = "etcd"

PRINT_WIDTH = 120


def increment(key: str, dictionary: dict, count: int) -> None:
    if key in dictionary:
        dictionary[key] += count
    else:
        dictionary[key] = count


def main():
    total_kube_ips_dict = {}
    total_etcd_ips_dict = {}

    kube_count = 0
    etcd_count = 0

    for file_name in os.listdir(INPUT_DIR):
        if file_name[(-1) * len(LOG_SUFFIX):] != LOG_SUFFIX:
            print("skipping '{}'".format(file_name))
            continue

        with open(INPUT_DIR + file_name, "r") as results_file:
            print("processing '{}'".format(file_name))

            total_json = json.loads(results_file.read())
            kube_map = total_json[KUBE]
            for kube_ip in kube_map:
                count_kube = kube_map[kube_ip]
                increment(kube_ip, total_kube_ips_dict, count_kube)
                kube_count += count_kube

            etcd_map = total_json[ETCD]
            for etcd_ip in etcd_map:
                count_etcd = etcd_map[etcd_ip]
                increment(etcd_ip, total_etcd_ips_dict, count_etcd)
                etcd_count += count_etcd

    print("\nKube Total Count: [{}]".format(kube_count))
    print("Etcd Total Count: [{}]\n".format(etcd_count))

    total = {
        "kubernetes": total_kube_ips_dict,
        "etcd": total_etcd_ips_dict
    }

    pprint.pprint(total, width=PRINT_WIDTH)
    print()
    with open(OUT_DIR + OUT_FILE, "w") as out_file:
        print("writing '{}'".format(OUT_DIR + OUT_FILE))
        out_file.write(json.dumps(total))


main()
