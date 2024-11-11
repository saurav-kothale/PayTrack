from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from app.Inventory_in.model import InvoiceDetailsDB
from app.product.model.model import InvoiceProductsDB
from app.Inventory_in.master_product.model import MasterProductDB
import calendar

async def get_invoice_with_products_and_bikes(db, invoice_id: str):
    result = await db.execute(
        select(InvoiceDetailsDB)
        .options(
            joinedload(InvoiceDetailsDB.products)
            .joinedload(InvoiceProductsDB.master_product)
            .joinedload(MasterProductDB.bikes)  # Load related Bike details
        )
        .where(InvoiceDetailsDB.invoice_id == invoice_id)
    )
    invoice = result.scalars().first()
    return invoice


def get_month_abbreviation(month_number):
    return calendar.month_abbr[month_number]