"""
byceps.blueprints.admin.news.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import re

from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional, Regexp

from ....util.l10n import LocalizedForm


SLUG_REGEX = re.compile('^[a-z0-9-]+$')


class ChannelCreateForm(LocalizedForm):
    channel_id = StringField('ID', validators=[Length(min=1, max=40)])
    url_prefix = StringField('URL-Präfix', [InputRequired(), Length(max=80)])


class ItemCreateForm(LocalizedForm):
    slug = StringField('Slug', [InputRequired(), Length(max=100), Regexp(SLUG_REGEX, message='Nur Kleinbuchstaben, Ziffern und Bindestrich sind erlaubt.')])
    title = StringField('Titel', [InputRequired(), Length(max=100)])
    body = TextAreaField('Text', [InputRequired()])
    image_url_path = StringField('Bild-URL-Pfad', [Optional(), Length(max=100)])


class ItemUpdateForm(ItemCreateForm):
    pass
