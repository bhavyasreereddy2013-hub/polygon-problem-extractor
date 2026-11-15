# Polygon Problem Extractor

A Django-based application designed to extract programming problem details and test cases from Polygon and migrate them to Azure Blob Storage.

## Project Overview

Polygon Problem Extractor integrates with the Polygon API to retrieve problem information, test cases, and custom checker files. It provides migration functionality to store test-case data and checker files in Azure Blob Storage.

## Features

- Integration with the Polygon API.
- Extraction of programming problem test cases.
- Retrieval of test inputs and expected outputs.
- Migration of test cases to Azure Blob Storage.
- Custom checker source retrieval and compilation.
- Upload of custom checker files to Azure Blob Storage.
- Redis-based test-case caching.
- Django-based web interface.
- Test-case migration validation.

## Technologies Used

- **Backend:** Python, Django
- **API Integration:** Polygon API
- **Cloud Storage:** Microsoft Azure Blob Storage
- **Caching:** Redis
- **Database:** Django-supported database
- **Frontend:** HTML, CSS
- **Development Environment:** Visual Studio Code

## Project Structure

```text
Polygon-Problem-Extractor/
│
├── PolygonMigration/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── problems/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── contents/
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/bhavyasreereddy2013-hub/polygon-problem-extractor.git
cd polygon-problem-extractor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Configure the required credentials:

- Polygon API credentials
- Azure Storage account details
- Redis connection details, if required by the application
- Other application-specific settings

**Important:** Never commit actual API keys, passwords, or cloud credentials to GitHub.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Django Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## Test Case Migration

The application supports retrieving test cases from Polygon and migrating them to Azure Blob Storage.

The migration process includes:

1. Connecting to the Polygon API.
2. Retrieving problem test cases.
3. Fetching input and expected output files.
4. Uploading available test cases to Azure Blob Storage.
5. Retrieving custom checker source files when available.
6. Compiling and uploading custom checker files.
7. Validating the availability of migrated test-case files.

## Security

- Credentials are maintained through environment configuration.
- `.env` files are excluded from Git tracking.
- Virtual environments and Python cache files are excluded from version control.

## Author

**Bhavya Sree Reddy**

GitHub: https://github.com/bhavyasreereddy2013-hub