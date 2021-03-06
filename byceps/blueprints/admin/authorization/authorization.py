"""
byceps.blueprints.admin.authorization.authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.util.authorization import create_permission_enum


RolePermission = create_permission_enum('role', [
    'assign',
    'view',
])
