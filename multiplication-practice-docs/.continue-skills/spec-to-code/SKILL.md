---
name: spec-to-code
description: Implements code from OpenSpec specifications by executing tasks defined in tasks.md. Works with existing OpenSpec changes (either from prd-to-spec or standalone spec changes). Use when the user wants to implement/generate code from a spec, execute tasks from tasks.md, or convert specifications into working code. Always run prd-to-spec first when starting from a PRD.
license: Apache-2.0
metadata:
  author: j.zapf@sap.com
  version: "1.0"
  openspec-min-version: "1.0.0"
  supported-agents: "OpenCode, Cline, Cursor, GitHub Copilot"
compatibility: Requires valid OpenSpec change structure in openspec/changes/<change-id>
allowed-tools: Bash(openspec:*) Bash(git:*) Bash(npm:*) Bash(ls:*) Bash(cd:*) Read Write Edit Glob
---

# Spec to Code Agent Skill

This skill implements code from OpenSpec specifications by systematically executing all tasks defined in the `tasks.md` file. It works with existing OpenSpec changes and ensures all implementation tasks are completed.

**Supported AI Coding Agents:** OpenCode, Cline, Cursor, and GitHub Copilot

## Overview

The spec-to-code skill focuses exclusively on the implementation phase of the OpenSpec workflow. It takes an existing, validated OpenSpec specification and implements all the tasks defined in `tasks.md`.

**When to use this skill:**
- User wants to implement/generate code from an existing spec
- User wants to execute tasks from tasks.md
- User asks to "implement the spec" or "generate code from spec"
- Following a completed prd-to-spec workflow

**When NOT to use this skill:**
- User wants to create a spec from a PRD → Use `prd-to-spec` instead
- User wants to generate specifications → Use `prd-to-spec` instead
- User asks to "generate code from a PRD" → Use `prd-to-spec` first, then this skill

## Prerequisites

### Required

One of the following **must** be true:

1. **Option A: After prd-to-spec workflow**
   - The `prd-to-spec` skill has been run successfully
   - A valid OpenSpec change exists in `openspec/changes/<change-id>/`
   - The change has been validated with `openspec validate <change-id>`

2. **Option B: Standalone OpenSpec change**
   - A valid OpenSpec change structure exists in `openspec/changes/<change-id>/`
   - The change has been validated with `openspec validate <change-id>`

### Additional Requirements

- **OpenSpec CLI** - Must be installed and accessible
- **Git** (for Git Mode) - Working directory must be inside a git repository with a `spec/<change-id>` branch
- **Agent skills** - The `openspec-apply-change` skill must be available

### Validation Before Implementation

Always validate the change before implementing:

```bash
openspec validate <change-id> --strict --no-interactive
```

If validation fails, you must fix the specification before proceeding with implementation.

## Workflow

### Step 1: Verify Prerequisites

Before starting implementation, verify:

1. **Change exists:**
   ```bash
   openspec list
   # Should show your <change-id>
   ```

2. **Change is valid:**
   ```bash
   openspec validate <change-id> --strict --no-interactive
   ```

3. **Tasks file exists:**
   ```bash
   ls openspec/changes/<change-id>/tasks.md
   # Should exist and contain tasks
   ```

4. **Agent skill is available:**
   - Confirm `openspec-apply-change` skill is loaded
   - If not, the user needs to follow the installation instructions here: https://github.tools.sap/btp-ai/cba-skills

### Step 2: Implement All Tasks

**IMPORTANT:** The `openspec-apply-change` skill is an agent skill that contains instructions and workflows, **NOT a bash command or executable script**.

Load the `openspec-apply-change` skill. This skill guides you through implementing all tasks in `tasks.md`. You **must** complete all tasks.

**CRITICAL REMINDER:** After completing ALL tasks from `openspec-apply-change`, you MUST return to this skill and continue with **Step 3: Implement Observability** (if building an AI agent). 
Do NOT consider the implementation complete until Step 3 is evaluated. To ensure this, add a final task in `tasks.md` that explicitly instructs you to return to the skill and complete Step 3.

