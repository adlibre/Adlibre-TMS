# -*- coding: utf-8 -*-

import xml_models

from saasu_client import DEFAULT_GET_URL
from saasu_client.models.base import BaseModel, CollectionField

__all__ = ['InventoryItem', 'FullInventoryItemList']


class InventoryItem(BaseModel):
    """ Inventory Item Entity """

    __model__ = 'InventoryItem'

    # Required for update.
    uid = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/@uid", default=0)
    # Required for update.
    lastUpdatedUid = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/@lastUpdatedUid")
    # Inventory item code. Must be unique.
    code = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/code")
    # Inventory item description.
    # Multi-line description is supported. Use the pipe (|) to indicate newline.
    description = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/description")
    # Default: True
    isActive = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isActive", default=True) 
    notes = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/notes")
    isInventoried = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isInventoried", default=False) 

    # Required only if IsInventoried is set to true. Accounts used must be of type Asset.
    assetAccountUid = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/assetAccountUid", default=0)
    # How many stocks on hand? This element is only used when you retrieve an Inventory Item from your File.
    # This value is ignored on insert and update.
    stockOnHand = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/stockOnHand", default=0)
    # Current stock value. This element is only used when you retrieve an Inventory Item from your File.
    # This value is ignored on insert and update.
    currentValue = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/currentValue", default=0)
    # Specifies if this item can be bought or not. Default: false (cannot be bought).
    isBought = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isBought", default=False)
    # Expense Account for tracking purchase.
    # Required only if the Inventory Item is not inventoried and item can be bought (isInventoried == false && isBought == true).
    # Accounts used must be of type Expense.
    purchaseExpenseAccountUid = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/purchaseExpenseAccountUid", default=0)
    # Default tax code when the inventory item is purchased.
    purchaseTaxCode = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/purchaseTaxCode")
    # Minimum stock level used for re-stocking alert report.
    minimumStockLevel = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/minimumStockLevel", default=0)

    # The primary supplier for this Inventory Item.
    primarySupplierContactUid = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/primarySupplierContactUid", default=0)
    # The primary supplier’s item code for this Inventory Item.
    primarySupplierItemCode = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/primarySupplierItemCode")
    # Default re-order quantity for re-stocking alert report.
    defaultReOrderQuantity = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/defaultReOrderQuantity", default=0)
    # Default buying price for the item. Only applicable if the Inventory Item is marked as bought.
    buyingPrice = xml_models.FloatField(xpath="/inventoryItemResponse/inventoryItem/buyingPrice", default=0)
    # A flag specifying whether the buying price includes/excludes tax.
    isBuyingPriceIncTax = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isBuyingPriceIncTax", default=True)
    # Specifies whether the Inventory Item can be sold or not. Default: false (cannot be sold).
    isSold = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isSold", default=True)
    # Account for tracking sales. Only required if the item can be sold (isSold == true). Accounts used must be of type Income.
    saleIncomeAccountUid = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/saleIncomeAccountUid", default=0)
    # Default tax code for sale.
    saleTaxCode = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/saleTaxCode")
    # Accounts for tracking cost of sales. Required only if Inventory Item is inventoried & for sale.
    # Accounts used must be of type Cost of Sales.
    saleCoSAccountUid = xml_models.IntField(xpath="/inventoryItemResponse/inventoryItem/saleCoSAccountUid", default=0)
    # The default selling price for this Inventory Item. Only applicable if the Inventory Item is marked as sold.
    sellingPrice = xml_models.FloatField(xpath="/inventoryItemResponse/inventoryItem/sellingPrice", default=0)
    isSellingPriceIncTax = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isSellingPriceIncTax", default=True) 

    # A flag that indicates this is an item you sell, that you haven’t bought or assembled as stock to make available for sale.
    isVirtual = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isVirtual", default=True)
    # The type if this item is marked as virtual.
    vType = xml_models.CharField(xpath="/inventoryItemResponse/inventoryItem/vType")
    # A flag to set the Item to visible, for an example this can be
    # used in your database so that Item is flagged to be displayed in your ecommerce product listings.
    isVisible = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isVisisble", default=False) 
    # A flag specifying whether this item is treated as a voucher.
    isVoucher = xml_models.BoolField(xpath="/inventoryItemResponse/inventoryItem/isVoucher", default=False) 

    # When the voucher becomes effective.
    validFrom = xml_models.DateField(xpath="/inventoryItemResponse/inventoryItem/validFrom", date_format="%Y-%m-%d")
    # When the voucher expires.
    validTo = xml_models.DateField(xpath="/inventoryItemResponse/inventoryItem/validTo", date_format="%Y-%m-%d") 

    finders = {
        (uid,): DEFAULT_GET_URL % __model__ + "&uid=%s",
        }


