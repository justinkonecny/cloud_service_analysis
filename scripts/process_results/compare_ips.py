import pprint
import json

INPUT_FILE = "../../visuals/combined_ip_results.json"

LOG_SUFFIX = ".json"

KUBE = "kubernetes"
ETCD = "etcd"

PRINT_WIDTH = 120


def increment(key: str, dictionary: dict, count: int) -> None:
    if key in dictionary:
        dictionary[key] += count
    else:
        dictionary[key] = count


def compare_both(kube_ip_dict, etcd_ip_dict):
    common_ip_dict = {}
    for kube_ip, kube_count in kube_ip_dict.items():
        if kube_ip in etcd_ip_dict:
            common_ip_dict[kube_ip] = kube_count + etcd_ip_dict[kube_ip]
    return common_ip_dict


def main():
    total_kube_ips_dict = {}
    total_etcd_ips_dict = {}

    kube_count = 0
    etcd_count = 0

    with open(INPUT_FILE, "r") as results_file:
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
    print("COMMON:")

    common = compare_both(total_kube_ips_dict, total_etcd_ips_dict)
    pprint.pprint(common, width=PRINT_WIDTH)


main()
