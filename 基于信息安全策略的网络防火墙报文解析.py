import struct
import socket


# 解析 P 协议头部的函数
def parse_p_header(packet):
    header = packet[:20]  # 只取前 20 个字节，P 头部长度为 20 字节

    (
        version_ihl,
        tos,
        total_length,
        identifier,
        flags_fragment_offset,
        ttl,
        protocol,
        header_checksum,
        source_ip,
        dest_ip,
    ) = struct.unpack("!BBHHHBBH4s4s", header)

    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    priority = tos >> 5
    tos_flags = tos & 0x1F
    min_delay = tos_flags & 0x10
    max_throughput = tos_flags & 0x08
    high_reliability = tos_flags & 0x04
    min_cost = tos_flags & 0x02

    source_ip = socket.inet_ntoa(source_ip)
    dest_ip = socket.inet_ntoa(dest_ip)

    print("=== P Header Information ===")
    print(f"Version: {version}")
    print(f"IHL (Header Length): {ihl * 4} bytes")
    print(
        f"Service Type: {tos} (Priority: {priority}, Min Delay: {bool(min_delay)}, Max Throughput: {bool(max_throughput)}, High Reliability: {bool(high_reliability)}, Min Cost: {bool(min_cost)})"
    )
    print(f"Total Length: {total_length} bytes")
    print(f"Identifier: {identifier}")
    print(f"Flags+Fragment Offset: {flags_fragment_offset}")
    print(f"TTL (Time to Live): {ttl}")
    print(f"Protocol: {protocol}")
    print(f"Header Checksum: {header_checksum}")
    print(f"Source IP: {source_ip}")
    print(f"Destination IP: {dest_ip}")


# 捕获网络数据包
def capture_packets():
    # 创建原始套接字（需要管理员权限）
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    # 绑定到本地网络接口 (可以根据情况修改为具体的网络接口)
    sniffer.bind(("0.0.0.0", 0))

    # 接收所有 IP 包
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    try:
        # 捕获一个数据包
        raw_packet = sniffer.recvfrom(65565)[0]

        # 调用解析函数，传入捕获的数据包
        parse_p_header(raw_packet)

    except KeyboardInterrupt:
        print("Stopping packet capture...")


# 运行捕获函数
capture_packets()
