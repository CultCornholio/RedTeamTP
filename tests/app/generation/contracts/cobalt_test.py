from app.generation.contracts.cobalt import contract
import pytest


def test_cobalt_contract_validation_successful():
    sanitized = contract.validate(
        {
            "op_number": "1234",
            "op_domain_name": "test.domain.com",
            "user_tag": "test-user-tag",
            "ttl": "2024-12-31",
            "cs_auth_header_name": "test-header-name",
            "cs_auth_header_value": "test-header-value",
            "cs_profile": "test-profile",
            "cdn_hostname": "test.domain.com",
            "github_user": "test",
            "github_ssh_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
        }
    )

    assert sanitized == {
        "op_number": "1234",
        "op_domain_name": "test.domain.com",
        "user_tag": "test-user-tag",
        "ttl": "2024-12-31",
        "cs_auth_header_name": "test-header-name",
        "cs_auth_header_value": "test-header-value",
        "cs_profile": "test-profile",
        "cdn_hostname": "test.domain.com",
        "github_user": "test",
        "github_ssh_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
    }


def test_cobalt_contract_validation_failure():
    with pytest.raises(Exception):
        contract.validate({})
