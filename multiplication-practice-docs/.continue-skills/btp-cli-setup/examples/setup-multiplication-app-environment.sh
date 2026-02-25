#!/bin/bash

# Setup BTP Environment for Multiplication Practice App
# This script creates a complete BTP environment for deploying the multiplication practice app

set -e  # Exit on error

# Configuration
DISPLAY_NAME="Multiplication Practice - Dev"
SUBDOMAIN="multiplication-practice-dev"
REGION="us10"  # Change to your preferred region
USER_EMAIL="${BTP_USER_EMAIL:-your.email@example.com}"  # Set BTP_USER_EMAIL env var or change here

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}BTP Environment Setup${NC}"
echo -e "${BLUE}Multiplication Practice App${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if btp CLI is installed
if ! command -v btp &> /dev/null; then
    echo -e "${RED}Error: btp CLI is not installed${NC}"
    echo "Install from: https://tools.hana.ondemand.com/"
    exit 1
fi

# Check if logged in
if ! btp target &> /dev/null; then
    echo -e "${RED}Error: Not logged in to BTP${NC}"
    echo "Run: btp login"
    exit 1
fi

echo -e "${GREEN}✓ btp CLI is installed and authenticated${NC}"
echo ""

# Step 1: Create Subaccount
echo -e "${BLUE}Step 1: Creating subaccount...${NC}"
RESULT=$(btp create accounts/subaccount \
  --display-name "$DISPLAY_NAME" \
  --subdomain "$SUBDOMAIN" \
  --region "$REGION" \
  --description "Development environment for Multiplication Practice App" \
  --output json 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}Error creating subaccount:${NC}"
    echo "$RESULT"
    exit 1
fi

SUBACCOUNT_ID=$(echo $RESULT | jq -r '.guid')
echo -e "${GREEN}✓ Subaccount created${NC}"
echo "  ID: $SUBACCOUNT_ID"
echo "  Subdomain: $SUBDOMAIN"
echo ""

# Step 2: Assign Cloud Foundry Runtime Entitlement (4GB)
echo -e "${BLUE}Step 2: Assigning Cloud Foundry runtime entitlement (4GB)...${NC}"
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service APPLICATION_RUNTIME \
  --plan MEMORY \
  --amount 4 > /dev/null 2>&1

echo -e "${GREEN}✓ Cloud Foundry runtime entitlement assigned (4GB)${NC}"
echo ""

# Step 3: Assign HANA Cloud Entitlement
echo -e "${BLUE}Step 3: Assigning HANA Cloud entitlement...${NC}"
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service hana-cloud \
  --plan hana \
  --amount 1 > /dev/null 2>&1

echo -e "${GREEN}✓ HANA Cloud entitlement assigned${NC}"
echo ""

# Step 4: Assign Destination Service
echo -e "${BLUE}Step 4: Assigning Destination service...${NC}"
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service destination \
  --plan lite \
  --amount 1 > /dev/null 2>&1

echo -e "${GREEN}✓ Destination service entitlement assigned${NC}"
echo ""

# Step 5: Assign XSUAA (Authorization & Trust Management)
echo -e "${BLUE}Step 5: Assigning XSUAA service...${NC}"
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service xsuaa \
  --plan application \
  --amount 1 > /dev/null 2>&1

echo -e "${GREEN}✓ XSUAA service entitlement assigned${NC}"
echo ""

# Step 6: Assign HTML5 Application Repository
echo -e "${BLUE}Step 6: Assigning HTML5 Application Repository...${NC}"
btp assign accounts/entitlement \
  --to-subaccount $SUBACCOUNT_ID \
  --for-service html5-apps-repo \
  --plan app-host \
  --amount 1 > /dev/null 2>&1

echo -e "${GREEN}✓ HTML5 Application Repository entitlement assigned${NC}"
echo ""

# Step 7: Enable Cloud Foundry Environment
echo -e "${BLUE}Step 7: Enabling Cloud Foundry environment...${NC}"
echo "  (This may take a few minutes)"

CF_RESULT=$(btp create accounts/environment-instance \
  --subaccount $SUBACCOUNT_ID \
  --environment cloudfoundry \
  --landscape-label cf-$REGION \
  --parameters "{\"instance_name\":\"$SUBDOMAIN-org\"}" \
  --output json 2>&1)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cloud Foundry environment enabled${NC}"
    echo "  Org name: $SUBDOMAIN-org"
else
    echo -e "${RED}Warning: Cloud Foundry environment creation may have failed${NC}"
    echo "  You can enable it manually in BTP Cockpit"
fi
echo ""

# Step 8: Assign Administrator Role
echo -e "${BLUE}Step 8: Assigning Subaccount Administrator role...${NC}"
btp assign security/role-collection \
  --to-user $USER_EMAIL \
  --of-role-collection "Subaccount Administrator" \
  --subaccount $SUBACCOUNT_ID > /dev/null 2>&1

echo -e "${GREEN}✓ Administrator role assigned to $USER_EMAIL${NC}"
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Setup Complete! 🎉${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Subaccount Details:"
echo "  Name: $DISPLAY_NAME"
echo "  ID: $SUBACCOUNT_ID"
echo "  Subdomain: $SUBDOMAIN"
echo "  Region: $REGION"
echo ""
echo "Entitlements Assigned:"
echo "  ✓ Cloud Foundry Runtime: 4GB"
echo "  ✓ HANA Cloud: 1 instance"
echo "  ✓ Destination Service: lite plan"
echo "  ✓ XSUAA: application plan"
echo "  ✓ HTML5 App Repository: app-host plan"
echo ""
echo "Next Steps:"
echo "  1. Login to BTP Cockpit: https://cockpit.btp.cloud.sap/"
echo "  2. Navigate to your subaccount: $SUBDOMAIN"
echo "  3. Create a Cloud Foundry space (e.g., 'dev')"
echo "  4. Create HANA Cloud instance in BTP Cockpit"
echo "  5. Deploy your app:"
echo "     cd /home/user/projects/multiplication-practice-app"
echo "     cf login"
echo "     cf push"
echo ""
echo "View subaccount in BTP Cockpit:"
echo "  https://cockpit.btp.cloud.sap/cockpit#/globalaccount/<your-ga>/subaccount/$SUBACCOUNT_ID"
echo ""
