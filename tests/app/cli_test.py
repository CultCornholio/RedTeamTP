from click.testing import CliRunner
import pytest
import os

from app.cli import generate


@pytest.fixture
def common_cli_options():
    """Common CLI options used across tests"""
    return [
        "--op-number",
        "1234",
        "--op-domain-name",
        "test.domain.com",
        "--user-tag",
        "test-opp-tag",
        "--ttl",
        "2024-12-31",
        "--github-user",
        "test",
        "--github-ssh-keys",
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
    ]


@pytest.fixture
def phish_cli_options():
    return [
        "--op-number",
        "1234",
        "--op-domain-name",
        "test.domain.com",
        "--user-tag",
        "test-phish-tag",
        "--ttl",
        "2024-12-31",
        "--phish-domains",
        "login.office365.com,portal.azure.com",
        "--redirect-url",
        "https://office.com",
        "--github-user",
        "test",
        "--github-ssh-keys",
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC",
    ]


def test_cobalt_generation(common_cli_options, tmp_dir):
    """Test Cobalt Strike configuration generation"""
    cs_options = [
        "--cs-auth-header-name",
        "test-header",
        "--cs-auth-header-value",
        "test-value",
        "--cs-profile",
        "test-profile",
        "--cdn-hostname",
        "cdn.test.com",
    ]

    runner = CliRunner()
    result = runner.invoke(
        generate,
        ["--type", "cobalt", *common_cli_options, *cs_options],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert fixture_matches_generated("cobalt", tmp_dir)


def test_cobalt_missing_required_options(common_cli_options):
    """Test Cobalt Strike missing required options"""
    runner = CliRunner()

    with pytest.raises(Exception) as exc_info:
        runner.invoke(
            generate,
            ["--type", "cobalt", *common_cli_options],  # Use common options directly
            catch_exceptions=False,
        )

    assert (
        "Schema validation error for 'cobalt' operation: "
        "Key 'cs_auth_header_name' "
        "error:\nNone should be instance of 'str'"
    ) in str(exc_info.value)


def test_phish_generation(phish_cli_options, tmp_dir):
    """Test phishing configuration generation"""
    runner = CliRunner()
    result = runner.invoke(
        generate, ["--type", "phish", *phish_cli_options], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert fixture_matches_generated("phish", tmp_dir)


def test_phish_missing_required_options(common_cli_options):
    """Test phishing missing required options"""
    runner = CliRunner()

    with pytest.raises(Exception) as exc_info:
        runner.invoke(
            generate,
            ["--type", "phish", *common_cli_options],  # Use common options directly
            catch_exceptions=False,
        )

    assert (
        "Schema validation error for 'phish' operation: "
        "Key 'phish_domains' "
        "error:\nNone should be instance of 'list'"
    ) in str(exc_info.value)


def fixture_matches_generated(name, tmp_dir):
    with open(f"{tmp_dir}/{name}.yml", "r") as f:
        generated_content = f.read()

    fixture_name = f"tests/fixtures/generated/{name}.yml"

    if os.environ.get("UPDATE_FIXTURES") == "true":
        with open(fixture_name, "w") as f:
            f.write(generated_content)

    with open(fixture_name, "r") as f:
        fixture_content = f.read()

    return generated_content == fixture_content
