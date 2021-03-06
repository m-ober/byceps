"""
byceps.blueprints.api.tourney.avatar.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from wtforms import FileField, StringField
from wtforms.validators import InputRequired

from .....util.l10n import LocalizedForm


class CreateForm(LocalizedForm):
    party_id = StringField('Party-ID', [InputRequired()])
    creator_id = StringField('User-ID', [InputRequired()])
    image = FileField('Bilddatei', [InputRequired()])
