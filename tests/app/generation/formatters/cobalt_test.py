from app.generation.formatters.cobalt import CobaltFormatter
import pytest

from app.configuration import Configuration


@pytest.fixture
def template():
    return Configuration.generation_persistence_adapter.find("cobalt")


def test_cobalt_config_factory_update(template):
    inputs = {
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

    formatter = CobaltFormatter(inputs, template)
    formatted_template = formatter.format()

    assert formatted_template["warhorse"]["general"]["op_number"] == "1234"
    assert formatted_template["warhorse"]["general"]["user_tag"] == "test-user-tag"
    assert formatted_template["warhorse"]["general"]["ttl"] == "2024-12-31"

    assert formatted_template["warhorse"]["dns"]["op_domain_name"] == "test.domain.com"

    assert (
        formatted_template["warhorse"]["vm"][0]["cobaltstrike"]["auth_header_name"]
        == "test-header-name"
    )
    assert (
        formatted_template["warhorse"]["vm"][0]["cobaltstrike"]["auth_header_value"]
        == "test-header-value"
    )
    assert (
        formatted_template["warhorse"]["vm"][0]["cobaltstrike"]["profile"]
        == "test-profile"
    )
    assert (
        formatted_template["warhorse"]["vm"][0]["cobaltstrike"]["cdn"][0]["hostname"]
        == "test.domain.com"
    )
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
