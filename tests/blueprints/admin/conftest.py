"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.

Fixtures specific to admin blueprints
"""

import pytest

from tests.base import CONFIG_FILENAME_TEST_ADMIN, create_app
from tests.conftest import database_recreated


@pytest.fixture(scope='session')
def admin_app_without_db(db):
    app = create_app(CONFIG_FILENAME_TEST_ADMIN)
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def app(admin_app_without_db, db):
    app = admin_app_without_db
    with database_recreated(db):
        yield app
