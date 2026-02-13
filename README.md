# NOVASPORT

NOVASPORT is a full-stack Django web application designed for managing and booking sports facilities.  
The platform enables users to discover available sports fields, make reservations, and securely process payments through an integrated booking system.

---

## Project Overview

NOVASPORT provides a centralized system for sports facility management with the following capabilities:

- User authentication and authorization
- Sports field discovery and filtering
- Real-time booking workflow
- Payment processing integration
- Role-based access control (RBAC)
- Modular Django application structure

The system is structured for scalability, maintainability, and secure operation.

---

## Architecture

The project follows a modular Django architecture with separated applications:

- users – Authentication and user management  
- locations – Sports field management and booking logic  
- payments – Payment processing workflows  
- pages – Static and dynamic page rendering  
- guests – Guest-related functionality  

The structure follows separation of concerns principles to improve maintainability and code clarity.

---

## Security Considerations

- Secure authentication mechanisms
- Role-based access control
- Server-side form validation
- Controlled booking authorization
- Structured backend logic to reduce business-logic vulnerabilities

---

## Technology Stack

Backend:
- Python
- Django

Database:
- SQLite (development environment)

Frontend:
- HTML5
- CSS3
- JavaScript

---

## Installation Guide

1. Clone the repository:

git clone https://github.com/Borhanalk/NOVASPORT.git  
cd NOVASPORT  

2. Create a virtual environment:

python -m venv venv  

3. Activate the virtual environment:

Windows:
venv\Scripts\activate  

4. Install dependencies:

pip install -r requirements.txt  

5. Apply migrations:

python manage.py migrate  

6. Run the development server:

python manage.py runserver  

---

## Future Improvements

- Production deployment configuration
- PostgreSQL integration
- REST API implementation
- CI/CD pipeline setup
- Security hardening and optimization

---

## Author

Borhan Kean  
Cybersecurity & Software Engineering Student  
Sami Shamoon College of Engineering (SCE)
