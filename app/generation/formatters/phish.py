import copy


class PhishFormatter(object):
    # Domain to phishlet mapping
    PHISHLET_MAPPING = {
        "login.office365.com": ["o365", "outlook"],
        "portal.azure.com": ["o365"],
        "outlook.office365.com": ["o365", "outlook"],
        "outlook.office.com": ["o365", "outlook"],
    }

    def __init__(self, inputs, template):
        self.inputs = inputs
        self.template = copy.deepcopy(template)

    def format(self):
        wc = self.template["warhorse"]
        inputs = self.inputs

        # Standard configuration updates
        wc["general"]["op_number"] = inputs["op_number"]
        wc["general"]["user_tag"] = inputs["user_tag"]
        wc["general"]["ttl"] = inputs["ttl"]
        wc["general"]["vault_key"] = "{{ vault_key }}"

        # Set domain variables properly
        full_domain = inputs["op_domain_name"]
        domain_parts = full_domain.split(".")
        base_domain = domain_parts[0]
        tld = ".".join(domain_parts[1:])  # Everything after first part

        # Update DNS configuration
        wc["dns"]["op_domain_name"] = full_domain
        wc["dns"]["op_tld"] = tld

        # Update hostnames using base domain
        o365_hostnames = {
            "www": f"{base_domain}-www",
            "login": f"{base_domain}-login",
            "aadcdn": f"{base_domain}-aadcdn",
            "sso": f"{base_domain}-sso",
        }

        # Update Evilginx2 configuration
        wc["vm"][0]["evilginx2"] = {
            "enabled": True,
            "evilginx_domain": "azureedge.net",
            "nginx_hostnames": list(o365_hostnames.values()),
            "cdn": [
                {"name": name, "provider": "azure", "hostname": hostname}
                for name, hostname in o365_hostnames.items()
            ],
            "o365": {
                "www_hostname": o365_hostnames["www"],
                "login_hostname": o365_hostnames["login"],
                "aadcdn_hostname": o365_hostnames["aadcdn"],
                "sso_hostname": o365_hostnames["sso"],
            },
            "phishlets": self._get_phishlets(inputs["phish_domains"]),
            "redirect_url": inputs["redirect_url"],
            "redirect_domain": inputs["redirect_url"]
            .replace("https://", "")
            .replace("http://", ""),
            "lures": [
                {
                    "name": "oauth",
                    "path": "/common/oauth2/v2.0",
                    "phishlet": "o365",
                    "redirect_url": "www.azure.com",
                }
            ],
        }

        # Update Terraform configuration
        wc["terraform"].update(
            {
                "state_bucket_key": f"{inputs['op_number']}/redteamtp",
            }
        )

        # Update users configuration
        wc["users"][0].update(
            {
                "username": inputs["github_user"],
                "name": inputs["github_user"].replace("-", " ").title(),
                "authorized_keys": [inputs["github_ssh_keys"]],
                "email": f"{inputs['github_user']}@github.com",
            }
        )

        return self.template

    def _get_phishlets(self, domains):
        """Convert input domains to evilginx2 phishlet names"""
        phishlets = set()  # Use set to avoid duplicates
        for domain in domains:
            if domain in self.PHISHLET_MAPPING:
                phishlets.update(self.PHISHLET_MAPPING[domain])
        return sorted(list(phishlets)) or [
            "o365",
            "outlook",
        ]  # Default to both phishlets
