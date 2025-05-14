#!/bin/bash

set -e 

source "_services/common_functions.sh"

function save_deployment_state {
    console_h1 "Saving deployment state"

    cd warhorse/OP/$OP_NUMBER/ && \
    mkdir -p state && \
    
    if [ -f "deploy.retry" ]; then
        cp deploy.retry state/
    fi

    echo "$(date -u)" > state/last_attempt
}


save_deployment_state