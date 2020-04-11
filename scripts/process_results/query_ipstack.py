import requests
import pprint
import json

IP_FILE_PATH = "../../results/ip/total_ip_results.json"

IPSTACK_API_KEY = ""
IPSTACK_URL = "http://api.ipstack.com/{}?access_key={}"

OUT_FILE = "../../results/ipstack/ip_coordinates.json"


def ips_to_coordinates(service_dict):
    """
    Takes a dict from ip to number of hits
    Adds coordinates to each IP.
    """
    coord_counts = []
    for ip in service_dict:
        print("querying for '{}'".format(ip))
        response = requests.get(IPSTACK_URL.format(ip, IPSTACK_API_KEY))
        content = json.loads(response.content)
        lat = content['latitude']
        long = content['longitude']
        coord_counts.append([lat, long, service_dict[ip]])
    return coord_counts


def main():
    if IPSTACK_API_KEY == "":
        print("Missing API key")
        return

    with open(IP_FILE_PATH, 'r') as ip_file:
        ips = json.load(ip_file)

        kubernetes_ips = ips['kubernetes']
        kubernetes_coords = ips_to_coordinates(kubernetes_ips)
        print()

        etcd_ips = ips['etcd']
        etcd_coords = ips_to_coordinates(etcd_ips)
        print()

        print("#####" * 15)
        print("Kubernetes")
        print("#####" * 15)
        pprint.pprint(kubernetes_coords, width=120)

        print()
        print("#####" * 15)
        print("Etcd")
        print("#####" * 15)
        pprint.pprint(etcd_coords, width=120)

        total = {
            "kubernetes": kubernetes_coords,
            "etcd": etcd_coords
        }

        with open(OUT_FILE, "w") as out_file:
            out_file.write(json.dumps(total))


if __name__ == '__main__':
    main()
