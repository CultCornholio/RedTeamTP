function console_h1 {
    echo "==============================================================="
    echo -e "\033[34m$@\033[0m"
    echo "==============================================================="
}


function install_terraform_and_vagrant {
    console_h1 "Installing Terraform and Vagrant"

    sudo apt-get install -y gnupg software-properties-common curl

    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/hashicorp.gpg
    echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/hashicorp.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

    sudo apt-get update
    sudo apt-get install -y terraform vagrant
}

function install_system_dependencies {
    console_h1 "Installing System Dependencies"

    sudo apt-get update
    sudo apt-get install -y \
        zip \
        software-properties-common \
        ssh \
        make \
        unzip \
        expect
}

function setup_python_env {
    console_h1 "Setting up Python Environment"

    pip install --upgrade pip
    pip install ansible-core
    pip install bcrypt==4.0.1 cryptography>=41.0.0 paramiko>=3.3.1 pexpect
    pip install jinja2 ansible-lint argcomplete

    console_h1 "Cloning Workhorse"

    git clone https://github.com/almart/warhorse.git --depth 1 --branch main
    cd warhorse

    console_h1 "Configuring Ansible"

    # Setup Ansible roles and collections
    ansible-galaxy install -r requirements.yml -p roles/ --force
    ansible-galaxy collection install -r requirements.yml --force
    ansible-galaxy collection install community.general ansible.posix community.crypto

    # Setup vault
    chmod +x vault-env
}


function configure_aws_cli {
    console_h1 "Configuring AWS CLI"

    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID --profile $AWS_PROFILE
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY --profile $AWS_PROFILE
    aws configure set region us-east-1 --profile $AWS_PROFILE
    aws configure set output json --profile $AWS_PROFILE
    aws sts get-caller-identity
}

function configure_azure_cli {
    console_h1 "Configuring Azure CLI"

    az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
    az account set --subscription $AZURE_SUBSCRIPTION_ID
}