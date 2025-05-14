#!/bin/bash

set -e 

source "_services/common_functions.sh"

console_h1 "Installing Dependencies"

install_system_dependencies
install_terraform_and_vagrant
