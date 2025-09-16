import os

from dotenv import load_dotenv

load_dotenv()
from dto.columns_dto import ColumnsDTO

columns = ColumnsDTO()

BASE_URLS = {
    'live': 'https://api-b2b.lamoda.ru',
    'demo': 'https://api-demo-b2b.lamoda.ru',
}

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

LIMIT_NOMENCLATURE = 1000
LIMIT_STOCK = 1000
LIMIT_ORDER = 1000
TIME_SLEEP_NOMENCLATURES = 10
TIME_SLEEP_STOCK = 10
TIME_SLEEP_ORDER = 25
TIME_SLEEP_ORDER_INFO = 0.5

BASE_COLUMNS_NAME = {'id': columns.id,
                     'paymentMethod': columns.payment_method,
                     'status': columns.status,
                     'sku': columns.sku,
                     'lamodaSku': columns.lamoda_sku,
                     'status_product': columns.status_product,
                     'totalDiscount': columns.total_discount,
                     'salePrice': columns.sale_price,
                     'paidPrice': columns.paid_price,
                     'basePrice': columns.base_price,
                     'couponDiscount': columns.coupon_discount,
                     'loyaltyDiscount': columns.loyalty_discount,
                     'partnerAgreedDiscount': columns.partner_agreed_discount,
                     'otherDiscounts': columns.other_discounts,
                     'platformDiscounts': columns.platform_discounts,
                     'partnerAgreedPrice': columns.partner_agreed_price,
                     'city': columns.city,
                     'shippingMethodCode': columns.shipping_method_code,
                     'comment': columns.comment,
                     'currency': columns.currency,
                     'shopName': columns.shop_name,
                     'quantity': columns.stock
                     }

STATUS_PRODUCT = 'status_product'
