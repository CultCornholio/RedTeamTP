import copy


class CobaltFormatter(object):
    def __init__(self, inputs, template):
        self.inputs = inputs
        self.template = copy.deepcopy(template)

    def format(self):
        wc = self.template["warhorse"]
        inputs = self.inputs

        wc["general"]["op_number"] = inputs["op_number"]
        wc["general"]["user_tag"] = inputs["user_tag"]
        wc["general"]["ttl"] = inputs["ttl"]

        # Set domain variables properly
        full_domain = inputs["op_domain_name"]
        domain_parts = full_domain.split(".")
        tld = ".".join(domain_parts[1:])  # Everything after first part

        # Update DNS configuration
        wc["dns"]["op_domain_name"] = full_domain
        wc["dns"]["op_tld"] = tld

        wc["vm"][0]["cobaltstrike"]["auth_header_name"] = inputs["cs_auth_header_name"]
        wc["vm"][0]["cobaltstrike"]["auth_header_value"] = inputs[
            "cs_auth_header_value"
        ]
        wc["vm"][0]["cobaltstrike"]["profile"] = inputs["cs_profile"]
        wc["vm"][0]["cobaltstrike"]["cdn"][0]["hostname"] = inputs["cdn_hostname"]
        wc["terraform"]["state_bucket_key"] = f"{inputs['op_number']}/redteamtp"

        wc["users"][0]["username"] = inputs["github_user"]
        wc["users"][0]["name"] = inputs["github_user"].replace("-", " ").title()
        wc["users"][0]["authorized_keys"] = [inputs["github_ssh_keys"]]
        wc["users"][0]["shell"] = "/usr/bin/zsh"
        wc["users"][0]["email"] = f"{inputs['github_user']}@github.com"

        return self.template
