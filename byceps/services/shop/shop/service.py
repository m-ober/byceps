"""
byceps.services.shop.shop.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from typing import List, Optional, Set

from ....database import db

from .models import Shop as DbShop
from .transfer.models import Shop, ShopID


class UnknownShopId(ValueError):
    pass


def create_shop(shop_id: ShopID, title: str, email_config_id: str) -> Shop:
    """Create a shop."""
    shop = DbShop(shop_id, title, email_config_id)

    db.session.add(shop)
    db.session.commit()

    return _db_entity_to_shop(shop)


def find_shop(shop_id: ShopID) -> Optional[Shop]:
    """Return the shop with that id, or `None` if not found."""
    shop = DbShop.query.get(shop_id)

    if shop is None:
        return None

    return _db_entity_to_shop(shop)


def get_shop(shop_id: ShopID) -> Shop:
    """Return the shop with that id, or raise an exception."""
    shop = find_shop(shop_id)

    if shop is None:
        raise UnknownShopId(shop_id)

    return shop


def find_shops(shop_ids: Set[ShopID]) -> List[Shop]:
    """Return the shops with those IDs."""
    if not shop_ids:
        return []

    shops = DbShop.query \
        .filter(DbShop.id.in_(shop_ids)) \
        .all()

    return [_db_entity_to_shop(shop) for shop in shops]


def get_all_shops() -> List[Shop]:
    """Return all shops."""
    shops = DbShop.query.all()

    return [_db_entity_to_shop(shop) for shop in shops]


def get_active_shops() -> List[Shop]:
    """Return all shops that are not archived."""
    shops = DbShop.query \
        .filter_by(archived=False) \
        .all()

    return [_db_entity_to_shop(shop) for shop in shops]


def _db_entity_to_shop(shop: DbShop) -> Shop:
    return Shop(
        shop.id,
        shop.title,
        shop.email_config_id,
        shop.closed,
        shop.archived,
    )
