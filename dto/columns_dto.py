from dataclasses import asdict, dataclass


@dataclass
class ColumnsDTO:
    id: str = 'Номер заказа'
    payment_method: str = 'Метод оплаты'
    status: str = 'Статус'
    sku: str = 'Артикул товара'
    lamoda_sku: str = 'Артикул товара (LAMODA)'
    status_product: str = 'Описание товара'
    total_discount: str = 'Итого сумма скидок'
    sale_price: str = 'Цена со скидкой'
    paid_price: str = 'Цена продажи'
    base_price: str = 'Цена без скидки'
    coupon_discount: str = 'Скидка по купону'
    loyalty_discount: str = 'Скидка по лояльности'
    partner_agreed_discount: str = 'Скидка согласованная с партнером'
    other_discounts: str = 'Прочие скидки'
    platform_discounts: str = 'Платформенные скидки'
    partner_agreed_price: str = 'Цена согласованная с партнером'
    city: str = 'Населенный пункт'
    shipping_method_code: str = 'Метод доставки',
    comment: str = 'Комментарий (для ТП)',
    currency: str = 'Валюта'
    shop_name: str = 'Партнер'
    created_at: str = 'Дата создания'
    updated_at: str = 'Дата изменения'
    stock: str = 'Остаток'
