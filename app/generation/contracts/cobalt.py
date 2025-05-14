from schema import Schema

from .validation_helpers import validate_hostname

contract = Schema(
    {
        "op_number": str,
        "op_domain_name": validate_hostname,
        "user_tag": str,
        "ttl": str,
        "cs_auth_header_name": str,
        "cs_auth_header_value": str,
        "cs_profile": str,
        "cdn_hostname": validate_hostname,
        "github_user": str,
        "github_ssh_keys": str,
    },
    ignore_extra_keys=True,
)
