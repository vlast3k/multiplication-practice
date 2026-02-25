# BTP CLI Setup Skill

## 🎯 Purpose

This skill provides comprehensive guidance for using the SAP BTP Command Line Interface (btp CLI) to:

- ✅ Create and manage subaccounts
- ✅ Assign and manage entitlements
- ✅ Enable Cloud Foundry environments
- ✅ Manage users and role collections
- ✅ Automate BTP environment setup

---

## 📚 Contents

### Main Documentation
- **`SKILL.md`** - Complete btp CLI reference guide
  - Installation instructions
  - Authentication and login
  - Subaccount management
  - Entitlements management
  - Environment setup (Cloud Foundry, Kyma)
  - User and role management
  - Complete workflow examples
  - Troubleshooting guide

### Example Scripts
- **`examples/setup-multiplication-app-environment.sh`** - Automated setup script
  - Creates subaccount
  - Assigns all required entitlements
  - Enables Cloud Foundry
  - Assigns administrator role
  - Ready-to-use for multiplication practice app

---

## 🚀 Quick Start

### 1. Install btp CLI

```bash
# Check if installed
btp --version

# If not installed, download and install
curl -LO https://tools.hana.ondemand.com/additional/btp-cli-linux-amd64.tar.gz
tar -xzf btp-cli-linux-amd64.tar.gz
sudo mv linux-amd64/btp /usr/local/bin/
```

### 2. Login to BTP

```bash
btp login
```

### 3. Run the Setup Script

```bash
# Edit the script to set your email
nano examples/setup-multiplication-app-environment.sh

# Run the script
./examples/setup-multiplication-app-environment.sh
```

**Or set environment variable:**

```bash
export BTP_USER_EMAIL="your.email@example.com"
./examples/setup-multiplication-app-environment.sh
```

---

## 📖 What the Setup Script Does

The automated script (`setup-multiplication-app-environment.sh`) performs these steps:

1. ✅ **Creates Subaccount**
   - Name: "Multiplication Practice - Dev"
   - Subdomain: "multiplication-practice-dev"
   - Region: us10 (configurable)

2. ✅ **Assigns Entitlements**
   - Cloud Foundry Runtime: 4GB memory
   - HANA Cloud: 1 instance
   - Destination Service: lite plan
   - XSUAA: application plan
   - HTML5 Application Repository: app-host plan

3. ✅ **Enables Cloud Foundry**
   - Creates CF organization
   - Sets up environment

4. ✅ **Assigns Administrator Role**
   - Gives you Subaccount Administrator access

---

## 🎯 Use Cases

### For Multiplication Practice App

The setup script creates the perfect environment for deploying the multiplication practice app:

- **Cloud Foundry** - For deploying the CAP backend
- **HANA Cloud** - For production database
- **HTML5 Repository** - For hosting the UI5 frontend
- **Destination Service** - For external service connections
- **XSUAA** - For authentication (future enhancement)

### General BTP Setup

Use the SKILL.md guide for:
- Creating multiple subaccounts (dev, test, prod)
- Managing entitlements across environments
- Setting up different runtime environments
- Automating BTP account management
- Bulk operations with scripts

---

## 📋 Common Commands

### Check Your Setup

```bash
# View your subaccounts
btp list accounts/subaccount

# View entitlements for a subaccount
btp list accounts/entitlement --subaccount <subaccount-id>

# View CF environments
btp list accounts/environment-instance --subaccount <subaccount-id>
```

### Create Subaccount Manually

```bash
btp create accounts/subaccount \
  --display-name "My Subaccount" \
  --subdomain "my-subdomain" \
  --region "us10" \
  --description "Development environment"
```

### Assign Entitlement

```bash
btp assign accounts/entitlement \
  --to-subaccount <subaccount-id> \
  --for-service APPLICATION_RUNTIME \
  --plan MEMORY \
  --amount 4
```

---

## 🔧 Configuration

### Customizing the Setup Script

Edit these variables in `setup-multiplication-app-environment.sh`:

```bash
DISPLAY_NAME="Multiplication Practice - Dev"  # Subaccount name
SUBDOMAIN="multiplication-practice-dev"       # Subdomain
REGION="us10"                                  # BTP region
USER_EMAIL="your.email@example.com"           # Your email
```

### Available Regions

- `us10` - US East (VA)
- `us20` - US West (WA)
- `us21` - US East (VA) - AWS
- `eu10` - Europe (Frankfurt)
- `eu20` - Europe (Netherlands)
- `ap10` - Australia (Sydney)
- `ap11` - Singapore
- `jp10` - Japan (Tokyo)

---

## 🆘 Troubleshooting

### "Not authenticated"

```bash
btp logout
btp login
```

### "Insufficient permissions"

You need one of these role collections in your global account:
- Global Account Administrator
- Global Account Viewer (for read operations)

Contact your BTP administrator.

### "Service not available in region"

Check available services for your region:

```bash
btp list accounts/available-environment --region us10
```

### Script Fails

Run commands manually from SKILL.md to identify the issue.

---

## 📚 Additional Resources

### Official Documentation
- **BTP CLI Guide**: https://help.sap.com/docs/btp/sap-business-technology-platform/account-administration-using-sap-btp-command-line-interface-btp-cli
- **Download btp CLI**: https://tools.hana.ondemand.com/
- **BTP Regions**: https://help.sap.com/docs/btp/sap-business-technology-platform/regions

### Related Skills
- **git** - For version control
- **sap-cap** - For CAP development
- **sapui5** - For UI5 development

---

## ✅ Verification Checklist

After running the setup script:

- [ ] Subaccount created and visible in BTP Cockpit
- [ ] Cloud Foundry entitlement assigned (4GB)
- [ ] HANA Cloud entitlement assigned
- [ ] Cloud Foundry environment enabled
- [ ] Administrator role assigned
- [ ] Can login with `cf login`
- [ ] Can create CF space
- [ ] Ready to deploy application

---

## 🎉 Next Steps

After setup is complete:

1. **Login to BTP Cockpit**
   - https://cockpit.btp.cloud.sap/

2. **Create CF Space**
   ```bash
   cf login
   cf create-space dev
   cf target -s dev
   ```

3. **Create HANA Cloud Instance**
   - Use BTP Cockpit or btp CLI
   - Wait for instance to be created (~10 minutes)

4. **Deploy Your App**
   ```bash
   cd /home/user/projects/multiplication-practice-app
   cf push
   ```

---

**Your BTP environment is ready for the multiplication practice app!** 🚀
