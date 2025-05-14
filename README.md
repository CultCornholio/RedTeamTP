```ascii
╔══════════════════════ CULT CORNHOLIO RED TEAM TP ══════════════════════╗
║     ⣀⣀⣤⣤⣴⣶⣶⣶⣶⣦⣤⣤⣀⣀⠀           ARE YOU THREATENING ME?!        ║
║   ⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄    I NEED TP FOR MY RED TEAM!       ║
║  ⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣆                               ║
║ ⢠⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⡀    [Deploying C2...]         ║
║ ⣾⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿          ┣━━━━━━━ 45%     ║
║ ⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿                               ║
║ ⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿    [Deploying Redirectors..]║
║ ⢸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇          ┣━━━━━━━ 67%     ║
║ ⠘⢿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡿⠃                               ║
║  ⠈⠻⢿⣿⣿⣿⣷⣤⣤⣤⣤⣤⣤⣤⣤⣴⣾⠟⠁      [Starting Evilginx...]     ║
║    ⠉⠛⠻⠿⣿⣿⣿⣿⣿⠿⠟⠉            ┣━━━━━━━ 89%             ║
║       ⠈⠉⠛⠛⠛⠛⠋⠉                                              ║
╚═════════════════════ Infrastructure Deployment ═════════════════════╝
```

# Red Team Infrastructure Deployment

CI/CD automated red team infrastructure deployment using GitHub Actions.

