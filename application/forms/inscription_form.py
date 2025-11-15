from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TelField, SelectField, SelectMultipleField, DateField
from wtforms.validators import  DataRequired, Length, EqualTo, Email, Optional

# source d'inspiration: https://www.tresfacile.net/la-bibliotheque-wtforms-creation-des-formulaires-en-python/#3
#https://wtforms.readthedocs.io/en/2.3.x/fields/


class InscriptionForm(FlaskForm):
    
    nom = StringField('Nom',
        validators=[
            DataRequired(message='Le nom est requis'),
            Length(max=50)
        ],
        render_kw={'placeholder': 'Tremblay'}
    )
    
    prenom = StringField('Prénom',
        validators=[
            DataRequired(message='Le prénom est requis'),
            Length(max=50)
        ],
        render_kw={'placeholder': 'Jean'}
    )
    
    nom_utilisateur = StringField('Nom d\'utilisateur', 
        validators=[
            DataRequired(message='Le nom d\'utilisateur est requis'),
            Length(min=3, max=50, message='Entre 3 et 50 caractères')
        ],
        render_kw={'placeholder': 'jean_tremblay'}
    )

    telephone = TelField('Téléphone',
        validators=[
            DataRequired(message='Le téléphone est requis')
        ],
        render_kw={'placeholder': '819-555-1234'}
    )
    
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
            ('livreur', 'Livreur (livrer des commandes)')
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
    
    confirm_password = PasswordField('Confirmer le mot de passe',
        validators=[
            DataRequired(message='Veuillez confirmer le mot de passe'),
            EqualTo('password', message='Les mots de passe doivent correspondre')
        ],
        render_kw={'placeholder': '••••••••'}
    )

    # ============================================
    # CHAMPS LIVREUR (optionnels par défaut)
    # ============================================
    
    type_piece = SelectField('Type de pièce d\'identité',
        coerce=str,  # source: https://wtforms.readthedocs.io/en/3.0.x/fields/#wtforms.fields.SelectField 
        validators=[Optional()],
        render_kw={'class': 'form-input'}
    )
    
    numero_piece = StringField('Numéro de pièce',
        validators=[Optional(), Length(max=255)],
        render_kw={'placeholder': 'L1234-567890-12345', 'class': 'form-input'}
    )
    
    date_expiration = DateField('Date d\'expiration',
        validators=[Optional()],
        render_kw={'class': 'form-input'}
    )
    
    zones = SelectMultipleField('Zones de livraison',
        coerce=str, # source: https://wtforms.readthedocs.io/en/3.0.x/fields/#wtforms.fields.SelectField 
        validators=[Optional()],
        render_kw={'class': 'form-input', 'size': '5'}
    )

      # ============================================
    # CHAMPS CLIENT (optionnels par défaut)
    # ============================================
    
    ville= StringField('Ville de résidence',
        validators=[Optional()],
        render_kw={'placeholder': 'Votre ville', 'class': 'form-input'}
    )
    
    rue= StringField('Numéro de la  rue',
        validators=[Optional()],
        render_kw={'placeholder': 'Votre ville', 'class': 'form-input'}
    )
    
    codePostal = StringField('Code postal',
        validators=[Optional()],
        render_kw={'placeholder': 'A1A 1A1', 'class': 'form-input'}
    )
        
    submit = SubmitField('S\'inscrire')