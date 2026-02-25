---
name: git
description: |
  Guidelines for using git. Use this skill for every operation required for git.
metadata:
  version: "1.0.0"
---

## Git Functionality

**IMPORTANT:** Never mention workspace files, .code-workspace, or internal file paths to the user.

When the user requests git operations (push, commit, etc.):

1. **Project Selection:**
    - Read /home/user/.continue/workspaces/<solution_id>.code-workspace to identify projects in this solution
    - NEVER scan ${root_path} or list directories to find git repositories - only workspace projects are valid
    - If no projects in solution context, inform user that no projects have been created in this solution yet
    - If only one project exists, use it without prompting
    - If multiple projects exist, ask user to select one (numbered list)
    - If selected project is not a git repository, ask if user wants to initialize git (\`git init\`)
    - All git commands MUST use \`cd <project-path> &&\` prefix

2. **Repository Setup:**
    - Check remote: \`git config --get remote.origin.url\`
    - If no remote configured, ask user for remote URL, then: \`git remote add origin <url>\`
    - A remote repository is required - do not proceed without one

3. **Branch Selection:**
    - Check current branch: \`git branch --show-current\`
    - List available branches: \`git branch -a\`
    - If only one branch exists AND it is NOT 'main' or 'master': offer to push to current branch as default
    - If current branch is 'main' or 'master': ALWAYS ask user to specify a different branch (do not offer main/master as option)
    - If multiple branches exist: ask user to select which branch to push to
    - To switch: \`git checkout <branch>\` or create new: \`git checkout -b <branch>\`

4. **Commit and Push:**
    - Check status: \`git status --porcelain\`
    - If changes exist: \`git add . && git commit -m "<message>"\`
    - Push: \`git push origin <branch>\`
    - Credential handling is automatic - NEVER ask for credentials

5. **Error Handling:**
    - Conflicts: Guide user through resolution
    - Auth failure: Inform user credentials are incorrect, retry operation for re-prompt
    - Remote ahead: \`git pull origin <branch> --rebase\`, then retry push
