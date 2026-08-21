# Data Quality Report

## Purpose

This document records data-quality issues identified across the three
source systems and explains how each issue is handled by the pipeline.

## Issues Found

### 1. Inconsistent capitalization

Examples:
- Pune
- PUNE
- pune

Planned handling:
Normalize city values before matching.

### 2. Inconsistent phone number formats

Examples:
- 9000000131
- 919000000131
- +91-9000000131
- +91-9000000131

Planned handling:
Normalize phone numbers to a consistent format before matching.

### 3. Inconsistent status capitalization

Examples:
- Active
- active
- ACTIVE

Planned handling:
Normalize status values.

### 4. Different column names for similar information

Examples:
- worker_name / Full Name / Name
- email_id / Email
- location / City
- Phone / Phone Number

Planned handling:
Map source-specific columns to a common internal schema.

### 5. Different compensation formats

Examples:
- 1415/hr
- 15k/month
- 72k/month

Planned handling:
Keep the original value and parse compensation into structured fields
where possible.