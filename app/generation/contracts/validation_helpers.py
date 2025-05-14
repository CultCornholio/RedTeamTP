import re
import ipaddress


def validate_ip(ip_str: str) -> bool:
    """Validate IP address format."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def validate_hostname(hostname: str) -> bool:
    """Validate hostname format."""
    if len(hostname) > 255:
        return False
    pattern = r"^[a-zA-Z0-9][-a-zA-Z0-9.]*[a-zA-Z0-9]$"
    return bool(re.match(pattern, hostname))


def validate_port(port: str) -> bool:
    """Validate port number."""
    try:
        port_num = int(port)
        return 0 <= port_num <= 65535
    except ValueError:
        return False
