from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Elderly, TaskReminder, HealthData, Caregiver, EmergencyAlert
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caremate.db'
db.init_app(app)

# Form for adding a new task reminder
class TaskReminderForm(FlaskForm):
    task_name = StringField('Task Name', validators=[InputRequired()])
    task_time = StringField('Task Time (HH:MM)', validators=[InputRequired()])
    submit = SubmitField('Add Task')

@app.route('/')
def index():
    elderly_people = Elderly.query.all()
    return render_template('index.html', elderly_people=elderly_people)

@app.route('/elderly/<int:id>')
def elderly_profile(id):
    elderly = Elderly.query.get_or_404(id)
    task_reminders = TaskReminder.query.filter_by(elderly_id=id).all()
    return render_template('elderly_profile.html', elderly=elderly, task_reminders=task_reminders)

@app.route('/add_task/<int:id>', methods=['GET', 'POST'])
def add_task(id):
    form = TaskReminderForm()
    if form.validate_on_submit():
        new_task = TaskReminder(
            elderly_id=id,
            task_name=form.task_name.data,
            task_time=form.task_time.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('elderly_profile', id=id))
    return render_template('add_task.html', form=form)

@app.route('/health_tracking/<int:id>')
def health_tracking(id):
    health_data = HealthData.query.filter_by(elderly_id=id).all()
    return render_template('health_tracking.html', health_data=health_data)

@app.route('/caregiver_marketplace')
def caregiver_marketplace():
    caregivers = Caregiver.query.filter_by(verified=True).all()
    return render_template('caregiver_marketplace.html', caregivers=caregivers)

@app.route('/emergency_alerts/<int:id>')
def emergency_alerts(id):
    alerts = EmergencyAlert.query.filter_by(elderly_id=id).all()
    return render_template('emergency_alerts.html', alerts=alerts)

@app.route('/send_emergency_alert/<int:id>', methods=['POST'])
def send_emergency_alert(id):
    description = request.form['description']
    new_alert = EmergencyAlert(
        elderly_id=id,
        alert_time=datetime.datetime.now(),
        description=description
    )
    db.session.add(new_alert)
    db.session.commit()
    return redirect(url_for('emergency_alerts', id=id))

if __name__ == '__main__':
    app.run(debug=True)
