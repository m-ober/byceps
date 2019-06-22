"""
byceps.blueprints.site_admin.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from wtforms import StringField
from wtforms.validators import Length

from ...util.l10n import LocalizedForm


class UpdateForm(LocalizedForm):
    title = StringField('Titel', validators=[Length(min=1, max=20)])


class CreateForm(UpdateForm):
    id = StringField('ID', validators=[Length(min=1, max=40)])