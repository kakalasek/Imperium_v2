from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ApiForm(FlaskForm):
    endpoint = StringField('API Endpoint', 
                            validators=[DataRequired()])
    submit = SubmitField('Test')

class ScanForm(FlaskForm):
    ip = StringField('IP Adress or Range',
                       validators=[DataRequired()])
    scan_type = SelectField("Scan Type", choices=[('-sS', 'Syn Scan'), ('-sV', 'Version Scan'), ('-O', 'System Scan'), ('-sF', 'Fin Scan'), ('-sU', 'UDP Scan'), ('-sT', 'Connect Scan')])
    submit = SubmitField('Scan')