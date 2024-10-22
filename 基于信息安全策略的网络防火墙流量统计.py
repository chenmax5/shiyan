from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

# 标志变量，用于判断是否已经捕获到TCP和UDP包
tcp_captured = False
udp_captured = False


# 解析并输出 TCP 头信息
def parse_tcp_packet(packet):
    tcp_layer = packet[TCP]
    print("\n=== TCP Packet ===")
    print(f"Source Port: {tcp_layer.sport}")
    print(f"Destination Port: {tcp_layer.dport}")
    print(f"Sequence Number: {tcp_layer.seq}")
    print(f"Acknowledgment Number: {tcp_layer.ack}")
    print(f"Data Offset: {tcp_layer.dataofs * 4} bytes")
    print(f"Flags: {tcp_layer.flags}")
    print(f"Window Size: {tcp_layer.window}")
    print(f"Checksum: {tcp_layer.chksum}")
    print(f"Urgent Pointer: {tcp_layer.urgptr}")


# 解析并输出 UDP 头信息
def parse_udp_packet(packet):
    udp_layer = packet[UDP]
    print("\n=== UDP Packet ===")
    print(f"Source Port: {udp_layer.sport}")
    print(f"Destination Port: {udp_layer.dport}")
    print(f"Length: {udp_layer.len}")
    print(f"Checksum: {udp_layer.chksum}")


# 根据协议类型解析数据包
def packet_handler(packet):
    global tcp_captured, udp_captured

    if IP in packet:
        ip_layer = packet[IP]
        print(f"\nSource IP: {ip_layer.src}")
        print(f"Destination IP: {ip_layer.dst}")
        print(f"Protocol: {ip_layer.proto}")

        if TCP in packet and not tcp_captured:
            parse_tcp_packet(packet)
            tcp_captured = True
        elif UDP in packet and not udp_captured:
            parse_udp_packet(packet)
            udp_captured = True

    # 如果已经捕获到一个 TCP 和一个 UDP 包，则停止捕获
    return tcp_captured and udp_captured


def main():
    # 捕获 IP 数据包，解析 TCP 和 UDP 协议
    print("Capturing one TCP packet and one UDP packet...")
    sniff(prn=packet_handler, filter="ip", store=0, stop_filter=packet_handler)


if __name__ == "__main__":
    main()
