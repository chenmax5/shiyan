from scapy.all import sniff
from scapy.layers.inet import IP


def parse_ip_packet(packet):
    # 判断数据包中是否有 IP 层
    if IP in packet:
        ip_layer = packet[IP]
        print(f"Source IP: {ip_layer.src}")
        print(f"Destination IP: {ip_layer.dst}")
        print(f"Version: {ip_layer.version}")
        print(f"IHL: {ip_layer.ihl * 4} bytes")
        print(f"Total Length: {ip_layer.len}")
        print(f"TTL: {ip_layer.ttl}")
        print(f"Protocol: {ip_layer.proto}")


def main():
    # 只捕获一个 IP 包
    print("Capturing one IP packet...")
    sniff(prn=parse_ip_packet, filter="ip", count=1, store=0)


if __name__ == "__main__":
    main()
