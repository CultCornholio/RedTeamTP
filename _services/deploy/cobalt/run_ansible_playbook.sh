#!/bin/bash

set -e 

source "_services/common_functions.sh"

function run_ansible_playbook {
    console_h1 "Running Ansible Playbook"

    cd warhorse && \
    ansible-playbook generate.yml -v \
    --vault-password-file <(echo "$VAULT_KEY") \
    -e @../generated/cobalt.yml \
    -e "op_base_dir=$(pwd)" \
    -e "bucket_access_key=${BUCKET_ACCESS_KEY}" \
    -e "bucket_secret_key=${BUCKET_SECRET_KEY}" \
    -e "do_token=${DO_TOKEN}" \
    -e "cs_password=${CS_PASSWORD}" \
    -e "cs_key=${CS_KEY}" \
    -e "subscription_id=${SUBSCRIPTION_ID}" \
    -e "ansible_ssh_private_key_file=${SSH_PRIVATE_KEY_FILE}" \
    -e "ssh_passphrase=${SSH_PASSPHRASE}"

    # Deploy step (staying in the same shell context)
    cd OP/$OP_NUMBER && \
    export TERRAFORM_PATH="$(pwd)/terraform"
    
    attempt=1
    max_attempts=$MAX_RETRIES
    until ansible-playbook deploy.yml \
    --vault-password-file <(echo "$ANSIBLE_VAULT_PASSWORD") \
    -i inventory/ \
    -e "bucket_access_key=${BUCKET_ACCESS_KEY}" \
    -e "terraform_path=${TERRAFORM_PATH}" \
    -e "bucket_secret_key=${BUCKET_SECRET_KEY}" \
    -e "digitalocean_token=${DO_TOKEN}" \
    -e "cs_password=${CS_PASSWORD}" \
    -e "cs_key=${CS_KEY}" \
    -e "terraform_project_path=$(pwd)" \
    -e "subscription_id=${SUBSCRIPTION_ID}" \
    -e "ansible_ssh_private_key_file=${SSH_PRIVATE_KEY_FILE}" \
    -e "ssh_passphrase=${SSH_PASSPHRASE}" \
    -e "ansible_ssh_retries=10" \
    -e "ansible_connection_timeout=60" \
    -e "ansible_connect_timeout=60" \
    -v --force-handlers --timeout=30; do
    if [ $attempt -ge $max_attempts ]; then
        console_h1 "Failed after $max_attempts attempts. Exiting..."
        exit 1
    fi
    console_h1 "Attempt $attempt failed. Waiting ${RETRY_DELAY}s before retry..."
    attempt=$((attempt + 1))
    sleep $RETRY_DELAY
    # Check for any retry files and use them
    if [ -f "deploy.retry" ]; then
        echo "Found retry file, targeting failed hosts..."
        ansible-playbook deploy.yml \
        --vault-password-file <(echo "$ANSIBLE_VAULT_PASSWORD") \
        -e @deploy.retry \
        --limit @deploy.retry \
        -vv --force-handlers --timeout=30
    fi
    done

    console_h1 "Deployment completed successfully"
}

run_ansible_playbook
