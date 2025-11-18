from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField,  SelectMultipleField
from wtforms.validators import  DataRequired, optional
from wtforms import widgets

class Commander(FlaskForm):
    
    taille = RadioField ( 'Taille de la pizza',
        coerce=str,
        validators=[DataRequired(message='Choisissez une taille de pizza')]    
    )
    
    sauce = RadioField ( 'Sauce de la pizza',
        coerce=str,
        validators=[DataRequired(message='Choisissez une sauce de pizza')]    
    )

    croute = RadioField ( 'Croûte de la pizza',
        coerce=str,
        validators=[DataRequired(message='Choisissez une croûte de pizza')]    
    )

    garnitures = SelectMultipleField(
        'Garnitures de la pizza',
        coerce=str,
        option_widget=widgets.CheckboxInput(),  
        widget=widgets.ListWidget(prefix_label=False),
        validators=[optional()]
    )


    
    submit = SubmitField('Ajouter au panier')