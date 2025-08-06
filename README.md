# Hospital Management System

A comprehensive web-based Hospital Management System built with Flask, offering role-based access control and multiple modules for efficient hospital operations.

## Features

- **Multi-Role Authentication System**
  - Admin
  - Doctor
  - Receptionist
  - Pharmacist
  - Lab Technician

- **Core Modules**
  - Patient Registration & Management
  - Appointment Scheduling
  - Doctor's Panel
  - Billing System
  - Pharmacy Management
  - Laboratory Management
  - Report Generation
  - Admin Dashboard

- **Additional Features**
  - Email Notifications
  - Statistical Dashboard
  - Dark/Light Theme Toggle
  - Responsive Design

## Tech Stack

- **Backend**: Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Flask-Login
- **PDF Generation**: ReportLab

## Project Structure

```
hospital_manager/
├── app/
│   ├── models/
│   ├── routes/
│   ├── static/
│   ├── templates/
│   └── utils/
├── migrations/
├── instance/
├── tests/
├── .env
├── config.py
├── requirements.txt
└── run.py
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hospital_manager
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file with required environment variables:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///hospital.db
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

## Module Features

### Doctor Module
- View and manage appointments
- Write prescriptions
- Request laboratory tests
- View patient medical history
- Generate medical reports

### Pharmacy Module
- Manage medication inventory
- Process prescriptions
- Track stock levels
- Generate stock reports
- Manage medication dispensing

### Laboratory Module
- Process test requests
- Record and manage test results
- Generate lab reports
- Track sample status
- Manage test inventory

### Admin Module
- User management
- System configuration
- Report generation
- Audit trail monitoring
- Backup management

## Security Measures

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Secure session management
- Role-based access control
- Input validation and sanitization
- XSS protection
- Secure file uploads

## Development

### Running Tests
```bash
python -m pytest
```

### Creating Database Migrations
```bash
flask db migrate -m "Migration description"
flask db upgrade
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation and community
- Bootstrap for responsive design
- Font Awesome for icons
- All contributors who have helped with the project   flask run
   ```

7. Access the application at `http://localhost:5000`

## Default Admin Credentials

- Email: admin@hospital.com
- Password: admin123

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.