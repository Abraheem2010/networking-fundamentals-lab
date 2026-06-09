"""Task 3 - IPv4 / CIDR subnet calculator.

Converts between dotted-decimal and integer IPv4 representations and, given a
CIDR block, computes the network address, broadcast address, host range, and
the number of hosts.
"""


def ip_to_int(ip):
    """
    dotted IPv4 -> 32-bit int
    """
    parts = ip.split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IP address format")
    ip_int = 0
    for part in parts:
        ip_int = (ip_int << 8) + int(part)
    return ip_int


def int_to_ip(n):
    """
    32-bit int -> dotted IPv4
    """
    parts = []
    for i in range(4):
        parts.append(str(n & 0xFF))
        n >>= 8
    return '.'.join(reversed(parts))


def cidr_to_mask(prefix_len):
    """
    prefix_len (0..32) -> 32-bit subnet mask as int
    """
    if prefix_len < 0 or prefix_len > 32:
        raise ValueError("Invalid prefix length")
    mask_int = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return mask_int


def parse_cidr(cidr_str):
    """
    parse 'a.b.c.d/p' -> (ip_int, mask_int, prefix_len_int)
    """
    ip_str, prefix_str = cidr_str.split('/')
    ip_int = ip_to_int(ip_str)
    prefix_len_int = int(prefix_str)
    mask_int = cidr_to_mask(prefix_len_int)
    return ip_int, mask_int, prefix_len_int


def network_info_from_cidr(cidr_str):
    """
    return dict with:
      - 'network'
      - 'broadcast'
      - 'first_host'
      - 'last_host'
      - 'hosts_count'
    """
    ip_int, mask_int, prefix_len_int = parse_cidr(cidr_str)
    network_int = ip_int & mask_int
    broadcast_int = (network_int | ~mask_int) & 0xFFFFFFFF
    first_host_int = network_int + 1
    last_host_int = broadcast_int - 1
    hosts_count = last_host_int - first_host_int + 1

    return {
        "network": int_to_ip(network_int),
        "broadcast": int_to_ip(broadcast_int),
        "first_host": int_to_ip(first_host_int),
        "last_host": int_to_ip(last_host_int),
        "hosts_count": hosts_count
    }


def main():
    """
    read CIDR from input, compute & print values
    """
    cidr_str = input("Enter CIDR notation (e.g., 192.168.1.0/24): ")
    info = network_info_from_cidr(cidr_str)
    for key, value in info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
