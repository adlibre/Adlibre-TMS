# -*- coding: utf-8 -*-

import xml_models

from saasu_client import DEFAULT_GET_URL
from saasu_client.models.base import BaseModel, CollectionField

__all__ = ['ServiceInvoice', 'ServiceInvoiceItem', 'ItemInvoice', 'ItemInvoiceItem',
           'ServicePurchase']


class ServiceInvoiceItem(BaseModel):
    """ Service Invoice Item Entity """

    __model__ = 'ServiceInvoiceItem'
    template_name = 'saasu_client/serviceinvoiceitem_model.xml'

    # Description of service invoice line item. Use pipe (|) character to indicate new line.
    description = xml_models.CharField(xpath="/serviceInvoiceItem/description") 
    # The Account for this line item.
    accountUid = xml_models.IntField(xpath="/serviceInvoiceItem/accountUid") 
    # Must be one of the tax codes in your file. Invalid tax code will be ignored.
    taxCode = xml_models.CharField(xpath="/serviceInvoiceItem/taxCode") 
    # The total amount (tax inclusive) for this line item. Positive, negative, and 0 are accepted. Maximum 2 decimals.
    totalAmountInclTax = xml_models.FloatField(xpath="/serviceInvoiceItem/totalAmountInclTax", default=0) 


class ServiceInvoice(BaseModel):
    """ Service Invoice Entity """

    __model__ = 'Invoice'
    template_name = 'saasu_client/serviceinvoice_model.xml'

    uid = xml_models.IntField(xpath="/invoiceResponse/invoice/@uid", default=0) 
    lastUpdatedUid = xml_models.CharField(xpath="/invoiceResponse/invoice/@lastUpdatedUid")
    # Either S for Sale or P for Purchase.
    transactionType = xml_models.CharField(xpath="/invoiceResponse/invoice/transactionType", default="S")
    # The invoice date.
    date = xml_models.DateField(xpath="/invoiceResponse/invoice/date", date_format="%Y-%m-%d") 
    # The contact for this invoice. 0 means no contact.
    contactUid = xml_models.IntField(xpath="/invoiceResponse/invoice/contactUid", default=0) 
    # The shipping contact for this invoice. Not specifying or 0 means no shipping contact.
    shipToContactUid = xml_models.IntField(xpath="/invoiceResponse/invoice/shipToContactUid", default=0) 
    # Separate multiple tags by comma. Max length for each tag is 35 characters.
    tags = xml_models.CharField(xpath="/invoiceResponse/invoice/tags", default='')
    # Don’t set this value in invoice because this field is not accessible from the UI.
    reference = xml_models.CharField(xpath="/invoiceResponse/invoice/reference", default='')
    # Brief summary of the invoice
    summary = xml_models.CharField(xpath="/invoiceResponse/invoice/summary", default='')
    # The currency of the particular invoice transaction.
    ccy = xml_models.CharField(xpath="/invoiceResponse/invoice/ccy", default='')
    # Indicates whether the FX rate for the invoice was set automatically.
    autoPopulateFxRate = xml_models.BoolField(xpath="/invoiceResponse/invoice/autoPopulateFxRate", default=False) 

    # The Foreign Currency(FC) to Base Currency(BC) FX Rate. If you are setting the FX rate manually, and only have the BC to FC FX
    # rate, then you should calculate the fcToBcFxRate for posting the transaction. For an example, if your base currency is AUD and 1
    # AUD = 0.89 USD, get the inverse by 1/0.89. So your fcToBcFxRate = 1.1235.
    fcToBcFxRate = xml_models.FloatField(xpath="/invoiceResponse/invoice/fcToBcFxRate", default=0) 
    notes = xml_models.CharField(xpath="/invoiceResponse/invoice/notes", default='')
    # Notes to be displayed on pdf.
    externalNotes = xml_models.CharField(xpath="/invoiceResponse/invoice/externalNotes", default='')
    requiresFollowUp = xml_models.BoolField(xpath="/invoiceResponse/invoice/requiresFollowUp", default=False) 
    # Invoice and/or order due date or quote expiry date.
    dueOrExpiryDate = xml_models.DateField(xpath="/invoiceResponse/invoice/dueOrExpiryDate", date_format="%Y-%m-%d") 

    # The invoice layout. Either S (Service) or I (Item)
    layout = xml_models.CharField(xpath="/invoiceResponse/invoice/layout", default='S')
    # Invoice status. Either Q (Quote), O (Order) or I (Invoice).
    status = xml_models.CharField(xpath="/invoiceResponse/invoice/status", default='I')
    # The sale invoice number. When inserting a sale, set to <Auto Number> to let the system generates the invoice number based on the preferences you set.
    invoiceNumber = xml_models.CharField(xpath="/invoiceResponse/invoice/invoiceNumber", default='')
    # The purchase order number (PO #). When inserting a purchase, set to <Auto Number> to let the system generates the PO# based on the preferences you set.
    purchaseOrderNumber = xml_models.CharField(xpath="/invoiceResponse/invoice/purchaseOrderNumber", default='')

    # TODO: Complete this part
    # quickPayment	 	 	 	Payment to be applied to this invoice.
    # payments	 	 	 	   All payments associated with this particular invoice, if incpayments is set to ‘true’ in the query string.

    # Indicates if the invoice has been sent/emailed to contact. This flag will be set to true automatically if the Invoice is sent successfully through the WSAPI.
    isSent = xml_models.BoolField(xpath="/invoiceResponse/invoice/isSent", default=False) 

    # You can include unlimited number of invoice items. For service invoice, use <ServiceInvoiceItem>?
    # For item invoice: use <ItemInvoiceItem>. You cannot mix the content of invoice items (i.e. having both <ServiceInvoiceItem> and <ItemInvoiceItem>).
    invoiceItems = CollectionField(ServiceInvoiceItem, xpath='/invoiceResponse/invoice/invoiceItems/serviceInvoiceItem')	 	 	 

    finders = {
        ('uid',): DEFAULT_GET_URL % __model__ + "&uid=%s",
        }


