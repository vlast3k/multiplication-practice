# BTP CLI Setup and Management Skill

## Overview

This skill provides comprehensive guidance for using the SAP BTP Command Line Interface (btp CLI) to manage SAP BTP accounts, subaccounts, entitlements, and services.

## Prerequisites

- SAP BTP Global Account
- User with appropriate permissions (Global Account Administrator or Subaccount Administrator)
- btp CLI installed

---

## Installation

### Check if btp CLI is Installed

```bash
btp --version
```

### Install btp CLI

#### Linux / macOS

```bash
# Download latest version
curl -LO https://tools.hana.ondemand.com/additional/btp-cli-linux-amd64.tar.gz

# Extract
tar -xzf btp-cli-linux-amd64.tar.gz

# Move to /usr/local/bin
sudo mv linux-amd64/btp /usr/local/bin/

# Verify installation
btp --version
```

#### Windows

```powershell
# Download from SAP
# https://tools.hana.ondemand.com/additional/btp-cli-windows-amd64.zip

# Extract and add to PATH
# Or use chocolatey:
choco install sap-btp-cli
```

#### Alternative: Use npm package

```bash
npm install -g @sap/btp-cli
```

---

## Authentication and Login

### Login to BTP

```bash
# Interactive login
btp login

# Login with specific global account
btp login --subdomain <your-subdomain>

# Login with SSO
btp login --sso

# Login with specific region
btp login --url https://cli.btp.cloud.sap/
```

### Check Current Login

```bash
# Show current context
btp target

# List available global accounts
btp list accounts/global-account
```

### Logout

```bash
btp logout
```

---

## Global Account Management

### View Global Account Details

```bash
# Get global account info
btp get accounts/global-account

# Get global account with details
btp get accounts/global-account --show-hierarchy
```

### List Directories

```bash
# List all directories in global account
btp list accounts/directory

# Get specific directory
btp get accounts/directory <directory-id>
```

---

## Subaccount Management

### List Subaccounts

```bash
# List all subaccounts
btp list accounts/subaccount

# List subaccounts in a directory
btp list accounts/subaccount --directory <directory-id>

# List with details
btp list accounts/subaccount --show-hierarchy
```

### Create Subaccount

```bash
# Create subaccount
btp create accounts/subaccount \
  --display-name "My Subaccount" \
  --subdomain "my-subaccount" \
  --region "us10" \
  --description "Development environment"

# Create subaccount in a directory
btp create accounts/subaccount \
  --display-name "Dev Subaccount" \
  --subdomain "dev-subaccount" \
  --region "us10" \
  --directory <directory-id>

# Create with beta features enabled
btp create accounts/subaccount \
  --display-name "Beta Subaccount" \
  --subdomain "beta-subaccount" \
  --region "us10" \
  --beta-enabled true
```

### Available Regions

Common regions:
- `us10` - US East (VA)
- `us20` - US West (WA)
- `us21` - US East (VA) - AWS
- `eu10` - Europe (Frankfurt)
- `eu20` - Europe (Netherlands)
- `ap10` - Australia (Sydney)
- `ap11` - Singapore
- `ap21` - Singapore - AWS
- `jp10` - Japan (Tokyo)

### Update Subaccount

```bash
# Update display name
btp update accounts/subaccount <subaccount-id> \
  --display-name "New Name"

# Update description
btp update accounts/subaccount <subaccount-id> \
  --description "Updated description"

# Enable beta features
btp update accounts/subaccount <subaccount-id> \
  --beta-enabled true
```

### Delete Subaccount

```bash
# Delete subaccount
btp delete accounts/subaccount <subaccount-id>

# Force delete without confirmation
btp delete accounts/subaccount <subaccount-id> --confirm
```

### Get Subaccount Details

```bash
# Get subaccount info
btp get accounts/subaccount <subaccount-id>

# Get with hierarchy
btp get accounts/subaccount <subaccount-id> --show-hierarchy
```

---

## Entitlements Management

### List Entitlements

```bash
# List all entitlements for global account
btp list accounts/entitlement

# List entitlements for specific subaccount
btp list accounts/entitlement --subaccount <subaccount-id>

# List available services
btp list accounts/available-environment

# List available service plans
btp list accounts/available-plan
```

### Assign Entitlements to Subaccount

```bash
# Assign entitlement
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service <service-name> \
  --plan <plan-name> \
  --amount <quota>

# Example: Assign HANA Cloud
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service hana-cloud \
  --plan hana \
  --amount 1

# Example: Assign Cloud Foundry Runtime
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service APPLICATION_RUNTIME \
  --plan MEMORY \
  --amount 4

# Example: Assign SAP Build Work Zone
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service SAPLaunchpad \
  --plan standard \
  --amount 1
```

