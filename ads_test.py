"""
BK9000 ADS Test - Raw socket ADS protocol

Findings:
- Port 100: Register access with IG=0, IO=register_address
- Port 300: Fieldbus data with IG=0xF020 for inputs
"""
import socket
import struct
from config import BK9000_IP

ADS_TCP_PORT = 48898
AMS_NET_ID = (10, 0, 0, 7, 1, 1)
SOURCE_NET_ID = (10, 0, 0, 1, 1, 1)

ADS_READ = 0x02


def build_ams_header(target_port, source_port, command_id, data_length):
    """Build AMS/TCP header"""
    ams_length = 32 + data_length
    tcp_header = struct.pack('<HI', 0, ams_length)

    target_netid = bytes(AMS_NET_ID)
    target_port_bytes = struct.pack('<H', target_port)
    source_netid = bytes(SOURCE_NET_ID)
    source_port_bytes = struct.pack('<H', source_port)

    command = struct.pack('<H', command_id)
    state_flags = struct.pack('<H', 0x0004)
    data_len = struct.pack('<I', data_length)
    error_code = struct.pack('<I', 0)
    invoke_id = struct.pack('<I', 1)

    ams_header = (target_netid + target_port_bytes +
                  source_netid + source_port_bytes +
                  command + state_flags + data_len + error_code + invoke_id)

    return tcp_header + ams_header


def ads_read(sock, target_port, index_group, index_offset, length):
    """Read data (Command 0x02)"""
    data = struct.pack('<III', index_group, index_offset, length)
    header = build_ams_header(target_port, 800, ADS_READ, len(data))

    sock.send(header + data)

    response = sock.recv(1024)
    if len(response) < 42:
        return None

    result = struct.unpack_from('<I', response, 38)[0]
    if result != 0:
        return {"error": result}

    data_len = struct.unpack_from('<I', response, 42)[0]
    data = response[46:46+data_len]
    return {"data": data}


def test_port_100_registers():
    """Test register access via ADS Port 100 with IG=0"""
    print("="*60)
    print("ADS Port 100 - Register Access (IG=0, IO=register)")
    print("="*60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((BK9000_IP, ADS_TCP_PORT))

    # Test with IG=0, IO=register address
    test_reads = [
        (0x1000, 16, "Coupler Info"),
        (0x1010, 16, "I/O Config Table"),
        (0x1012, 2, "Digital Outputs Count"),
        (0x1013, 2, "Digital Inputs Count"),
        (0x1120, 2, "Watchdog Timeout"),
        (0x1122, 2, "Watchdog Mode"),
    ]

    print("\nUsing IG=0, IO=register_address:\n")

    for offset, length, desc in test_reads:
        result = ads_read(sock, 100, 0, offset, length)
        if result and "data" in result:
            data = result["data"]
            hex_str = data.hex()
            if len(data) == 2:
                value = struct.unpack('<H', data)[0]
                print(f"  0x{offset:04X} ({desc}): {hex_str} = {value}")
            else:
                # Try to decode as ASCII
                try:
                    ascii_val = data.decode('ascii', errors='replace').replace('\x00', ' ')
                    print(f"  0x{offset:04X} ({desc}): {hex_str}")
                    print(f"         ASCII: {ascii_val}")
                except:
                    print(f"  0x{offset:04X} ({desc}): {hex_str}")
        else:
            print(f"  0x{offset:04X} ({desc}): Error {result}")

    # Scan more registers
    print("\nScanning register range 0x1000-0x1030:\n")
    for offset in range(0x1000, 0x1030, 2):
        result = ads_read(sock, 100, 0, offset, 2)
        if result and "data" in result:
            data = result["data"]
            value = struct.unpack('<H', data)[0]
            if value != 0:  # Only show non-zero values
                print(f"  0x{offset:04X}: {value} (0x{value:04X})")

    sock.close()


def test_port_300_io():
    """Test I/O access via ADS Port 300"""
    print("\n" + "="*60)
    print("ADS Port 300 - Fieldbus I/O Data")
    print("="*60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((BK9000_IP, ADS_TCP_PORT))

    # According to Beckhoff docs for Port 300:
    # 0xF020 = Inputs, 0xF030 = Outputs
    test_reads = [
        (0xF020, 0, 8, "Inputs (0xF020, offset 0)"),
        (0xF020, 0, 24, "All 24 Inputs"),
        (0xF030, 0, 8, "Outputs (0xF030, offset 0)"),
        (0xF030, 0, 20, "All 20 Outputs"),

        # Try IG=0
        (0, 0, 8, "IG=0, IO=0"),
        (0, 0xF020, 8, "IG=0, IO=0xF020"),
    ]

    for ig, io, length, desc in test_reads:
        result = ads_read(sock, 300, ig, io, length)
        if result and "data" in result:
            data = result["data"]
            print(f"  {desc}: {data.hex()}")
            # Interpret as bits for I/O
            if len(data) >= 3:
                bits = ''.join(format(b, '08b')[::-1] for b in data)
                print(f"         Bits: {bits[:24]}")
        else:
            print(f"  {desc}: Error {result}")

    sock.close()


def test_terminal_info():
    """Try to get terminal/module information via ADS"""
    print("\n" + "="*60)
    print("Testing Terminal Information Access")
    print("="*60)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((BK9000_IP, ADS_TCP_PORT))

    # Try terminal register access
    # According to docs, 0x4xxx should be terminal registers
    print("\nTrying Port 100, IG=0, Terminal offsets:\n")

    for term in range(1, 12):
        # Try 0x4000 + terminal number
        offset = 0x4000 + term
        result = ads_read(sock, 100, 0, offset, 8)
        if result and "data" in result:
            print(f"  Terminal {term} (0x{offset:04X}): {result['data'].hex()}")
        else:
            print(f"  Terminal {term} (0x{offset:04X}): No data")

    sock.close()


if __name__ == "__main__":
    test_port_100_registers()
    test_port_300_io()
    test_terminal_info()
