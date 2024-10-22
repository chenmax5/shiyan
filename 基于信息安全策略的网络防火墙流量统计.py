import struct
import socket


def parse_tcp_header(packet):
    # TCP 头部长度为最少 20 字节
    tcp_header = packet[:20]

    # 解析 TCP 头部
    (
        source_port,
        dest_port,
        seq_number,
        ack_number,
        data_offset_reserved_flags,
        flags,
        window_size,
        checksum,
        urgent_pointer,
    ) = struct.unpack("!HHLLBBHHH", tcp_header)

    # 提取头部长度 (data_offset: 高4位，表示头部长度，单位是4字节)
    data_offset = (data_offset_reserved_flags >> 4) * 4

    # 提取标志位
    urg = (flags & 0x20) >> 5
    ack = (flags & 0x10) >> 4
    psh = (flags & 0x08) >> 3
    rst = (flags & 0x04) >> 2
    syn = (flags & 0x02) >> 1
    fin = flags & 0x01

    print("=== TCP Header Information ===")
    print(f"Source Port: {source_port}")
    print(f"Destination Port: {dest_port}")
    print(f"Sequence Number: {seq_number}")
    print(f"Acknowledgment Number: {ack_number}")
    print(f"Header Length: {data_offset} bytes")
    print(f"Flags: URG={urg}, ACK={ack}, PSH={psh}, RST={rst}, SYN={syn}, FIN={fin}")
    print(f"Window Size: {window_size}")
    print(f"Checksum: {checksum}")
    print(f"Urgent Pointer: {urgent_pointer}\n")


def parse_udp_header(packet):
    # UDP 头部长度为 8 字节
    udp_header = packet[:8]

    # 解析 UDP 头部
    source_port, dest_port, length, checksum = struct.unpack("!HHHH", udp_header)

    print("=== UDP Header Information ===")
    print(f"Source Port: {source_port}")
    print(f"Destination Port: {dest_port}")
    print(f"Length: {length} bytes")
    print(f"Checksum: {checksum}\n")


def capture_packet():
    # 创建原始套接字（需要管理员权限）
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    # 绑定到本地网络接口 (可以根据情况修改为具体的网络接口)
    sniffer.bind(("0.0.0.0", 0))

    # 接收所有 IP 包
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    tcp_packet_captured = False
    udp_packet_captured = False

    try:
        while not (tcp_packet_captured and udp_packet_captured):
            # 捕获一个数据包
            raw_packet, addr = sniffer.recvfrom(65565)

            # IP 头部长度
            ip_header = raw_packet[:20]
            ip_proto = struct.unpack("!BBHHHBBH4s4s", ip_header)[6]

            # 判断协议类型
            if ip_proto == 6 and not tcp_packet_captured:  # TCP (protocol number 6)
                print("TCP packet captured:")
                parse_tcp_header(raw_packet[20:])  # 跳过IP头部，解析TCP头部
                tcp_packet_captured = True

            elif ip_proto == 17 and not udp_packet_captured:  # UDP (protocol number 17)
                print("UDP packet captured:")
                parse_udp_header(raw_packet[20:])  # 跳过IP头部，解析UDP头部
                udp_packet_captured = True

    except KeyboardInterrupt:
        print("Stopping packet capture...")

    finally:
        sniffer.close()


# 运行捕获函数，只捕获一个TCP和一个UDP数据包
capture_packet()
