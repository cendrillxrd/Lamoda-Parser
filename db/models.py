from sqlalchemy import Column, Date, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LamodaOrdersModel(Base):
    """
    Заказы Lamoda, одна строка на позицию заказа.

    Внутри одного заказа может быть несколько строк с одинаковым (id, sku) — например,
    товар заказан в нескольких экземплярах как отдельные позиции. 'position' — порядковый
    номер повторения такой пары (аналог composite-key решения из order_collector),
    вычисляется в LamodaOrdersRepository перед записью.

    PK назван record_id (а не id), потому что бизнес-колонка 'Номер заказа' в DTO
    называется именно 'id' — иначе имя конфликтовало бы с атрибутом модели.
    """
    __tablename__ = 'lamoda_orders'

    record_id = Column(Integer, primary_key=True, autoincrement=True)

    id = Column(String(64), nullable=False)  # Номер заказа
    sku = Column(String(255), nullable=False)  # Артикул товара
    position = Column(Integer, nullable=False)  # порядковый номер повторения (id, sku)

    shop_name = Column(String(255))
    created_at = Column(String(64))
    updated_at = Column(String(64))
    status = Column(String(100))
    supplier_parent_sku = Column(String(255))
    description = Column(String(500))
    collection = Column(String(255))
    size = Column(String(50))
    status_product = Column(String(100))
    payment_method = Column(String(100))
    total_discount = Column(Float)
    sale_price = Column(Float)
    paid_price = Column(Float)
    base_price = Column(Float)
    coupon_discount = Column(Float)
    loyalty_discount = Column(Float)
    partner_agreed_discount = Column(Float)
    other_discounts = Column(Float)
    platform_discounts = Column(Float)
    partner_agreed_price = Column(Float)
    city = Column(String(255))
    shipping_method_code = Column(String(100))

    __table_args__ = (
        UniqueConstraint('id', 'sku', 'position', name='uq_lamoda_orders_id_sku_position'),
    )


class LamodaNomenclatureModel(Base):
    """
    Номенклатура Lamoda, одна строка на артикул на дату.

    Заменяет сразу два старых CSV (накопительный 'Номенклатура' и снэпшот
    'Последняя номенклатура') — в БД это одна и та же таблица: история накапливается
    сама по себе, а "последний снэпшот" — это просто запрос с MAX(date) при необходимости.
    """
    __tablename__ = 'lamoda_nomenclature'

    id = Column(Integer, primary_key=True, autoincrement=True)

    supplier_sku = Column(String(255), nullable=False)
    supplier_parent_sku = Column(String(255))
    brand = Column(String(255))
    supplier_size = Column(String(50))
    date = Column(Date, nullable=False)
    quantity = Column(Integer)
    on_the_way = Column(Integer)
    total_quantity = Column(Integer)
    barcode = Column(String(255))
    name = Column(String(500))
    lamoda_sub_category = Column(String(255))
    created_at = Column(String(64))
    updated_at = Column(String(64))
    status = Column(String(100))
    collection = Column(String(255))
    price = Column(Float)

    __table_args__ = (
        UniqueConstraint('supplier_sku', 'date', name='uq_lamoda_nomenclature_sku_date'),
    )