class InventoryListItem(xml_models.Model):
    """ Inventory List Item Entity """

    uid = xml_models.IntField(xpath="/inventoryItem/@uid", default=0)
    lastUpdatedUid = xml_models.CharField(xpath="/inventoryItem/@lastUpdatedUid")
    utcFirstCreated = xml_models.CharField(xpath="/inventoryItem/utcFirstCreated") 
    utcLastModified = xml_models.CharField(xpath="/inventoryItem/utcLastModified") 

    code = xml_models.CharField(xpath="/inventoryItem/code") 
    description = xml_models.CharField(xpath="/inventoryItem/description") 
    isActive = xml_models.BoolField(xpath="/inventoryItem/isActive", default=True) 
    isInventoried = xml_models.BoolField(xpath="/inventoryItem/isInventoried", default=False) 

    assetAccountUid = xml_models.IntField(xpath="/inventoryItem/assetAccountUid", default=0)
    stockOnHand = xml_models.IntField(xpath="/inventoryItem/stockOnHand", default=0)
    currentValue = xml_models.IntField(xpath="/inventoryItem/currentValue", default=0)
    quantityOnOrder = xml_models.IntField(xpath="/inventoryItem/quantityOnOrder", default=0)
    quantityCommited = xml_models.IntField(xpath="/inventoryItem/quantityCommited", default=0)

    isBought = xml_models.BoolField(xpath="/inventoryItem/isBought", default=False) 

    purchaseExpenseAccountUid = xml_models.IntField(xpath="/inventoryItem/purchaseExpenseAccountUid", default=0)
    minimumStockLevel = xml_models.IntField(xpath="/inventoryItem/minimumStockLevel", default=0)
    primarySupplierContactUid = xml_models.IntField(xpath="/inventoryItem/primarySupplierContactUid", default=0)
    defaultReOrderQuantity = xml_models.IntField(xpath="/inventoryItem/defaultReOrderQuantity", default=0)

    isSold = xml_models.BoolField(xpath="/inventoryItem/isSold", default=True) 

    saleIncomeAccountUid = xml_models.IntField(xpath="/inventoryItem/saleIncomeAccountUid", default=0)
    saleTaxCode = xml_models.CharField(xpath="/inventoryItem/saleTaxCode") 
    saleCoSAccountUid = xml_models.IntField(xpath="/inventoryItem/saleCoSAccountUid", default=0)
    sellingPrice = xml_models.FloatField(xpath="/inventoryItem/sellingPrice", default=0)

    isSellingPriceIncTax = xml_models.BoolField(xpath="/inventoryItem/isSellingPriceIncTax", default=True) 
    buyingPrice = xml_models.FloatField(xpath="/inventoryItem/buyingPrice", default=0)
    isBuyingPriceIncTax = xml_models.BoolField(xpath="/inventoryItem/isBuyingPriceIncTax", default=True) 
    isVoucher = xml_models.BoolField(xpath="/inventoryItem/isVoucher", default=False) 

    validFrom = xml_models.DateField(xpath="/inventoryItem/validFrom", date_format="%Y-%m-%d") 
    validTo = xml_models.DateField(xpath="/inventoryItem/validTo", date_format="%Y-%m-%d") 

    isVirtual = xml_models.BoolField(xpath="/inventoryItem/isVirtual", default=True) 
    isVisible = xml_models.BoolField(xpath="/inventoryItem/isVisisble", default=False) 

    
class FullInventoryItemList(BaseModel):
    """ Full Inventory Item List Entity """

    __model__ = 'FullInventoryItemList'
    
    items = CollectionField(InventoryListItem, xpath='/inventoryItemListResponse/inventoryItemList/inventoryItem')

    isActive = xml_models.BoolField(xpath="/inventoryItemListResponse/inventoryItemList/inventoryItem/isActive", default=True) 

    finders = {
        (isActive,) : DEFAULT_GET_URL % __model__ + "&isActive=%s",
        }

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()