### Step 3: Implement Observability

> **Note:** This step only applies when building an AI agent. Skip this step if the implementation is not an agent (e.g., a CAP/UI5 extension).

After implementing all tasks, set up observability by copying the lowcode module and configuration file to the project root. This enables agent configuration tracking and parameter exposure.

#### 3.1 Copy the lowcode Module, config.py, and .vscode Directory

Copy the `lowcode` directory, `.vscode` directory from the skill assets to the project root:
Copy the `config.py` into the folder or module where the agent is implemented (most likely /app).

```bash
cp -r .claude/skills/spec-to-code/assets/lowcode ./lowcode
cp .claude/skills/spec-to-code/assets/config.py ./app/config.py
cp -r .claude/skills/spec-to-code/assets/.vscode ./.vscode
```

The `lowcode` module provides:
- `decorators.py` - Decorators for exposing agent configuration (`@agent_config`, `@prompt_section`, `@mcp_server`, `@exposed_param`)
- `registry.py` - Registry for tracking exposed fields and their metadata
- `runtime.py` - Runtime utilities for config resolution

#### 3.2 Adapt config.py to the Current Agent

Modify `config.py` to reflect the implemented agent's configuration. The template provides a basic example:

```python
from lowcode.decorators import agent_config

@agent_config(key="agent.model", label="LLM Model", description="LLM Model Identifier")
def model_name():
    return "gpt-5"
```

Extend this file based on the agent's actual configuration needs. Common additions include:

```python
from lowcode.decorators import agent_config, prompt_section, mcp_server
from lowcode.registry import GroupKind

# Agent configuration
@agent_config(key="agent.model", label="LLM Model", description="LLM Model Identifier")
def model_name():
    return "gpt-5"  # Update to match implemented agent

@agent_config(key="agent.temperature", label="Temperature", description="LLM sampling temperature")
def temperature():
    return 0.7

@agent_config(key="agent.max_tokens", label="Max Tokens", description="Maximum tokens in response")
def max_tokens():
    return 4096

# Prompt sections (if applicable)
@prompt_section(
    key="prompts.system",
    label="System Prompt",
    description="Main system prompt for the agent",
    group=GroupKind.BASICS,
    order=0
)
def system_prompt():
    return "You are a helpful assistant."

# MCP servers (if applicable)
@mcp_server(
    key="mcp.filesystem",
    label="Filesystem Server",
    description="MCP server for filesystem access",
    group=GroupKind.MCP_SERVER,
    order=0
)
def filesystem_server():
    return {"command": "npx", "args": ["-y", "@anthropic/mcp-server-filesystem"]}
```

**Adaptation Guidelines:**
1. Review the implemented agent's code to identify all configurable parameters
2. Add `@agent_config` decorators for each configuration option (model, temperature, etc.)
3. Add `@prompt_section` decorators for editable prompt components
4. Add `@mcp_server` decorators for any MCP server configurations
5. Update default values to match the actual implementation
6. Organize fields using `GroupKind` categories for better UI presentation

#### 3.3 Integrate config.py Functions into the Agent

After defining the configuration functions in `config.py`, you **must** update the agent code to actually call these functions. The decorated functions are not automatically wired into the agent—they must be explicitly imported and invoked where the configuration values are used.

**Integration Steps:**

1. **Import the config module** in your agent's main entry point or wherever configuration is needed:
   ```python
   import config
   ```

2. **Replace hardcoded values** with calls to the config functions:
   ```python
   # Before (hardcoded):
   model = "gpt-4"
   temperature = 0.7
   system_prompt = "You are a helpful assistant."
   
   # After (using config.py functions):
   model = config.model_name()
   temperature = config.temperature()
   system_prompt = config.system_prompt()
   ```

3. **For MCP server configurations**, use the returned dictionary:
   ```python
   fs_server_config = config.filesystem_server()
   # Returns: {"command": "npx", "args": ["-y", "@anthropic/mcp-server-filesystem"]}
   ```