class ItemInvoiceItem(BaseModel):
    """ Item Invoice Item Entity """

    __model__ = 'ItemInvoiceItem'
    template_name = 'saasu_client/iteminvoiceitem_model.xml'

    # The quantity. Maximum 3 decimals.
    quantity = xml_models.FloatField(xpath="/itemInvoiceItem/quantity", default=0)
    # The inventory item for this invoice line item. This also covers
    # combo item. For combo item, use combo item uid.
    inventoryItemUid = xml_models.IntField(xpath="/itemInvoiceItem/inventoryItemUid", default=0) 
    # Description of service invoice line item. Use pipe (|) character to indicate new line.
    description = xml_models.CharField(xpath="/itemInvoiceItem/description") 
    # Must be one of the tax codes in your file. Invalid tax code will be ignored.
    taxCode = xml_models.CharField(xpath="/itemInvoiceItem/taxCode") 
    # Unit price of inventory item.
    unitPriceInclTax = xml_models.FloatField(xpath="/itemInvoiceItem/unitPriceInclTax", default=0) 
    # Percentage discount. E.g. for 10% off the unit price is set the value to 10.
    # Valid values: between 0 and 100.  Maximum 2 decimals.
    percentageDiscount = xml_models.IntField(xpath="/itemInvoiceItem/percentageDiscount", default=0) 


