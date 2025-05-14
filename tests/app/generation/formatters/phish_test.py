from app.generation.formatters.phish import PhishFormatter
import pytest

from app.configuration import Configuration


@pytest.fixture
def template():
    return Configuration.generation_persistence_adapter.find("phish")


def test_phish_config_factory_update(template):
    inputs = {
        "op_number": "1234",
        "op_domain_name": "test.domain.com",
        "user_tag": "test-user-tag",
        "ttl": "2024-12-31",
        "phish_domains": ["login.office365.com", "portal.azure.com"],
        "redirect_url": "https://office.com",  # Will be transformed to just "office.com"
        "github_user": "test",
        "github_ssh_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
    }

    formatter = PhishFormatter(inputs, template)
    formatted_template = formatter.format()

    # Test general configuration
    assert formatted_template["warhorse"]["general"]["op_number"] == "1234"
    assert formatted_template["warhorse"]["general"]["user_tag"] == "test-user-tag"
    assert formatted_template["warhorse"]["general"]["ttl"] == "2024-12-31"

    # Test DNS configuration
    assert formatted_template["warhorse"]["dns"]["op_domain_name"] == "test.domain.com"
    assert formatted_template["warhorse"]["dns"]["op_tld"] == "domain.com"

    # Test Evilginx configuration with phishlets
    vm_config = formatted_template["warhorse"]["vm"][0]
    assert vm_config["evilginx2"]["phishlets"] == ["o365", "outlook"]

    # Test Evilginx configuration with domain-only redirect
    assert (
        vm_config["evilginx2"]["redirect_domain"] == "office.com"
    )  # Just the domain, no protocol

    # Test O365 hostnames and CDN configuration
    domain_base = inputs["op_domain_name"].split(".")[0]  # Should be "test"
    expected_hostnames = [
        f"{domain_base}-www",
        f"{domain_base}-login",
        f"{domain_base}-aadcdn",
        f"{domain_base}-sso",
    ]

    # Test nginx hostnames
    assert vm_config["evilginx2"]["nginx_hostnames"] == expected_hostnames

    # Test CDN configuration
    expected_cdn = [
        {"name": "www", "provider": "azure", "hostname": f"{domain_base}-www"},
        {"name": "login", "provider": "azure", "hostname": f"{domain_base}-login"},
        {"name": "aadcdn", "provider": "azure", "hostname": f"{domain_base}-aadcdn"},
        {"name": "sso", "provider": "azure", "hostname": f"{domain_base}-sso"},
    ]
    assert vm_config["evilginx2"]["cdn"] == expected_cdn

    # Test O365 hostnames
    assert vm_config["evilginx2"]["nginx_hostnames"] == expected_hostnames
    assert vm_config["evilginx2"]["o365"]["www_hostname"] == f"{domain_base}-www"
    assert vm_config["evilginx2"]["o365"]["login_hostname"] == f"{domain_base}-login"
    assert vm_config["evilginx2"]["o365"]["aadcdn_hostname"] == f"{domain_base}-aadcdn"
    assert vm_config["evilginx2"]["o365"]["sso_hostname"] == f"{domain_base}-sso"

    # Test terraform configuration
    assert (
        formatted_template["warhorse"]["terraform"]["state_bucket_key"]
        == "1234/redteamtp"
    )

    # Test user configuration
    assert formatted_template["warhorse"]["users"][0]["username"] == "test"
    assert formatted_template["warhorse"]["users"][0]["name"] == "Test"
    assert formatted_template["warhorse"]["users"][0]["authorized_keys"] == [
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC"
    ]
    assert formatted_template["warhorse"]["users"][0]["email"] == "test@github.com"