**Example Integration:**

If your agent has a main initialization file (e.g., `agent.py` or `main.py`):

```python
import config
from some_llm_library import LLMClient

# Initialize LLM with config values
client = LLMClient(
    model=config.model_name(),
    temperature=config.temperature(),
    max_tokens=config.max_tokens(),
)

# Use prompt sections
system_message = config.system_prompt()
```

**Why This Matters:**
- The decorators in `config.py` register the fields in the `REGISTRY` for discoverability and UI exposure
- But the actual runtime behavior requires calling the functions to get the current values
- This separation allows the lowcode platform to override values while maintaining code clarity


## What This Skill Does NOT Do

This skill does **NOT** perform the following actions (these are left to the user):

- Create or modify specifications (use `prd-to-spec` for this)
- Commit changes to git
- Push code to remote repositories
- Create pull requests
- Merge branches
- Tag releases

**Rationale:** The user should review all implemented code before committing and sharing it.

## Command Reference

### Verification Commands

| Command | Purpose |
|---------|---------|
| `openspec list` | List all OpenSpec changes |
| `openspec show <change-id>` | Show change details |
| `openspec validate <change-id> --strict` | Validate the change structure |
| `cat openspec/changes/<change-id>/tasks.md` | View implementation tasks |

### Agent Skills

**CRITICAL:** These are agent skills that contain instructions and workflows, **NOT bash commands or executable scripts**.

| Skill Name | Purpose |
|---------|---------|
| `openspec-apply-change` | Implement all tasks from tasks.md - Load this skill with the change ID |

## Relationship with prd-to-spec

This skill is designed to work seamlessly with the `prd-to-spec` skill:

### Full PRD-to-Code Workflow

When a user wants to generate code from a PRD:

1. **First:** Use `prd-to-spec` skill
   - Processes the PRD
   - Generates the specification
   - Creates OpenSpec change structure
   - Validates the spec

2. **Then:** Use `spec-to-code` skill (this skill)
   - Implements the tasks from the generated spec
   - Verifies implementation
   - Completes the code

### Standalone Spec Implementation

When a user has an existing OpenSpec change (created manually or from another source):

1. **Verify** the change structure exists and is valid
2. **Use** `spec-to-code` skill directly to implement tasks

## Troubleshooting

### "OpenSpec change not found"

**Cause:** No change exists with the specified ID

**Solution:**
```bash
# List all changes
openspec list

# Verify the change ID exists
ls openspec/changes/
```

If no changes exist, you need to:
- Run `prd-to-spec` first to create a change from a PRD, or
- Manually create a valid OpenSpec change structure

### "tasks.md not found or empty"

**Cause:** The specification doesn't have implementation tasks defined

**Solution:**
- If you used `prd-to-spec`, re-run the spec generation step
- If using a manual spec, create `tasks.md` with implementation tasks
- Validate the change structure: `openspec validate <change-id> --strict`

### "openspec-apply-change skill not available"

**Cause:** Agent skills haven't been loaded

**Solution:**
1. Instruct the user to follow the installation instructions here: https://github.tools.sap/btp-ai/cba-skills
2. Reload your agent to pick up the newly installed skills
3. Try loading the skill again

### "Validation failed"

**Cause:** The OpenSpec change structure is invalid or incomplete

**Solution:**
```bash
# Run validation with details
openspec validate <change-id> --strict

# Fix reported issues in the spec
# Re-validate before attempting implementation
```

### "Git branch not found (Git Mode)"

**Cause:** Not on the correct `spec/<change-id>` branch

**Solution:**
```bash
# Check current branch
git branch

# Switch to the spec branch
git checkout spec/<change-id>

# Or create it if it doesn't exist
git checkout -b spec/<change-id>
```

## Reference

- OpenSpec documentation: See the OpenSpec CLI help (`openspec --help`)
- prd-to-spec skill: For creating specs from PRDs


### FINAL INSTRUCTIONS

Once the code is generated, do this:
Execute the add-code-decorators skill to add decorators for the low level UI of the agent