class ItemInvoice(BaseModel):
    """ Item Invoice Entity """

    __model__ = 'Invoice'
    template_name = 'saasu_client/iteminvoice_model.xml'

    uid = xml_models.IntField(xpath="/invoiceResponse/invoice/@uid", default=0) 
    lastUpdatedUid = xml_models.CharField(xpath="/invoiceResponse/invoice/@lastUpdatedUid")
    # Either S for Sale or P for Purchase.
    transactionType = xml_models.CharField(xpath="/invoiceResponse/invoice/transactionType", default="S")
    # The invoice date.
    date = xml_models.DateField(xpath="/invoiceResponse/invoice/date", date_format="%Y-%m-%d") 
    # The contact for this invoice. 0 means no contact.
    contactUid = xml_models.IntField(xpath="/invoiceResponse/invoice/contactUid", default=0) 
    # The shipping contact for this invoice. Not specifying or 0 means no shipping contact.
    shipToContactUid = xml_models.IntField(xpath="/invoiceResponse/invoice/shipToContactUid", default=0) 
    # Separate multiple tags by comma. Max length for each tag is 35 characters.
    tags = xml_models.CharField(xpath="/invoiceResponse/invoice/tags", default='')
    # Don’t set this value in invoice because this field is not accessible from the UI.
    reference = xml_models.CharField(xpath="/invoiceResponse/invoice/reference", default='')
    # Brief summary of the invoice
    summary = xml_models.CharField(xpath="/invoiceResponse/invoice/summary", default='')
    # The currency of the particular invoice transaction.
    ccy = xml_models.CharField(xpath="/invoiceResponse/invoice/ccy", default='')
    # Indicates whether the FX rate for the invoice was set automatically.
    autoPopulateFxRate = xml_models.BoolField(xpath="/invoiceResponse/invoice/autoPopulateFxRate", default=False) 

    # The Foreign Currency(FC) to Base Currency(BC) FX Rate. If you are setting the FX rate manually, and only have the BC to FC FX
    # rate, then you should calculate the fcToBcFxRate for posting the transaction. For an example, if your base currency is AUD and 1
    # AUD = 0.89 USD, get the inverse by 1/0.89. So your fcToBcFxRate = 1.1235.
    fcToBcFxRate = xml_models.FloatField(xpath="/invoiceResponse/invoice/fcToBcFxRate", default=0) 
    notes = xml_models.CharField(xpath="/invoiceResponse/invoice/notes", default='')
    # Notes to be displayed on pdf.
    externalNotes = xml_models.CharField(xpath="/invoiceResponse/invoice/externalNotes", default='')
    requiresFollowUp = xml_models.BoolField(xpath="/invoiceResponse/invoice/requiresFollowUp", default=False) 
    # Invoice and/or order due date or quote expiry date.
    dueOrExpiryDate = xml_models.DateField(xpath="/invoiceResponse/invoice/dueOrExpiryDate", date_format="%Y-%m-%d") 

    # The invoice layout. Either S (Service) or I (Item)
    layout = xml_models.CharField(xpath="/invoiceResponse/invoice/layout", default='I')
    # Invoice status. Either Q (Quote), O (Order) or I (Invoice).
    status = xml_models.CharField(xpath="/invoiceResponse/invoice/status", default='I')
    # The sale invoice number. When inserting a sale, set to <Auto Number> to let the system generates the invoice number based on the preferences you set.
    invoiceNumber = xml_models.CharField(xpath="/invoiceResponse/invoice/invoiceNumber", default='')
    # The purchase order number (PO #). When inserting a purchase, set to <Auto Number> to let the system generates the PO# based on the preferences you set.
    purchaseOrderNumber = xml_models.CharField(xpath="/invoiceResponse/invoice/purchaseOrderNumber", default='')

    # TODO: Complete this part
    # quickPayment	 	 	 	Payment to be applied to this invoice.
    # payments	 	 	 	   All payments associated with this particular invoice, if incpayments is set to ‘true’ in the query string.

    # Indicates if the invoice has been sent/emailed to contact. This flag will be set to true automatically if the Invoice is sent successfully through the WSAPI.
    isSent = xml_models.BoolField(xpath="/invoiceResponse/invoice/isSent", default=False) 

    # You can include unlimited number of invoice items. For service invoice, use <ServiceInvoiceItem>?
    # For item invoice: use <ItemInvoiceItem>. You cannot mix the content of invoice items (i.e. having both <ServiceInvoiceItem> and <ItemInvoiceItem>).
    invoiceItems = CollectionField(ItemInvoiceItem, xpath='/invoiceResponse/invoice/invoiceItems/itemInvoiceItem')	 	 	 

    finders = {
        ('uid',): DEFAULT_GET_URL % __model__ + "&uid=%s",
        }


