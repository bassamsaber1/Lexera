# Lexera CRM

A Customer Relationship Management (CRM) extension for Microsoft Dynamics 365 Business Central.

## Features

This extension provides comprehensive CRM functionality including:

### Contacts Management
- Track both person and company contacts
- Store complete contact information (address, phone, email)
- Manage customer status (Prospect, Lead, Opportunity, Customer, Inactive)
- Assign contacts to salespeople and territories

### Opportunity Management
- Track sales opportunities through the pipeline
- Multiple sales stages (Qualification, Needs Analysis, Proposal, Negotiation, Closed Won, Closed Lost)
- Estimated value and probability tracking
- Link opportunities to contacts
- Monitor expected close dates

### Activity Management
- Track various activity types (Phone Call, Meeting, Task, Email, Note)
- Schedule activities with start/end date/time
- Set priorities (Low, Normal, High, Urgent)
- Assign activities to team members
- Link activities to contacts and opportunities

## Structure

- **Tables**: Core data structures for Contacts, Opportunities, and Activities
- **Pages**: User interfaces for viewing and editing CRM data
  - List pages for browsing records
  - Card pages for detailed view/edit
- **Enums**: Enumeration types for status values and classifications

## Installation

1. Open the project in Visual Studio Code with the AL Language extension
2. Configure your launch.json with your Business Central environment
3. Press F5 to build and publish the extension

## Usage

After installation, you can access:
- **CRM Contact List**: Browse and manage all contacts
- **CRM Opportunity List**: View and track sales opportunities
- **CRM Activity List**: Manage tasks and interactions

## Object ID Ranges

This extension uses object IDs in the range 50100-50149.