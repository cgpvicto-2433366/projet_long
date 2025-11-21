from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import  DataRequired, Length, Email

# source d'inspiration: https://www.tresfacile.net/la-bibliotheque-wtforms-creation-des-formulaires-en-python/#3
#https://wtforms.readthedocs.io/en/2.3.x/fields/


class ConnexionForm(FlaskForm):    
 
    courriel = StringField('Courriel',
        validators=[
            DataRequired(message='Le courriel est requis'),
            Email(message='Courriel invalide')
        ],
        render_kw={'placeholder': 'jean.tremblay@email.com'}
    )
    
    type_compte = SelectField('Type de compte',
        choices=[
            ('', '-- Choisir --'),
            ('client', 'Client (commander des pizzas)'),
            ('livreur', 'Livreur (livrer des commandes)'),
            ('administrateur', 'Gestionnaire de la pizzaria')
        ],
        validators=[DataRequired(message='Choisissez un type de compte')]
    )

    password = PasswordField('Mot de passe',
        validators=[
            DataRequired(message='Le mot de passe est requis'),
            Length(min=6, message='Minimum 6 caractères')
        ],
        render_kw={'placeholder': '••••••••'}
    )
    
    submit = SubmitField('Se connecter')