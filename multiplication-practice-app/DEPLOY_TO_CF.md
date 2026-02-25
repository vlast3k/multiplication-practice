# 🚀 Deploy to Cloud Foundry - Step by Step Guide

## Prerequisites

✅ Cloud Foundry CLI installed (`cf --version`)
✅ SAP BTP account with Cloud Foundry environment
✅ MTA Build Tool installed (optional, for MTA deployment)

---

## Option 1: Simple CF Push (Fastest)

### Step 1: Login to Cloud Foundry

```bash
cf login
```

You'll be prompted for:
- **API endpoint**: Your CF API URL (e.g., `https://api.cf.us10.hana.ondemand.com`)
- **Email**: Your SAP BTP email
- **Password**: Your password
- **Org**: Select your organization
- **Space**: Select your space (e.g., `dev`)

### Step 2: Create HANA Cloud Service Instance

```bash
cf create-service hana hdi-shared multiplication-practice-db
```

Wait for the service to be created (check status):
```bash
cf service multiplication-practice-db
```

### Step 3: Push the Application

```bash
cd /home/user/projects/multiplication-practice-app
cf push
```

This will:
- Upload your application
- Bind to the HANA database service
- Start the application

### Step 4: Access Your App

```bash
cf apps
```

Look for the URL of `multiplication-practice-app` and open it in your browser!

---

## Option 2: MTA Deployment (Recommended for Production)

### Step 1: Install MTA Build Tool

```bash
npm install -g mbt
```

### Step 2: Build the MTA Archive

```bash
cd /home/user/projects/multiplication-practice-app
mbt build
```

This creates `mta_archives/multiplication-practice_1.0.0.mtar`

### Step 3: Login to Cloud Foundry

```bash
cf login
```

### Step 4: Deploy the MTA

```bash
cf deploy mta_archives/multiplication-practice_1.0.0.mtar
```

This will:
- Create the HANA HDI container
- Deploy the application
- Bind services
- Start the app

### Step 5: Check Deployment Status

```bash
cf apps
cf services
```

---

## Files Created for Deployment

### 1. `manifest.yml`
- Simple CF deployment configuration
- Defines memory, buildpack, services

### 2. `mta.yaml`
- Multi-target application descriptor
- Defines modules and resources
- Includes HANA Cloud service binding

### 3. `package.json` (updated)
- Added `@sap/cds-hana` dependency for production
- Added CDS configuration for HANA Cloud
- Production profile configured

---

## Troubleshooting

### Issue: "No API endpoint set"
**Solution:** Run `cf login` first

### Issue: "Service not found"
**Solution:** Create the HANA service:
```bash
cf create-service hana hdi-shared multiplication-practice-db
```

### Issue: "Not enough memory"
**Solution:** Increase memory in `manifest.yml`:
```yaml
memory: 512M
```

### Issue: "Buildpack not found"
**Solution:** Specify buildpack explicitly:
```bash
cf push -b nodejs_buildpack
```

### Issue: "App crashes on start"
**Solution:** Check logs:
```bash
cf logs multiplication-practice-app --recent
```

---

## Environment Variables

If needed, set environment variables:

```bash
cf set-env multiplication-practice-app NODE_ENV production
cf restage multiplication-practice-app
```

---

## Scaling

Scale your application:

```bash
# Scale instances
cf scale multiplication-practice-app -i 2

# Scale memory
cf scale multiplication-practice-app -m 512M
```

---

## Monitoring

View logs in real-time:
```bash
cf logs multiplication-practice-app
```

View recent logs:
```bash
cf logs multiplication-practice-app --recent
```

Check app health:
```bash
cf app multiplication-practice-app
```

---

## Clean Up

To delete the deployment:

```bash
cf delete multiplication-practice-app -r
cf delete-service multiplication-practice-db
```

---

## Next Steps After Deployment

1. **Test the deployed app** - Open the URL from `cf apps`
2. **Configure custom domain** - Map a custom domain if needed
3. **Set up authentication** - Add SAP IAS or XSUAA
4. **Enable persistence** - Data currently uses in-memory SQLite
5. **Monitor performance** - Use SAP BTP Cockpit

---

## Important Notes

⚠️ **Current Configuration:**
- Uses **in-memory SQLite** for local development
- Uses **HANA Cloud** for production (when deployed to CF)
- **Mock data** will NOT be available in production (need to migrate data)

⚠️ **Before Production:**
1. Remove mock CSV data or migrate to HANA
2. Add authentication (XSUAA service)
3. Configure proper logging
4. Set up monitoring
5. Test thoroughly in dev space first

---

## Quick Reference

```bash
# Login
cf login

# Create service
cf create-service hana hdi-shared multiplication-practice-db

# Push app
cf push

# Check status
cf apps
cf services

# View logs
cf logs multiplication-practice-app --recent

# Delete
cf delete multiplication-practice-app
cf delete-service multiplication-practice-db
```

---

**Your app is now ready to deploy to Cloud Foundry!** 🚀
