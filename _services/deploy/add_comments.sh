#!/bin/bash

set -e

source "_services/common_functions.sh"

function add_comments {
    console_h1 "Adding comments to PR"

    local job_status=$1
    local op_number=$2

    # Search for the PR based on the naming convention
    local pr_number=$(gh pr list --search "config/$op_number" --json number -q ".[0].number")

    echo "PR Number: $pr_number"
    echo "Job Status: $job_status"
    echo "Operation Number: $op_number"

    if [ ! -z "$pr_number" ]; then
        if [ "$job_status" == "success" ]; then
            gh pr edit "$pr_number" --add-label "config/deployed"
            gh pr comment "$pr_number" --body "✅ Deployment successful for Operation $op_number
            - Timestamp: $(date -u)
            - Artifacts saved to workflow run"
        else
            gh pr edit "$pr_number" --add-label "config/deploy-failed"
            gh pr comment "$pr_number" --body "❌ Deployment failed for Operation $op_number
            - Timestamp: $(date -u)
            - Please check workflow logs for details"
        fi
    else
        echo "No matching PR found to update"
    fi
}

add_comments "$@"
