# Troubleshooting Guide

This guide covers common issues and solutions for the PRD-to-Spec skill.

## Common Issues

### "Invalid task_type" or "task_type argument is required"

**Symptom:** Setup script exits with error about missing or invalid task_type.

**Cause:** The setup script requires a valid task type parameter.

**Solution:**
```bash
# Provide a valid task type when running setup
node /path/to/skills/prd-to-spec/scripts/setup.js <task_type>

# Valid task types:
# - extension        (Side-by-side extension with CAP and custom UI5)
# - langchain-agent  (Pro-Code AI Agent using LangChain v1)
# - appfnd-agent     (Pro-Code AI Agent for SAP App Foundation)
```

**Example:**
```bash
node /path/to/skills/prd-to-spec/scripts/setup.js appfnd-agent
```

### "Missing required OpenSpec skills"

**Symptom:** Setup script exits with error about missing OpenSpec skills during step [1/4].

**Cause:** The OpenSpec agent skills have not been installed yet.

**Solution:**
Direct the user to follow the installation instructions here: https://github.tools.sap/btp-ai/cba-skills

**Required skills:**
- `openspec-new-change` - Create new OpenSpec changes
- `openspec-ff-change` - Generate specifications using fast-forward mode
- `openspec-apply-change` - Apply specifications to implement code

### "No Git user configured" (Git Mode)

**Symptom:** Setup script fails in Git Mode with missing user configuration.

**Solution:**
```bash
# Configure git user globally
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

**Note:** This error only occurs in Git Mode. In Non-Git Mode, git user configuration is not required.

### "Config file not found"

**Symptom:** Setup script shows warning about missing config file during step [4/4].

**Cause:** The task-specific config file is missing from the skill's `assets/config_files/` directory.

**Solution:**
1. Verify the skill installation is complete
2. Check that the `assets/config_files/` directory contains:
   - `config-extension.yaml`
   - `config-langchain-agent.yaml`
   - `config-appfnd-agent.yaml`
3. If files are missing, reinstall the prd-to-spec skill

### "OpenSpec CLI not found"

**Symptom:** Warning about OpenSpec not being installed (or auto-install attempt).

**Auto-installation:**

The setup script will automatically attempt to install OpenSpec if:
- npm is available
- You have permissions for global npm installs

**If auto-install fails:**

1. **Check npm availability:**
   ```bash
   npm --version
   # If not found, install Node.js: https://nodejs.org/
   ```

2. **Check npm permissions:**
   ```bash
   # On Linux/Mac, you may need to configure npm for non-root global installs
   # See: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally
   ```

3. **Manual installation:**
   ```bash
   npm install -g @fission-ai/openspec@latest
   ```

4. **Verify installation:**
   ```bash
   openspec --version
   which openspec
   ```

**Common issues:**

- **npm not installed:** Install Node.js from https://nodejs.org/
- **Permission denied:** Configure npm for non-root installs or use sudo (not recommended)
- **PATH issues:** Ensure npm global bin directory is in your PATH

### Project files not copied

**Symptom:** Setup succeeds but expected project files aren't in current directory.

**Debugging steps:**

1. **Check setup output:**
   - If you see "Note: No project stub found for <task_type>", this means no stub files exist for that task type
   - This is not an error - some task types may not have stub files

2. **Verify current directory:**
   ```bash
   pwd
   # Ensure you're in the intended target directory
   ```

3. **Check permissions:**
   ```bash
   ls -la
   # Ensure you have write permissions
   ```

4. **Verify openspec directory was created:**
   ```bash
   ls -la openspec/
   # Should contain config.yaml
   ```

5. **Re-run setup:**
   ```bash
   node /path/to/skills/prd-to-spec/scripts/setup.js <task_type>
   ```

### Agent Skills Not Available

**Symptom:** Agent skills `openspec-new-change`, `openspec-ff-change`, or `openspec-apply-change` are not recognized.

**Cause:** Agent has not loaded the OpenSpec skills, or skills were not installed.

**Solution:**

1. **Verify skills were installed:**
   ```bash
   ls -la /path/to/skills/
   # Look for: openspec-new-change/, openspec-ff-change/, openspec-apply-change/
   ```

2. **If skills are missing:**
   - Instruct user to run the IBD Skills installer: https://github.tools.sap/btp-ai/cba-skills

3. **Remember: These are agent skills, not bash commands:**
   - Use the Skill tool to load them (e.g., load skill `openspec-new-change`)
   - **DO NOT** execute them as bash commands (e.g., `./openspec-new-change`)

## Additional Resources

- **Git Documentation:** https://git-scm.com/doc
- **Setup Reference:** [SETUP.md](SETUP.md)