*Building upon the foundation laid by [Ralph May WarHorse](https://github.com/warhorse/warhorse)*

## About This Project

This toolkit provides automated deployment of red team infrastructure through GitHub Actions workflows. It supports configurable C2 frameworks and phishing operations with a focus on secure, repeatable deployments.

## Key Features

- **Infrastructure Types**
  - C2 Infrastructure
    - Cobalt Strike (with CDN redirectors)
    - Mythic Framework (experimental)
  - Phishing Infrastructure (Evilginx2 + GoPhish)
  - Multi-Cloud Support
    - DigitalOcean (primary compute)
    - AWS (CDN/redirectors)
    - Azure (CDN/redirectors)

- **Core Features**
  - Template-Based Configuration Generation
  - Infrastructure as Code (Terraform)
  - Ansible Deploy/Destroy
  - Automated DNS Management
  - SSL/TLS Configuration
  - GitHub Actions Workflows Manages Infrastructure Lifecycle
  - Collobrative Infrastructure Management via Labels/Commits

## Quick Start

1. Fork this repository
2. Configure required GitHub secrets (see Configuration section)
3. Use GitHub Actions workflows to manage your infrastructure:
   - **Generate**: Creates and validates infrastructure configuration
   - **Deploy**: Provisions and configures infrastructure based on templates
   - **Destroy**: Safely tears down infrastructure when complete

## Available Workflows

### 1. Generate Configuration

- **Cobalt Strike**: `.github/workflows/generate-cobalt.yml`
  ```yaml
  # Required inputs:
  - operation_number      # Unique identifier for the operation
  - domain                # Domain for the C2 infrastructure
  - user_tag              # Tag for the operator
  - expiry                # Infrastructure TTL (YYYY-MM-DD)
  - cs_profile            # Cobalt Strike profile name
  - cs_auth_header_name   # Authentication header name
  - cs_auth_header_value  # Authentication header value
  - cdn_hostname          # Azure CDN hostname
  ```

- **Phishing**: `.github/workflows/generate-phish.yml`
  ```yaml
  # Required inputs:
  - op_number             # Operation number
  - op_domain_name        # Domain for phishing infrastructure
  - user_tag              # Tag for the operator
  - ttl                   # Infrastructure TTL (YYYY-MM-DD)
  - phish_domains         # Target phishing domains (comma-separated)
  - redirect_url          # Post-phishing redirect URL
  ```

### 2. Deploy Infrastructure

We have specialized deployment workflows for different infrastructure types:

- **Cobalt Strike**: `.github/workflows/deploy-cobalt.yml`
- **Phishing**: `.github/workflows/deploy-phish.yml`

These workflows are triggered automatically on configuration PRs or can be manually invoked with:

```yaml
# Required inputs for manual dispatch:
- repo                    # Repository containing configuration
- op_number               # Operation number
- dry_run                 # Whether to perform a dry run (optional)
```

![Cornholion in Holy Cornholio](https://upload.wikimedia.org/wikipedia/en/5/56/Cornholion_in_Holy_Cornholio.jpg)

### 3. Destroy Infrastructure

The `.github/workflows/destroy.yml` workflow handles infrastructure teardown and can be triggered:
- Automatically when configuration PRs are closed
- Manually through workflow dispatch

```yaml
# Required inputs for manual dispatch:
- repo                    # Operation tag (e.g., cs-1111)
- op_number               # Operation number from deployment
```

![Drones (Beavis and Butt-Head)](https://upload.wikimedia.org/wikipedia/en/6/64/Drones_B_and_B.jpg)

## CLI Usage

The project also provides a command-line interface for local configuration generation:

```bash
# Generate Cobalt Strike configuration
./bin/cli generate --type cobalt \
  --op-number "OP001" \
  --op-domain-name "example.com" \
  --user-tag "operator1" \
  --ttl "2024-12-31" \
  --cs-auth-header-name "Authorization" \
  --cs-auth-header-value "Bearer XXXX" \
  --cs-profile "amazon" \
  --cdn-hostname "cdn.example.com" \
  --github-user "username" \
  --github-ssh-keys "ssh-rsa AAA..."

# Generate Phishing configuration
./bin/cli generate --type phish \
  --op-number "OP001" \
  --op-domain-name "phish.example.com" \
  --user-tag "operator1" \
  --ttl "2024-12-31" \
  --phish-domains "login.office365.com,portal.azure.com" \
  --redirect-url "https://office.com" \
  --github-user "username" \
  --github-ssh-keys "ssh-rsa AAA..."
```

## Required Configuration

### GitHub Secrets

#### Core Infrastructure
```yaml
DO_API_TOKEN: "DigitalOcean API token"
ANSIBLE_VAULT_PASSWORD: "Ansible vault encryption key"
BUCKET_ACCESS_KEY: "S3 bucket access"
BUCKET_SECRET_KEY: "S3 bucket secret"
CS_PASSWORD: "Cobalt Strike password" # For Cobalt Strike deployment
CS_LICENSE_KEY: "Cobalt Strike license key" # For Cobalt Strike deployment
```

#### AWS Configuration
```yaml
AWS_ACCESS_KEY_ID: "AWS API access key"
AWS_SECRET_ACCESS_KEY: "AWS API secret key"
```

#### Azure Configuration
```yaml
AZURE_TENANT_ID: "Azure tenant ID"
AZURE_CLIENT_ID: "Azure client ID" 
AZURE_CLIENT_SECRET: "Azure client secret"
AZURE_SUBSCRIPTION_ID: "Azure subscription ID"
```

## Development Guide

### Local Testing

1. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest tests/
```

### Project Structure

```
.
├── app/                   # Core application code
│   ├── generation/        # Config generation logic
│   │   ├── config_updaters/  # Template updaters for each infrastructure type
│   │   ├── contracts/     # Input validation contracts
│   │   └── services/     # Service layer for generation
│   └── cli.py            # CLI interface
├── templates/             # Infrastructure templates
│   └── warhorse/         # Base templates for different infrastructure types
├── _services/             # Deployment and operation scripts
│   ├── deploy/           # Deployment scripts
│   │   ├── cobalt/       # Cobalt Strike deployment 
│   │   └── phish/        # Phishing deployment
│   ├── destroy/          # Infrastructure teardown scripts
│   └── common_functions.sh # Shared Bash functions
├── generated/            # Output directory for generated configurations
├── tests/                # Test suite
└── .github/workflows/    # GitHub Actions definitions
```

### Adding New Features

1. Create feature branch
2. Add tests in `tests/` directory
3. Implement feature
4. Update templates if needed
5. Submit PR with workflow test results

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
