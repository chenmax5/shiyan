import logging
import argparse
from scapy.all import IP, TCP, UDP, ICMP, sr1

# 配置日志
logging.basicConfig(
    filename="scanner.log", level=logging.INFO, format="%(asctime)s %(message)s"
)


# 定义扫描器类
class NetworkScanner:
    def __init__(self, host, ports, scan_type):
        self.host = host
        self.ports = ports
        self.scan_type = scan_type

    # TCP SYN 扫描
    def tcp_syn_scan(self):
        for port in self.ports:
            pkt = IP(dst=self.host) / TCP(dport=port, flags="S")
            resp = sr1(pkt, timeout=1, verbose=0)
            if resp:
                if resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
                    logging.info(f"Port {port} is OPEN")
                    print(f"Port {port} is OPEN")
                elif resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x14:
                    logging.info(f"Port {port} is CLOSED")
                    print(f"Port {port} is CLOSED")
            else:
                logging.info(f"Port {port} is FILTERED or UNRESPONSIVE")
                print(f"Port {port} is FILTERED or UNRESPONSIVE")

    # UDP 扫描
    def udp_scan(self):
        for port in self.ports:
            pkt = IP(dst=self.host) / UDP(dport=port)
            resp = sr1(pkt, timeout=1, verbose=0)
            if resp is None:
                logging.info(f"Port {port} is OPEN or FILTERED")
                print(f"Port {port} is OPEN or FILTERED")
            elif resp.haslayer(ICMP):
                logging.info(f"Port {port} is CLOSED")
                print(f"Port {port} is CLOSED")

    # 开始扫描
    def scan(self):
        if self.scan_type == "tcp_syn":
            self.tcp_syn_scan()
        elif self.scan_type == "udp":
            self.udp_scan()
        else:
            print("Unsupported scan type")
            logging.error("Unsupported scan type")


# 处理命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="Simple Network Scanner")
    parser.add_argument("--host", required=True, help="Target host IP")
    parser.add_argument(
        "--ports", required=True, help="Port range to scan (e.g., 1-1024)"
    )
    parser.add_argument(
        "--scan",
        required=True,
        choices=["tcp_syn", "udp"],
        help="Scan type (tcp_syn or udp)",
    )
    args = parser.parse_args()
    return args


# 主函数
if __name__ == "__main__":
    args = parse_args()

    # 解析端口范围
    port_range = args.ports.split("-")
    ports = list(range(int(port_range[0]), int(port_range[1]) + 1))

    # 初始化并启动扫描
    scanner = NetworkScanner(args.host, ports, args.scan)
    scanner.scan()
