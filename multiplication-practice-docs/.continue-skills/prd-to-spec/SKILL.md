---
name: prd-to-spec
description: Processes Product Requirements Documents (PRDs) using OpenSpec to generate specifications. Automates the workflow from PRD to spec artifacts including proposal.md, spec deltas, and tasks.md. Works in both git and non-git modes. Requires task type selection (extension, langchain-agent, or appfnd-agent). Use when the user wants to generate/create a spec from a PRD. For implementation, use spec-to-code skill after this. When user wants to generate code from a PRD, run this skill first, then spec-to-code.
license: Apache-2.0
metadata:
  author: j.zapf@sap.com
  version: "1.1"
  openspec-min-version: "1.0.0"
  supported-agents: "OpenCode, Cline, Cursor, GitHub Copilot"
compatibility: Requires Git for Git Mode operation and Node.js/npm for OpenSpec auto-installation
allowed-tools: Bash(git:*) Bash(npm:*) Bash(openspec:*) Bash(chmod:*) Bash(ls:*) Bash(cd:*) Read Write Edit Glob
---

# PRD to Spec Agent Skill

This skill automates the workflow of processing Product Requirements Documents (PRDs) using OpenSpec and generating specifications. It initializes projects based on task type (extension, langchain-agent, or appfnd-agent) and works in both git and non-git environments. **For implementation, use the spec-to-code skill after generating the spec.**

**Supported AI Coding Agents:** OpenCode, Cline, Cursor, and GitHub Copilot

## Overview

The skill supports two modes of operation:

### Git Mode
When executed in a git repository:
1. Initializes project with task-specific configuration and stubs
2. Creates a new working branch `spec/<change-id>`
3. Generates specs from PRD using OpenSpec
4. **For implementation:** Use the `spec-to-code` skill

### Non-Git Mode
When executed in a regular folder (or when Git is not installed):
1. Initializes project with task-specific configuration and stubs
2. Generates specs from PRD using OpenSpec
3. **For implementation:** Use the `spec-to-code` skill

## Prerequisites

### Required

