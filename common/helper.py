import unittest


def extract_data_package(data):
    # First determine the package length
    package_length_bytes = data[0:2]
    package_length = determine_package_length(package_length_bytes)
    # Get the complete data package
    data = data[2:package_length + 2]
    # Extract the command and the package
    command, payload = data[0:3], data[3:]
    return command, payload

def determine_package_length(chrs):
    assert len(chrs) == 2
    return ord(chrs[0]) * 16 + ord(chrs[1])


def calc_prefix_chars(length):
    a = length / 16
    b = length % 16
    prefix = chr(a) + chr(b)
    return prefix


def send_message(sock, message, udp_info):
    total_len = len(message)
    assert total_len <= 255

    prefix = calc_prefix_chars(total_len)

    sock.sendto(prefix+message, udp_info)

