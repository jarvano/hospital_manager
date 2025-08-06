from app import create_app, db
from app.models import User, Patient, Appointment, Prescription, Medication, LabTest

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Patient': Patient,
        'Appointment': Appointment,
        'Prescription': Prescription,
        'Medication': Medication,
        'LabTest': LabTest
    }

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])