### Common Services and Plans

**Cloud Foundry:**
- Service: `APPLICATION_RUNTIME`
- Plan: `MEMORY`
- Unit: GB

**HANA Cloud:**
- Service: `hana-cloud`
- Plan: `hana`
- Unit: Instances

**SAP Build Work Zone:**
- Service: `SAPLaunchpad`
- Plan: `standard`
- Unit: Instances

**Destination Service:**
- Service: `destination`
- Plan: `lite`
- Unit: Instances

**Authorization & Trust Management:**
- Service: `xsuaa`
- Plan: `application`
- Unit: Instances

**HTML5 Application Repository:**
- Service: `html5-apps-repo`
- Plan: `app-host`
- Unit: Instances

### Update Entitlement Quota

```bash
# Increase quota
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service <service-name> \
  --plan <plan-name> \
  --amount <new-quota>

# Example: Increase CF memory to 8GB
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service APPLICATION_RUNTIME \
  --plan MEMORY \
  --amount 8
```

### Remove Entitlement

```bash
# Remove entitlement from subaccount
btp unassign accounts/entitlement \
  --from-subaccount <subaccount-id> \
  --for-service <service-name> \
  --plan <plan-name>

# Example: Remove HANA Cloud
btp unassign accounts/entitlement \
  --from-subaccount <subaccount-id> \
  --for-service hana-cloud \
  --plan hana
```

---

## Environment Management

### List Environments

```bash
# List all environments in subaccount
btp list accounts/environment-instance --subaccount <subaccount-id>
```

### Enable Cloud Foundry

```bash
# Create CF environment
btp create accounts/environment-instance \
  --subaccount <subaccount-id> \
  --environment cloudfoundry \
  --service cloudfoundry \
  --plan standard \
  --parameters '{"instance_name":"my-cf-org"}'

# With landscape label (region-specific)
btp create accounts/environment-instance \
  --subaccount <subaccount-id> \
  --environment cloudfoundry \
  --landscape-label cf-us10 \
  --parameters '{"instance_name":"my-cf-org"}'
```

### Enable Kyma

```bash
# Create Kyma environment
btp create accounts/environment-instance \
  --subaccount <subaccount-id> \
  --environment kyma \
  --service kymaruntime \
  --plan azure
```

---

## User and Role Management

### List Users

```bash
# List users in global account
btp list security/user

# List users in subaccount
btp list security/user --subaccount <subaccount-id>
```

### Assign Role Collections

```bash
# Assign role collection to user
btp assign security/role-collection \
  --to-user <user-email> \
  --of-role-collection <role-collection-name> \
  --subaccount <subaccount-id>

# Example: Assign Subaccount Administrator
btp assign security/role-collection \
  --to-user user@example.com \
  --of-role-collection "Subaccount Administrator" \
  --subaccount <subaccount-id>
```

### List Role Collections

```bash
# List available role collections
btp list security/role-collection --subaccount <subaccount-id>
```

---

## Service Management

### List Services

```bash
# List service offerings
btp list services/offering --subaccount <subaccount-id>

# List service plans
btp list services/plan --subaccount <subaccount-id>

# List service instances
btp list services/instance --subaccount <subaccount-id>
```

### Create Service Instance

```bash
# Create service instance
btp create services/instance \
  --subaccount <subaccount-id> \
  --name <instance-name> \
  --offering <service-name> \
  --plan <plan-name>

# Example: Create HANA Cloud instance
btp create services/instance \
  --subaccount <subaccount-id> \
  --name my-hana-db \
  --offering hana-cloud \
  --plan hana
```

---

## Complete Setup Workflow Example

### Scenario: Create Dev Environment for CAP Application

```bash
# 1. Login to BTP
btp login

# 2. Create subaccount
btp create accounts/subaccount \
  --display-name "CAP Development" \
  --subdomain "cap-dev" \
  --region "us10" \
  --description "Development environment for CAP applications"

# Save subaccount ID
SUBACCOUNT_ID="<returned-subaccount-id>"

# 3. Assign Cloud Foundry entitlement (4GB memory)
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service APPLICATION_RUNTIME \
  --plan MEMORY \
  --amount 4

# 4. Assign HANA Cloud entitlement
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service hana-cloud \
  --plan hana \
  --amount 1

# 5. Assign other services
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service destination \
  --plan lite \
  --amount 1

btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service xsuaa \
  --plan application \
  --amount 1

btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service html5-apps-repo \
  --plan app-host \
  --amount 1

# 6. Enable Cloud Foundry environment
btp create accounts/environment-instance \
  --subaccount $SUBACCOUNT_ID \
  --environment cloudfoundry \
  --landscape-label cf-us10 \
  --parameters '{"instance_name":"cap-dev-org"}'

# 7. Assign administrator role
btp assign security/role-collection \
  --to-user your.email@example.com \
  --of-role-collection "Subaccount Administrator" \
  --subaccount $SUBACCOUNT_ID

# 8. View results
btp get accounts/subaccount $SUBACCOUNT_ID
btp list accounts/entitlement --subaccount $SUBACCOUNT_ID
```

