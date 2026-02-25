---
name: sap-cap
description: |
  Guidelines for CAP Application creation and development. Use this skill for every new CAP application creation, or when editing an existing CAP application.
metadata:
  version: "1.0.0"
---

# Guidelines for CAP Application Creation and Development

1. You MUST follow this procedure for creating a new CAP application:
- Before running 'cds init <application_name>', check if the intended folder name already exists. If it does, choose a unique folder name by appending a numeric suffix (e.g., "-v2", "-v3", "-2", "-3").
- You MUST use 'cds init <application_name>' cli to init the application folder with the chosen unique name.
- You MUST use the CAP MCP tools to generate the CAP application with full schema entities and services at path <root_path>/<application_name>
- After the CAP project generation is finished successfully, call 'npm install'.
- Call the following command to link the CAP application project into the solution:
'solution-actions project-created -s <solution_id> -p <full path of CAP application's root folder> -t com.sap.project.bas.fs'
- After successfully linking the project, update the workspace file at /home/user/.continue/workspaces/<solution_id>.code-workspace (see "Workspace File Management" section below)
- You MUST use the CAP MCP tools to create sample data for data model entities in 'test/data' as CSV files.      
- Run the following commands to make sure the created code and sample data have no errors. Fix any errors that occur in these commands, and repeat this step until the commands run with no errors.
    1.1 'cds compile srv --for nodejs > /dev/null'
    1.2 'cds deploy --to sqlite::memory:'
- Once verified the service can run with no errors, create UI applications as requested by the user. Always use skill for guidelines to create the UI in the context of CAP application. DO NOT use 'cds add' for creating UI.
- Make sure UI is created only in 'app' folder under the CAP application root folder (that was created with 'cds init' operation).
- Create only the entities, services and UI applications that were approved from the application summary, unless user explicitly requests otherwise.
- Once completing creating the CAP application including its UI, continue with creating relevant processes that should be triggered by this CAP application, exactly as was approved by the user in the application summary.

2. On any operation done on the CAP application, always make sure to be in the root folder of the CAP application that you created with cds init. This including creating UI creation, terminal commands, reading, writing and updating files. Make sure not to consider any file outside this root application folder.
3. DO NOT consider any file outside this root application folder.
4. You MUST use cds 9 compatible code and features.
5. DO NOT change package.json file directly. Changes must be applied only via cds commands as 'cds add' or 'cds import' commands, or npm commands as 'npm add'.
6. DO NOT create sample service and data model entities (with 'cds add sample'), unless user explicitly requests otherwise.
7. When you want to test the CAP application or to find errors, run the following commands in the specified order. If the command returns an error, fix it before running the next.
    7.1 If app directory exists, run 'cds compile app --for nodejs > /dev/null' else run 'cds compile srv --for nodejs > /dev/null'
    7.2 'cds deploy --to sqlite::memory:'

## CAP Project Structure Requirements
- ALL CAP projects MUST follow the official CAP structure: package.json, srv/, db/, app/
- DO NOT allow or create files outside this standard structure
- Before making any changes, validate that the target location follows CAP conventions
- When creating or modifying files, ensure they are placed in the correct standard CAP directories

## CAP / CDS MCP Server Integration
- You MUST use available CAP / CDS MCP server capabilities to gather context and information before making any CAP-related changes or suggestions.
- You MUST search for CDS definitions, like entities, fields and services (which include HTTP endpoints) using the CDS MCP tools, only if it fails you MAY read *.cds files in the project.
- You MUST search for CAP docs using the CDS MCP tools EVERY TIME you modify CDS models or when using APIs from CAP. Do NOT propose, suggest or make any changes without first checking it. This ensures you:
* Use correct CAP syntax and patterns before implementing any CAP functionality
* Follow current best practices
* Implement features according to official documentation
- NEVER propose, suggest, or implement CAP-related changes without first consulting the available CAP MCP server tools.
- MCP server search capabilities support partial matches (e.g., searching for "book" will find "Books" entity).
- Always verify entity relationships, annotations, and service definitions using MCP server model analysis tools before making modifications.