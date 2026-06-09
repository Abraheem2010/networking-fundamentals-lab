"""Task 1 - Round-Trip Time (RTT) probe over TCP or UDP.

Sends a series of messages to an echo server, measures the RTT of each
message, and prints the per-message RTT together with the average.
"""
import argparse
import socket
import time


def make_socket(protocol, timeout_sec):
    """
    protocol: "tcp" or "udp"
    return an initialized socket with timeout set to timeout_sec seconds
    """
    if protocol == "tcp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
    elif protocol == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
    else:
        raise ValueError("Invalid protocol. Use 'tcp' or 'udp'.")
    sock.settimeout(timeout_sec)
    return sock


def send_and_time(sock, server_addr, payload):
    """
    send payload, wait for echo, measure RTT using time.time()
    return measured_rtt_seconds (float)
    """
    start_time = time.time()  # Record the start time
    if isinstance(sock, socket.socket) and sock.type == socket.SOCK_STREAM:  # TCP
        sock.sendall(payload)  # Send payload
        response = sock.recv(1024)  # Wait for echo
    elif isinstance(sock, socket.socket) and sock.type == socket.SOCK_DGRAM:  # UDP
        sock.sendto(payload, server_addr)  # Send payload
        response, _ = sock.recvfrom(1024)  # Wait for echo
    else:
        raise ValueError("Invalid socket type.")
    end_time = time.time()  # Record the end time
    rtt = end_time - start_time  # Calculate RTT
    return rtt


def run_rtt_probe(server_host, server_port, protocol="tcp", count=10, timeout_sec=2.0):
    """
    create socket, loop count times, measure per-message RTTs,
    print each RTT and the average at the end
    """
    if protocol == "tcp":
        sock = make_socket(protocol, timeout_sec)  # Create TCP socket
        sock.connect((server_host, server_port))  # Connect to server
    elif protocol == "udp":
        sock = make_socket(protocol, timeout_sec)  # Create UDP socket
    else:
        raise ValueError("Invalid protocol. Use 'tcp' or 'udp'.")
    server_addr = (server_host, server_port)  # Server address
    rtts = []  # List to store RTTs

    for i in range(count):
        payload = f"Message {i}".encode()  # Create payload
        try:
            rtt = send_and_time(sock, server_addr, payload)  # Measure RTT
            rtts.append(rtt)  # Store RTT
            print(f"RTT for message {i}: {rtt:.4f} seconds")  # Print RTT
        except socket.timeout:
            print(f"Timeout for message {i}")  # Handle timeout

    if rtts:
        average_rtt = sum(rtts) / len(rtts)  # Calculate average RTT
        print(f"Average RTT: {average_rtt:.4f} seconds")  # Print average RTT
    else:
        print("No successful RTT measurements.")  # No successful measurements
    sock.close()  # Close socket
    return rtts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Measure round-trip time (RTT) to an echo server over TCP or UDP."
    )
    parser.add_argument("--host", default="127.0.0.1",
                        help="server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000,
                        help="server port (default: 5000)")
    parser.add_argument("--protocol", choices=["tcp", "udp"], default="tcp",
                        help="transport protocol (default: tcp)")
    parser.add_argument("--count", type=int, default=10,
                        help="number of messages to send (default: 10)")
    parser.add_argument("--timeout", type=float, default=2.0,
                        help="socket timeout in seconds (default: 2.0)")
    args = parser.parse_args()

    run_rtt_probe(args.host, args.port, protocol=args.protocol,
                  count=args.count, timeout_sec=args.timeout)
