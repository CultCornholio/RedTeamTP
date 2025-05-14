"""Command line interface for RedTeam Infrastructure Tool"""

import click
from app.generation.services.generation_service import GenerationService
from schema import SchemaError
from app.configuration import Configuration


@click.group()
def cli():
    """Red Team Infrastructure Configuration Tool"""
    pass


@cli.command("generate")
@click.option(
    "--type",
    "-t",
    required=True,
    type=click.Choice(["cobalt", "phish"]),
    help="Type of configuration to generate",
)
@click.option("--op-number", required=True, help="Operation number")
@click.option("--op-domain-name", required=True, help="Domain name for operation")
@click.option("--user-tag", required=True, help="Operator tag")
@click.option("--ttl", required=True, help="Infrastructure TTL (YYYY-MM-DD)")
# Cobalt Strike specific options
@click.option(
    "--cs-auth-header-name", help="Cobalt Strike auth header name", required=False
)
@click.option(
    "--cs-auth-header-value", help="Cobalt Strike auth header value", required=False
)
@click.option("--cs-profile", help="Cobalt Strike profile name", required=False)
@click.option(
    "--cdn-hostname",
    help="Azure CDN hostname (required for Cobalt Strike only)",
    required=False,
)
# Phishing specific options
@click.option(
    "--phish-domains",
    help="Comma-separated list of phishing domains",
    required=False,
    callback=lambda ctx, param, value: value.split(",") if value else None,
    type=str,
)
@click.option(
    "--redirect-url", help="URL to redirect after phishing", required=False, type=str
)
# Common options
@click.option("--github-user", help="GitHub user", required=True)
@click.option("--github-ssh-keys", help="GitHub SSH keys", required=True)
def generate(**options):
    """Generate infrastructure configuration"""
    Configuration.validate()

    operation = options.pop("type")

    try:
        GenerationService.generate_with(operation=operation, inputs=options)
    except SchemaError as err:
        raise Exception(f"Schema validation error for '{operation}' operation: {err}")


@cli.command("help")
@click.argument("command", required=False, type=click.Choice(["generate"]))
def help_command(command):
    """Show extended help for a command"""
    if command == "generate":
        click.echo("Usage: redteamtp generate [OPTIONS]")
        click.echo("")
        click.echo("  Generate infrastructure configuration")
        click.echo("")
        click.echo("Options:")
        click.echo(
            "  -t, --type [cobalt|phish]  Type of configuration to generate (required)"
        )
        click.echo("  --op-number TEXT           Operation number (required)")
        click.echo("  --op-domain-name TEXT      Domain name for operation (required)")
        click.echo("  --user-tag TEXT            Operator tag (required)")
        click.echo(
            "  --ttl TEXT                 Infrastructure TTL (YYYY-MM-DD) (required)"
        )
        click.echo("")
        click.echo("  Cobalt Strike Options:")
        click.echo("    --cs-auth-header-name TEXT   Cobalt Strike auth header name")
        click.echo("    --cs-auth-header-value TEXT  Cobalt Strike auth header value")
        click.echo("    --cs-profile TEXT            Cobalt Strike profile name")
        click.echo(
            "    --cdn-hostname TEXT          Azure CDN hostname (required for Cobalt Strike only)"
        )
        click.echo("")
        click.echo("  Phishing Options:")
        click.echo(
            "    --phish-domains TEXT       Comma-separated list of phishing domains"
        )
        click.echo("    --redirect-url TEXT          URL to redirect after phishing")
        click.echo("")
        click.echo("  Common Options:")
        click.echo("    --github-user TEXT           GitHub user (required)")
        click.echo("    --github-ssh-keys TEXT       GitHub SSH keys (required)")
        click.echo("")
        click.echo("Example:")
        click.echo(
            "redteamtp generate --type cobalt "
            "--op-number OP123 --op-domain-name test.com "
            "--user-tag test --ttl 2024-12-31 "
            "--cs-auth-header-name auth --cs-auth-header-value value "
            "--cs-profile profile.4.5 --cdn-hostname cdn.test.com "
            '--github-user testuser --github-ssh-keys "ssh-rsa AAA..."'
        )
    else:
        click.echo("Available commands: generate")
