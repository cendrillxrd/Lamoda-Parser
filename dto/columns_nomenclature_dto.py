from dataclasses import asdict, dataclass


@dataclass
class ColumnsNomenclatureDTO:
    supplier_sku: str = 'Артикул товара'
    supplier_parent_sku: str = 'Родительский артикул товара'
    brand: str = 'Бренд'
    supplier_size: str = 'Размер'
    date: str = 'Дата сбора данных'
    quantity: str = 'Остаток'
    on_the_way: str = 'В пути'
    total_quantity: str = 'Общий остаток'
    color: str = 'Цвет'
    barcode: str = 'Баркод'
    name: str = 'Наименование'
    lamoda_sub_category: str = 'Категория (LAMODA)'
    created_at: str = 'Дата создания'
    updated_at: str = 'Дата изменения'
    status: str = 'Статус'
    is_sellable: str = 'Продается?'
    collection: str = 'Коллекция'
    price: str = 'Цена'
