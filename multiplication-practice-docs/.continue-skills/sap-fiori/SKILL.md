---
name: sap-fiori
description: |
  Guidelines for creation and development of SAP Fiori UI, as part of CAP application. Use this skill for every new Fiori UI application creation in the context of CAP, or when editing an existing Fiori UI within the CAP application.
metadata:
  version: "1.0.0"
---

# Guidelines for Creation and Development of SAP Fiori UI, as part of CAP application

1. Use the Fiori MCP tools to create the fiori UI in the CAP application folder context, using the SAP Fiori elements and SAPUI5 technologies.
2. The UI must be created in the 'app' folder under the CAP application root folder created before with 'cds init' operation. This root folder is always a sub folder directly under working directory.
3. When creating UI applications following a CAP application summary, make sure to use UI application names as described in the project structure of the summary, unless user explicitly requested otherwise.
4. After the Fiori MCP Server tools execute successfully:
    - Inform the user that the UI has been created successfully
    - Ask if they need help with anything else
    - Do not double-check or verify if the UI was created successfully - trust that the Fiori MCP Server tools completed the task as intended.
5. When completing creation of the application components do not provide more information on the created components and do not provide information on how to run it. 
6. On any follow-up request to change or modify the UI of the full stack (CAP) application, always try first to make the change by modifying only the app/annotations.cds file. 

## Rules for creation or modification of SAP Fiori elements apps

- When asked to create an SAP Fiori elements app check whether the user input can be interpreted as an application organized into one or more pages containing table data or forms, these can be translated into a SAP Fiori elements application, else ask the user for suitable input.
- The application typically starts with a List Report page showing the data of the base entity of the application in a table. Details of a specific table row are shown in the ObjectPage. This first Object Page is therefore based on the base entity of the application.
- An Object Page can contain one or more table sections based on to-many associations of its entity type. The details of a table section row can be shown in an another Object Page based on the associations target entity.
- The data model must be suitable for usage in a SAP Fiori elements frontend application. So there must be one main entity and one or more navigation properties to related entities.
- Each property of an entity must have a proper datatype.
- For all entities in the data model provide primary keys of type UUID.
- When creating sample data in CSV files, all primary keys and foreign keys MUST be in UUID format (e.g., \`550e8400-e29b-41d4-a716-446655440001\`).
- When generating or modifying the SAP Fiori elements application on top of the CAP service use the Fiori MCP server if available.
- When attempting to modify the SAP Fiori elements application like adding columns you must not use the screen personalization but instead modify the code of the project, before this first check whether an MCP server provides a suitable function.
- When previewing the SAP Fiori elements application use the most specific script for the app in the package.json.