class ServicePurchase(BaseModel):
    """ Service Purchase Entity """

    __model__ = 'Invoice'
    template_name = 'saasu_client/servicepurchase_model.xml'

    uid = xml_models.IntField(xpath="/invoiceResponse/invoice/@uid", default=0) 
    lastUpdatedUid = xml_models.CharField(xpath="/invoiceResponse/invoice/@lastUpdatedUid")
    # Either S for Sale or P for Purchase.
    transactionType = xml_models.CharField(xpath="/invoiceResponse/invoice/transactionType", default="P")
    # The invoice date.
    date = xml_models.DateField(xpath="/invoiceResponse/invoice/date", date_format="%Y-%m-%d") 
    # The contact for this invoice. 0 means no contact.
    contactUid = xml_models.IntField(xpath="/invoiceResponse/invoice/contactUid", default=0) 
    # The shipping contact for this invoice. Not specifying or 0 means no shipping contact.
    shipToContactUid = xml_models.IntField(xpath="/invoiceResponse/invoice/shipToContactUid", default=0) 
    # Separate multiple tags by comma. Max length for each tag is 35 characters.
    tags = xml_models.CharField(xpath="/invoiceResponse/invoice/tags", default='')
    # Don’t set this value in invoice because this field is not accessible from the UI.
    reference = xml_models.CharField(xpath="/invoiceResponse/invoice/reference", default='')
    # Brief summary of the invoice
    summary = xml_models.CharField(xpath="/invoiceResponse/invoice/summary", default='')
    # The currency of the particular invoice transaction.
    ccy = xml_models.CharField(xpath="/invoiceResponse/invoice/ccy", default='')
    # Indicates whether the FX rate for the invoice was set automatically.
    autoPopulateFxRate = xml_models.BoolField(xpath="/invoiceResponse/invoice/autoPopulateFxRate", default=False) 

    # The Foreign Currency(FC) to Base Currency(BC) FX Rate. If you are setting the FX rate manually, and only have the BC to FC FX
    # rate, then you should calculate the fcToBcFxRate for posting the transaction. For an example, if your base currency is AUD and 1
    # AUD = 0.89 USD, get the inverse by 1/0.89. So your fcToBcFxRate = 1.1235.
    fcToBcFxRate = xml_models.FloatField(xpath="/invoiceResponse/invoice/fcToBcFxRate", default=0) 
    notes = xml_models.CharField(xpath="/invoiceResponse/invoice/notes", default='')
    # Notes to be displayed on pdf.
    externalNotes = xml_models.CharField(xpath="/invoiceResponse/invoice/externalNotes", default='')
    requiresFollowUp = xml_models.BoolField(xpath="/invoiceResponse/invoice/requiresFollowUp", default=False) 
    # Invoice and/or order due date or quote expiry date.
    dueOrExpiryDate = xml_models.DateField(xpath="/invoiceResponse/invoice/dueOrExpiryDate", date_format="%Y-%m-%d") 

    # The invoice layout. Either S (Service) or I (Item)
    layout = xml_models.CharField(xpath="/invoiceResponse/invoice/layout", default='S')
    # Invoice status. Either Q (Quote), O (Order) or I (Invoice).
    status = xml_models.CharField(xpath="/invoiceResponse/invoice/status", default='O')
    # The sale invoice number. When inserting a sale, set to <Auto Number> to let the system generates the invoice number based on the preferences you set.
    invoiceNumber = xml_models.CharField(xpath="/invoiceResponse/invoice/invoiceNumber", default='')
    # The purchase order number (PO #). When inserting a purchase, set to <Auto Number> to let the system generates the PO# based on the preferences you set.
    purchaseOrderNumber = xml_models.CharField(xpath="/invoiceResponse/invoice/purchaseOrderNumber", default='')

    # TODO: Complete this part
    # quickPayment	 	 	 	Payment to be applied to this invoice.
    # payments	 	 	 	   All payments associated with this particular invoice, if incpayments is set to ‘true’ in the query string.

    # Indicates if the invoice has been sent/emailed to contact. This flag will be set to true automatically if the Invoice is sent successfully through the WSAPI.
    isSent = xml_models.BoolField(xpath="/invoiceResponse/invoice/isSent", default=False) 

    # You can include unlimited number of invoice items. For service invoice, use <ServiceInvoiceItem>?
    # For item invoice: use <ItemInvoiceItem>. You cannot mix the content of invoice items (i.e. having both <ServiceInvoiceItem> and <ItemInvoiceItem>).
    invoiceItems = CollectionField(ServiceInvoiceItem, xpath='/invoiceResponse/invoice/invoiceItems/serviceInvoiceItem')	 	 	 

    finders = {
        ('uid',): DEFAULT_GET_URL % __model__ + "&uid=%s",
        }