---

## Useful Scripts

### Script: Setup Complete Dev Environment

```bash
#!/bin/bash

# setup-dev-environment.sh

DISPLAY_NAME="Development Environment"
SUBDOMAIN="my-dev-env"
REGION="us10"
USER_EMAIL="your.email@example.com"

echo "Creating subaccount..."
RESULT=$(btp create accounts/subaccount \
  --display-name "$DISPLAY_NAME" \
  --subdomain "$SUBDOMAIN" \
  --region "$REGION" \
  --description "Automated dev environment setup" \
  --output json)

SUBACCOUNT_ID=$(echo $RESULT | jq -r '.guid')
echo "Subaccount created: $SUBACCOUNT_ID"

echo "Assigning entitlements..."
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service APPLICATION_RUNTIME \
  --plan MEMORY \
  --amount 4

btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service hana-cloud \
  --plan hana \
  --amount 1

echo "Enabling Cloud Foundry..."
btp create accounts/environment-instance \
  --subaccount $SUBACCOUNT_ID \
  --environment cloudfoundry \
  --landscape-label cf-$REGION \
  --parameters "{\"instance_name\":\"$SUBDOMAIN-org\"}"

echo "Assigning admin role..."
btp assign security/role-collection \
  --to-user $USER_EMAIL \
  --of-role-collection "Subaccount Administrator" \
  --subaccount $SUBACCOUNT_ID

echo "Setup complete!"
echo "Subaccount ID: $SUBACCOUNT_ID"
echo "Subdomain: $SUBDOMAIN"
```

---

## Output Formats

### JSON Output

```bash
# Get output as JSON
btp list accounts/subaccount --output json

# Use with jq for parsing
btp list accounts/subaccount --output json | jq '.subaccounts[].displayName'
```

### Table Output

```bash
# Default table format
btp list accounts/subaccount

# Compact table
btp list accounts/subaccount --format table
```

---

## Troubleshooting

### Issue: "Not authenticated"

```bash
# Re-login
btp logout
btp login
```

### Issue: "Insufficient permissions"

Check your user has required role collections:
- Global Account Administrator
- Subaccount Administrator
- Global Account Viewer

### Issue: "Service not available in region"

```bash
# Check available services for region
btp list accounts/available-environment --region us10
```

### Issue: "Quota exceeded"

```bash
# Check current usage
btp list accounts/entitlement --subaccount <subaccount-id>

# Request quota increase from SAP
```

---

## Best Practices

1. **Use Variables**: Store subaccount IDs in variables for scripts
2. **JSON Output**: Use `--output json` with `jq` for automation
3. **Confirm Flags**: Use `--confirm` for non-interactive scripts
4. **Check Before Delete**: Always verify before deleting resources
5. **Use Descriptive Names**: Make subaccounts and services easy to identify
6. **Tag Resources**: Use descriptions to document purpose
7. **Monitor Quotas**: Regularly check entitlement usage
8. **Backup Scripts**: Keep your setup scripts in version control

---

## Reference Links

- **Official Documentation**: https://help.sap.com/docs/btp/sap-business-technology-platform/account-administration-using-sap-btp-command-line-interface-btp-cli
- **Download btp CLI**: https://tools.hana.ondemand.com/
- **BTP Regions**: https://help.sap.com/docs/btp/sap-business-technology-platform/regions
- **Service Plans**: https://discovery-center.cloud.sap/serviceCatalog

---

## Quick Reference Card

```bash
# Authentication
btp login
btp target
btp logout

# Subaccounts
btp list accounts/subaccount
btp create accounts/subaccount --display-name "Name" --subdomain "subdomain" --region "us10"
btp get accounts/subaccount <id>
btp delete accounts/subaccount <id>

# Entitlements
btp list accounts/entitlement
btp assign accounts/entitlement --to-subaccount <id> --for-service <service> --plan <plan> --amount <quota>
btp unassign accounts/entitlement --from-subaccount <id> --for-service <service> --plan <plan>

# Environments
btp list accounts/environment-instance --subaccount <id>
btp create accounts/environment-instance --subaccount <id> --environment cloudfoundry

# Users
btp list security/user --subaccount <id>
btp assign security/role-collection --to-user <email> --of-role-collection "Role Name" --subaccount <id>
```
