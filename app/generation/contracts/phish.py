from schema import Schema, And, Optional
from .validation_helpers import validate_hostname

contract = Schema(
    {
        "op_number": str,
        "op_domain_name": validate_hostname,
        "user_tag": str,
        "ttl": str,
        "phish_domains": And(list, lambda x: all(isinstance(h, str) for h in x)),
        "redirect_url": str,
        "github_user": str,
        "github_ssh_keys": str,
        Optional("o365_hostnames"): {
            "www": validate_hostname,
            "login": validate_hostname,
            "aadcdn": validate_hostname,
            "sso": validate_hostname
        }
    },
    ignore_extra_keys=True,
)
