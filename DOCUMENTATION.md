# Polygon Problem Migration – Technical Documentation

## 1. Project Overview

**Project Name:** Hatsu – Problem Migrator

The Polygon Problem Migration application is a Django-based web application designed to retrieve competitive programming problems and their test cases from Polygon and migrate the information into a database and Azure Blob Storage.

The application helps simplify problem management by retrieving problem details through the Polygon API, storing problem metadata in the database, and uploading test-case input and output files to Azure Blob Storage.

## 2. Project Objectives

The main objectives are:

- Retrieve programming problem details from Polygon.
- Fetch sample and regular test cases.
- Display problem information through a web interface.
- Store problem metadata in the database.
- Migrate test cases into the database.
- Upload test-case input and output files to Azure Blob Storage.
- Support custom checker information.
- Verify whether test-case files have been uploaded successfully.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web application framework |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions |
| PostgreSQL | Database storage |
| Redis | Test-case caching |
| Polygon API | Fetching problem information |
| Azure Blob Storage | Storing test-case files |
| Git and GitHub | Version control |

## 4. System Architecture

The application follows this workflow:

1. The user enters a Polygon Problem ID.
2. Django receives the request.
3. The Polygon API retrieves the problem details.
4. The application fetches the available test cases.
5. Problem metadata is saved to the database when database migration is requested.
6. Test cases are uploaded to Azure Blob Storage.
7. The application verifies the uploaded test-case files.

### Architecture Flow

User  
↓  
Django Web Application  
↓  
Polygon API  
↓  
Problem Details and Test Cases  
↓  
Database Migration / Azure Blob Migration  
↓  
Verification

## 5. Main Functional Modules

### 5.1 Polygon API Integration

The Polygon API integration retrieves:

- Problem ID
- Problem title
- Problem statement
- Input format
- Output format
- Time limit
- Memory limit
- Test cases
- Checker information

### 5.2 Problem Database Migration

The database migration functionality stores problem metadata in the database.

It supports creating a new problem record or updating an existing record based on its Polygon ID.

### 5.3 Test Case Migration to Database

The application processes test cases and stores their information in the database.

The current implementation limits the stored input and output data to 260 characters. Therefore, the database records may not contain complete test-case contents.

### 5.4 Azure Blob Storage Migration

Azure Blob Storage is used to store test-case input and output files separately.

The naming convention is:

```text
test_cases/<database_problem_id>/<test_number>
test_cases/<database_problem_id>/<test_number>.a
```

For example:

```text
test_cases/1/01
test_cases/1/01.a
test_cases/1/02
test_cases/1/02.a
```

The application also supports uploading custom checker-related files.

### 5.5 Test Case Verification

The verification functionality checks whether the input and output blobs exist for each expected test case.

It reports:

- Total test cases
- Complete test cases
- Missing input files
- Missing output files

## 6. Project Directory Structure

```text
PolygonMigration/
│
├── contents/
├── logs/
├── PolygonMigration/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── problems/
│   ├── models.py
│   ├── views.py
│   ├── polygon_api.py
│   ├── AzureTestcase.py
│   ├── templates/
│   └── migrations/
│
├── screenshots/
│   ├── 01_problem_fetched.png
│   ├── 02_test_cases.png
│   ├── 03_database.png
│   ├── 04_azure_migration.png
│   └── 05_verification.png
│
├── static/
├── users/
├── .env
├── .env.example
├── manage.py
├── README.md
└── requirements.txt
```

## 7. Installation and Setup

### Prerequisites

- Python
- Visual Studio Code
- PostgreSQL
- Redis
- Azure Storage account
- Polygon API credentials

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

### Step 2: Navigate to the Project

```bash
cd Polygon-migration-assignment/PolygonMigration
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Configure the required Polygon API credentials, database settings, Redis settings, and Azure storage connection details.

The Azure connection string should be configured using:

```text
AZURE_STORAGE_CONNECTION_STRING=<your-private-connection-string>
```

Do not commit `.env` or expose API credentials and connection strings.

### Step 7: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 8: Run the Django Application

```bash
python manage.py runserver
```

Open the local development server in your browser:

```text
http://127.0.0.1:8000/
```

## 8. Demonstration Workflow

The following workflow demonstrates the main application functionality.

1. Open the Hatsu Problem Migrator application.
2. Enter Polygon Problem ID `69933`.
3. Fetch the problem details.
4. Review the retrieved test cases.
5. Create or update the problem in the database.
6. Migrate test cases to Azure Blob Storage.
7. Verify the uploaded test cases.
8. Review the verification results.

## 9. Test Case Storage Example

For a problem with database ID `1`, the Azure container uses the following structure:

```text
test_cases/
    1/
       01
       01.a
       02
       02.a
       03
       03.a
       ...
       custom_checker.cpp
```

Each test case consists of an input file and its corresponding output file.

## 10. Current Limitations and Future Improvements

### Current Limitations

- Database migration truncates test-case input and output data to 260 characters.
- Obsolete database test-case records are not automatically removed during re-migration.
- Azure migration deletes existing blobs before uploading replacements.
- Interactive problems require a separate interactor-based execution mechanism.
- Upload verification should be completed before reporting a migration as successful.

### Future Improvements

- Preserve complete test-case data in the database or external storage.
- Implement reliable synchronization and cleanup of obsolete records.
- Use safer Azure upload and replacement strategies.
- Improve error handling and migration status reporting.
- Add automated tests for API integration and storage operations.
- Implement secure sandboxed execution for interactive problems.

## 11. Conclusion

The Polygon Problem Migration application integrates Django, Polygon API, database storage, Redis caching, and Azure Blob Storage to simplify competitive programming problem migration.

It provides a workflow for retrieving problem information, storing metadata, migrating test cases, and checking storage completeness.

The project demonstrates API integration, backend development, database operations, cloud storage integration, and verification workflows.