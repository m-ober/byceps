"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from pathlib import Path
from uuid import UUID

import pytest

from byceps.util.image.models import ImageType

from testfixtures.user import create_user
from testfixtures.user_avatar import create_avatar

from tests.helpers import app_context


@pytest.mark.parametrize('data_path, avatar_id, image_type, expected', [
    (
        Path('/var/byceps/data'),
        UUID('2e17cb15-d763-4f93-882a-371296a3c63f'),
        ImageType.jpeg,
        Path('/var/byceps/data/global/users/avatars/2e17cb15-d763-4f93-882a-371296a3c63f.jpeg'),
    ),
    (
        Path('/home/byceps/data'),
        UUID('f0266761-c37e-4519-8cb8-5812d2bfe595'),
        ImageType.png,
        Path('/home/byceps/data/global/users/avatars/f0266761-c37e-4519-8cb8-5812d2bfe595.png'),
    ),
])
def test_path(data_path, avatar_id, image_type, expected):
    user = create_user()

    avatar = create_avatar(user.id, id=avatar_id, image_type=image_type)

    with app_context() as app:
        app.config['PATH_DATA'] = data_path
        assert avatar.path == expected
