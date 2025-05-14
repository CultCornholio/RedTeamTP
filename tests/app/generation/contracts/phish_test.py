from app.generation.contracts.phish import contract
import pytest


def test_phish_contract_validation_successful():
    sanitized = contract.validate(
        {
            "op_number": "1234",
            "op_domain_name": "test.domain.com",
            "user_tag": "test-user-tag",
            "ttl": "2024-12-31",
            "phish_domains": ["login.office365.com", "portal.azure.com"],
            "redirect_url": "https://office.com",
            "github_user": "test",
            "github_ssh_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
            "o365_hostnames": {
                "www": "test-domain-www",
                "login": "test-domain-login",
                "aadcdn": "test-domain-aadcdn",
                "sso": "test-domain-sso"
            }
        }
    )

    assert sanitized == {
        "op_number": "1234",
        "op_domain_name": "test.domain.com",
        "user_tag": "test-user-tag",
        "ttl": "2024-12-31",
        "phish_domains": ["login.office365.com", "portal.azure.com"],
        "redirect_url": "https://office.com",
        "github_user": "test",
        "github_ssh_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
        "o365_hostnames": {
            "www": "test-domain-www",
            "login": "test-domain-login",
            "aadcdn": "test-domain-aadcdn",
            "sso": "test-domain-sso"
        }
    }


def test_phish_contract_validation_failure():
    with pytest.raises(Exception):
        contract.validate({})


def test_phish_contract_invalid_hostname():
    with pytest.raises(Exception):
        contract.validate({
            "op_number": "1234",
            "op_domain_name": "invalid hostname!@#",
            "user_tag": "test-user-tag",
            "ttl": "2024-12-31",
            "phish_domains": ["invalid!host", "also!invalid"],
            "redirect_url": "https://office.com",
            "github_user": "test",
            "github_ssh_keys": "ssh-key"
        })
