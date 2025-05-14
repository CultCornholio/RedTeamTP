#!/bin/bash

set -e 

source "_services/common_functions.sh"

console_h1 "Installing Dependencies"

function install_hashicorp_tools {
    console_h1 "Installing HashiCorp Tools"

    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | \
        sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
        https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
        sudo tee /etc/apt/sources.list.d/hashicorp.list
}


install_system_dependencies
install_hashicorp_tools
install_terraform_and_vagrant
