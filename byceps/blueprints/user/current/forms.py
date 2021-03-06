"""
byceps.blueprints.user.current.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from wtforms import DateField, StringField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Length, Optional

from ....util.l10n import LocalizedForm


class DetailsForm(LocalizedForm):
    first_names = StringField('Vorname(n)', [InputRequired(), Length(min=2)])
    last_name = StringField('Nachname', [InputRequired(), Length(min=2, max=80)])
    date_of_birth = DateField('Geburtsdatum',
                              [Optional()],
                              format='%d.%m.%Y')
    country = StringField('Land', [Optional(), Length(max=60)])
    zip_code = StringField('PLZ', [Optional()])
    city = StringField('Stadt', [Optional()])
    street = StringField('Straße', [Optional()])
    phone_number = TelField('Telefonnummer', [Optional(), Length(max=20)])