- **OpenSpec Skills** - The openspec-new-change, openspec-ff-change, and openspec-apply-change skills must be installed and loaded first. These are installed by the user by running the install.sh script from the cba-skills repository (https://github.tools.sap/btp-ai/cba-skills).
- **Node.js and npm** - For OpenSpec auto-installation (if not already installed)

**Note:** The setup script will auto-install OpenSpec CLI if not found and verify all requirements.

### Additional Requirements for Git Mode

- **Git** - Required only for Git Mode operation
- **Git user configuration** - user.name and user.email must be set globally
- Working directory must be inside a git repository

### Agent Skills

This skill requires three OpenSpec agent skills that must be installed first by running the install.sh script from the cba-skills repository:

- `openspec-new-change` - Creates a new OpenSpec change
- `openspec-ff-change` - Generates specifications using fast-forward mode
- `openspec-apply-change` - Applies specifications to implement code (used by spec-to-code skill)

**Important:** These skills must be installed before running the prd-to-spec skill setup.

**How to use these skills:**
- **DO NOT execute these as bash commands** (e.g., `./openspec-new-change` or `bash -c "openspec-new-change"`)
- **DO load the skill and perform the actions** it defines using the Skill tool
- These are agent skills that contain instructions and workflows, not executable scripts

## Workflow

### Step 1: Determine Task Type

**CRITICAL:** Before running setup, you **must** determine the task type based on the PRD content and user requirements.

**Supported task types:**

- `extension` - Side-by-side extension with CAP and custom UI5
- `langchain-agent` - Pro-Code AI Agent using LangChain v1 with AI Core integration, FastAPI server, and chat UI
- `appfnd-agent` - Pro-Code AI Agent for SAP App Foundation using Agent2Agent (A2A) protocol

**How to determine task type:**
- Review the PRD content carefully
- Look for keywords: "agent", "AI", "extension", "CAP", "UI5", "LangChain"
- Default to `appfnd-agent` if building an AI agent
- Only use `langchain-agent` if the PRD or user explicitly mention LangChain
- Use `extension` for traditional application extensions with CAP/UI5

### Step 2: Run Setup

Run the setup script with the task type you determined in Step 1:

```bash
node /path/to/skills/prd-to-spec/scripts/setup.js <task_type>
```

**Example:**
```bash
# For an extension project
node /path/to/skills/prd-to-spec/scripts/setup.js extension

# For a LangChain agent
node /path/to/skills/prd-to-spec/scripts/setup.js langchain-agent

# For an App Foundation agent
node /path/to/skills/prd-to-spec/scripts/setup.js appfnd-agent
```

**What this does:**

1. **Validates task type parameter**
   - Ensures a valid task type is provided (extension, langchain-agent, or appfnd-agent)
   - Exits with error if missing or invalid

2. **Verifies OpenSpec skills are installed**
   - Checks that all required skills (openspec-new-change, openspec-ff-change, openspec-apply-change) are present
   - Exits with error if skills are missing

3. **Detects operating mode**
   - Git Mode (if Git is installed and in a git repository) or Non-Git Mode
   - Falls back to Non-Git Mode if Git is not installed
   - In Git Mode: validates Git user configuration

4. **Installs OpenSpec**
   - Auto-installs if not found (requires npm)
   - Configures environment and disables telemetry

5. **Initializes project based on task type**
   - Copies task-specific config file to `openspec/config.yaml`
   - Copies project stub files for the selected task type to current directory
   - Creates necessary directory structure

**Expected output:**
- Task type confirmation
- OpenSpec skills verification status
- Operating mode (Git Mode or Non-Git Mode)
- Git user information (if in Git Mode)
- OpenSpec installation status (installed or auto-installed)
- Project initialization progress
- Config file and stub files copy confirmation

### Step 3: Create Git Branch (Git Mode Only)

If running in Git Mode, create a new branch for your spec work:

```bash
# Agent will determine the change-id from the PRD
git checkout -b spec/<change-id>
```

**Change ID format:**
- Derived from PRD title or content
- Lowercase with hyphens (e.g., `user-authentication`, `payment-integration`)
- If branch exists, append suffix: `spec/<change-id>-v2`

### Step 4: Create OpenSpec Change

**IMPORTANT:** After running the setup script, you **must** ensure that you can access the newly installed agent skills (`openspec-new-change`, `openspec-ff-change`, `openspec-apply-change`).

Create a new change in OpenSpec by loading the `openspec-new-change` agent skill and follow its instructions to create a new OpenSpec change with the name `<change-name>`.

**Change name should:**
- Be descriptive of the feature (e.g., "user-authentication")
- Use lowercase with hyphens
- Avoid special characters
- Be the same as the branch name in Git Mode

### Step 5: Generate Specification

Generate the full spec based on the PRD by loading the `openspec-ff-change` agent skill and following its instructions.

### Step 6: Validate Specification

Validate the generated spec:

```bash
openspec validate <change-id> --strict --no-interactive
```

**Validation checks:**
- Spec structure and format
- Required fields and metadata
- Cross-references and consistency
- Task completeness

## Next Steps: Implementation

After generating and validating the specification, you can implement the code using the **spec-to-code** skill.

**When to use spec-to-code:**
- User explicitly requests implementation
- User asks to "implement the spec" or "generate code from spec"  
- User wants to execute tasks from tasks.md

**How to proceed:**
1. Load the `spec-to-code` skill
2. The spec-to-code skill will verify prerequisites and implement all tasks from tasks.md
3. See the spec-to-code skill documentation for details

**Note:** If the user wants to "generate code from a PRD," you should:
1. Run this skill (prd-to-spec) first to create the specification
2. Then run the spec-to-code skill to implement the code

## What the Agent Does NOT Do

The agent does **NOT** perform the following actions (these are left to the user or other skills):

- **Implement code** - Use the `spec-to-code` skill for implementation
- Commit changes to git
- Push code to remote repositories
- Create pull requests
- Merge branches
- Tag releases

**Rationale:** 
- Specification and implementation are separate concerns
- The user should review all generated artifacts before committing and sharing them

## Command Reference

### Setup Commands

| Command | Purpose |
|---------|---------|
| `node /path/to/skills/prd-to-spec/scripts/setup.js <task_type>` | Complete setup - validates task type, verifies prerequisites, installs OpenSpec, initializes project |

### Agent Skills (Slash Commands)

**CRITICAL:** These are agent skills that contain instructions and workflows, **NOT bash commands or executable scripts**.

**How to use these skills:**
1. Use the Skill tool to load the skill by name
2. Follow the instructions provided by the loaded skill
3. **DO NOT** execute these as bash commands (e.g., `./openspec-new-change` or `bash -c "openspec-new-change"`)

| Skill Name | Purpose |
|---------|---------|
| `openspec-new-change` | Create a new OpenSpec change - Load this skill with the change name |
| `openspec-ff-change` | Generate full spec from PRD using fast-forward mode - Load this skill with your prompt |

**Note:** For implementation, use the `spec-to-code` skill which utilizes the `openspec-apply-change` skill.

### OpenSpec CLI Commands

| Command | Purpose |
|---------|---------|
| `openspec validate <id> --strict` | Validate a change |
| `openspec list` | List active changes |
| `openspec show <item>` | View change or spec details |

## Troubleshooting

For common issues and detailed solutions, see [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md).

### Quick Fixes

**"Invalid task_type"** - Ensure you provide a valid task type: extension, langchain-agent, or appfnd-agent

**"Missing required OpenSpec skills"** - Run the cba-skills install.sh script first to install the OpenSpec agent skills

**"No Git user configured"** (Git Mode only) - Run: `git config --global user.name "Your Name"` and `git config --global user.email "email@example.com"`

**"Config file not found"** - Ensure the prd-to-spec skill includes the assets/config_files directory with task-type-specific config files

## Reference

- For detailed setup instructions: [references/SETUP.md](references/SETUP.md)

# When PRD to Spec is finished

- recommend to the user to generate code from the specs. If the user accepts the recommendation use spec-to-code skill
