import os

from dotenv import load_dotenv

load_dotenv()
from dto.columns_main_dto import ColumnsMainDTO
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO

columns_main = ColumnsMainDTO()
columns_nomenclature = ColumnsNomenclatureDTO()

BASE_URLS = {
    'live': 'https://api-b2b.lamoda.ru',
    'demo': 'https://api-demo-b2b.lamoda.ru',
}

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

LIMIT_NOMENCLATURE = 1000
LIMIT_STOCK = 1000
LIMIT_ORDER = 1000
TIME_SLEEP_NOMENCLATURES = 20
TIME_SLEEP_STOCK = 20
TIME_SLEEP_ORDER = 20
TIME_SLEEP_ORDER_INFO = 0.1

BASE_COLUMNS_NAME = {'id': columns_main.id,
                     'paymentMethod': columns_main.payment_method,
                     'status': columns_main.status,
                     'sku': columns_main.sku,
                     'lamodaSku': columns_main.lamoda_sku,
                     'status_product': columns_main.status_product,
                     'totalDiscount': columns_main.total_discount,
                     'salePrice': columns_main.sale_price,
                     'paidPrice': columns_main.paid_price,
                     'basePrice': columns_main.base_price,
                     'couponDiscount': columns_main.coupon_discount,
                     'loyaltyDiscount': columns_main.loyalty_discount,
                     'partnerAgreedDiscount': columns_main.partner_agreed_discount,
                     'otherDiscounts': columns_main.other_discounts,
                     'platformDiscounts': columns_main.platform_discounts,
                     'partnerAgreedPrice': columns_main.partner_agreed_price,
                     'city': columns_main.city,
                     'shippingMethodCode': columns_main.shipping_method_code,
                     'comment': columns_main.comment,
                     'currency': columns_main.currency,
                     'shopName': columns_main.shop_name,
                     'quantity': columns_main.stock,
                     'supplier_sku': columns_nomenclature.supplier_sku,
                     'supplier_parent_sku': columns_nomenclature.supplier_parent_sku,
                     'brand': columns_nomenclature.brand,
                     'color': columns_nomenclature.color,
                     'barcode': columns_nomenclature.barcode,
                     'name': columns_nomenclature.name,
                     'createdAt': columns_nomenclature.created_at,
                     'updatedAt': columns_nomenclature.updated_at,
                     'isSellable': columns_nomenclature.is_sellable,
                     'description': columns_main.description,
                     'supplierParentSku': columns_nomenclature.supplier_parent_sku,
                     'supplier_size': columns_nomenclature.supplier_size,
                     'lamodaSubCategory': columns_nomenclature.lamoda_sub_category,
                     }
