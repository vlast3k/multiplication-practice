# Setup Reference

Detailed setup instructions for the PRD-to-Spec skill.

## Prerequisites

### 1. OpenSpec Skills (Required)

The OpenSpec agent skills must be installed **before** running the prd-to-spec setup script. These skills are installed by the cba-skills install.sh script.

**Required skills:**
- `openspec-new-change` - Create new OpenSpec changes
- `openspec-ff-change` - Generate specifications using fast-forward mode
- `openspec-apply-change` - Apply specifications to implement code

If these skills are not installed, the prd-to-spec setup script will exit with an error and direct you to install them first.
The installation instructions are here: https://github.tools.sap/btp-ai/cba-skills

### 2. Node.js and npm (Required for OpenSpec auto-installation)

Node.js and npm are required **only if OpenSpec CLI is not already installed**. The setup script needs npm to auto-install OpenSpec.

**Check installation:**
```bash
npm --version
node --version
```

**Install Node.js:**
- Download from https://nodejs.org/ (includes npm)
- macOS: `brew install node`
- Windows: Use the installer from nodejs.org
- Linux: Use your distribution's package manager

### 3. OpenSpec CLI (Auto-installed)

OpenSpec CLI is **automatically installed** by the setup script if not found. You do not need to install it manually.

**The setup script will:**
1. Check if `openspec` command is available
2. If not found, automatically install it using: `npm install -g @fission-ai/openspec@latest`
3. Verify the installation succeeded

**Manual installation (if auto-install fails):**
```bash
npm install -g @fission-ai/openspec@latest
```

**Verify installation:**
```bash
openspec --version
```

## Operating Modes

The skill automatically detects which mode to operate in:

### Git Mode

**When it activates:**
- You run the skill inside a git repository
- `git rev-parse --git-dir` succeeds

**Requirements:**
- Git installed
- Git user configured (user.name and user.email)
- Inside a git repository

**Install Git:**
- macOS: `brew install git`
- Windows: https://git-scm.com/download/win
- Linux: Use your distribution's package manager (e.g., `apt install git`)

**Configure Git user:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Features:**
- Creates branch `spec/<change-id>`
- Integrates with git workflow
- User can commit, push, and create PRs manually

**Example directory:**
```bash
cd my-project/          # Your git repository
git status              # Verify it's a git repo
# Run skill here → Git Mode
```

### Non-Git Mode

**When it activates:**
- Git is not installed, OR
- You run the skill in a regular directory (not a git repository)

**Requirements:**
- None (Git not needed)

**Features:**
- Initializes project directly
- No branch management
- User works with files directly

**Example directory:**
```bash
mkdir my-workspace
cd my-workspace/
# Run skill here → Non-Git Mode
```

## Running the Setup Script

The setup script handles all prerequisites, environment detection, OpenSpec installation, and project initialization in a single command.

**IMPORTANT:** You must provide a task type parameter when running the setup script.

**Usage:**
```bash
node /path/to/skills/prd-to-spec/scripts/setup.js <task_type>
```

**Valid task types:**
- `extension` - Side-by-side extension with CAP and custom UI5
- `langchain-agent` - Pro-Code AI Agent using LangChain v1 with AI Core integration
- `appfnd-agent` - Pro-Code AI Agent for SAP App Foundation using A2A protocol

**Examples:**
```bash
# For an App Foundation agent
node /path/to/skills/prd-to-spec/scripts/setup.js appfnd-agent

# For an extension project
node /path/to/skills/prd-to-spec/scripts/setup.js extension

# For a LangChain agent
node /path/to/skills/prd-to-spec/scripts/setup.js langchain-agent
```

**What the setup script does:**

1. **Validates task type parameter**
   - Ensures a valid task type is provided
   - Exits with error if missing or invalid

2. **Checks OpenSpec skills are installed**
   - Verifies `openspec-new-change`, `openspec-ff-change`, `openspec-apply-change` are present
   - Exits with error if skills are missing (directs user to run install.sh)

3. **Detects operating mode**
   - Checks if Git is installed and if current directory is in a git repository
   - Sets mode to "Git Mode" or "Non-Git Mode"
   - Falls back to Non-Git Mode if Git is not installed
   - In Git Mode: validates Git user configuration (exits with error if not configured)

4. **Installs or verifies OpenSpec**
   - Checks if `openspec` command is available
   - If not found, automatically installs via npm:
     - Verifies npm is installed
     - Runs `npm install -g @fission-ai/openspec@latest`
     - Verifies installation succeeded
   - If already installed, displays version
   - Disables telemetry
   - Exits with error if npm is not available

5. **Initializes project based on task type**
   - Copies task-specific config file to `openspec/config.yaml`
   - Copies project stub files for the selected task type to current directory (if a project stub exists for the task type)
   - Creates necessary directory structure
   - Displays summary with task type, operating mode, and next steps

## Project Initialization

The setup script initializes the project directly from assets bundled with the skill:

### Config Files

Task-specific OpenSpec configuration files are stored in `assets/config_files/` and copied to `openspec/config.yaml`:
- `config-extension.yaml` - Configuration for extension projects
- `config-langchain-agent.yaml` - Configuration for LangChain agent projects
- `config-appfnd-agent.yaml` - Configuration for App Foundation agent projects

### Project Stubs

Task-specific project stub files are stored in `assets/project_stubs/<task_type>/` and copied to the current directory:
- Boilerplate code and structure for the selected task type
- If no stub exists for a task type, this step is skipped with a note

## Workflow Summary

### Quick Start (Git Mode)

```bash
# 1. Navigate to your git repository
cd /path/to/your/git/repo

# 2. Run setup with your task type
node /path/to/skills/prd-to-spec/scripts/setup.js appfnd-agent

# 3. Use agent skills (load these using the Skill tool, NOT as bash commands)
#    Load the openspec-new-change skill to create branch and change
#    Load the openspec-ff-change skill with prompt: "Create all planning artifacts based on PRD.md"

# 4. Validate
openspec validate <change-id> --strict
```

### Quick Start (Non-Git Mode)

```bash
# 1. Navigate to your working directory
cd /path/to/workspace

# 2. Run setup with your task type
node /path/to/skills/prd-to-spec/scripts/setup.js extension

# 3. Use agent skills and OpenSpec commands
#    Load openspec-new-change skill using the Skill tool (NOT as a bash command)
#    Load openspec-ff-change skill with prompt: "Create all planning artifacts based on PRD.md"
openspec validate <change-id> --strict

# 4. Review files
ls -la openspec/changes/<change-id>/
```

## Additional Resources

- **Git Documentation:** https://git-scm.com/doc
