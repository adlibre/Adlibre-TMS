# -*- coding: utf-8 -*-

import xml_models

from saasu_client import DEFAULT_GET_URL
from saasu_client.models.base import BaseModel, CollectionField

__all__ = ['TransactionCategory', 'TransactionCategoryList']


class TransactionCategory(xml_models.Model):
    """ Transaction Category Entity """

    __model__ = 'TransactionCategory'

    uid = xml_models.IntField(xpath='/transactionCategoryResponse/transactionCategory/@uid', default=0)
    lastUpdatedUid = xml_models.CharField(xpath='/transactionCategoryResponse/transactionCategory/@lastUpdatedUid')
    name = xml_models.CharField(xpath='/transactionCategoryResponse/transactionCategory/name')
    # Valid value is one of the following:
    # Income, Expense, Asset, Equity, Liability, Other Income, Other Expense, Cost of Sales
    type = xml_models.CharField(xpath='/transactionCategoryResponse/transactionCategory/type')
    isActive = xml_models.BoolField(xpath='/transactionCategoryResponse/transactionCategory/isActive', default=True) 

    finders = {
        (uid,) : DEFAULT_GET_URL % __model__ + "&uid=%s",
        }


class TransactionCategoryListItem(xml_models.Model):
    """ Transaction Category List Item Entity """

    uid = xml_models.IntField(xpath='/transactionCategoryListItem/transactionCategoryUid', default=0)
    lastUpdatedUid = xml_models.CharField(xpath='/transactionCategoryListItem/lastUpdatedUid')
    name = xml_models.CharField(xpath='/transactionCategoryListItem/name')
    # Valid value is one of the following:
    # Income, Expense, Asset, Equity, Liability, Other Income, Other Expense, Cost of Sales
    type = xml_models.CharField(xpath='/transactionCategoryListItem/type')
    isActive = xml_models.BoolField(xpath='/transactionCategoryListItem/isActive', default=True) 
    # Inbuilt Accounts are system-wide Accounts that are shared across all Files.
    isInbuilt = xml_models.BoolField(xpath='/transactionCategoryListItem/isInbuilt', default=True) 


class TransactionCategoryList(BaseModel):
    """ List of Transaction Categories """

    __model__ = 'TransactionCategoryList'

    items = CollectionField(TransactionCategoryListItem, xpath='/transactionCategoryListResponse/transactionCategoryList/transactionCategoryListItem')

    # Valid value is one of the following:
    # Income, Expense, Asset, Equity, Liability, Other Income, Other Expense, Cost of Sales
    type = xml_models.CharField(xpath='/transactionCategoryListResponse/transactionCategoryList/transactionCategoryListItem/type')
    isActive = xml_models.BoolField(xpath='/transactionCategoryListResponse/transactionCategoryList/transactionCategoryListItem/isActive', default=True) 
    # Inbuilt Accounts are system-wide Accounts that are shared across all Files.
    isInbuilt = xml_models.BoolField(xpath='/transactionCategoryListResponse/transactionCategoryList/transactionCategoryListItem/isInbuilt', default=True) 

    finders = {
        (type,) : DEFAULT_GET_URL % __model__ + "&type=%s",
        (isActive,) : DEFAULT_GET_URL % __model__ + "&isActive=%s",
        (isActive, type) : DEFAULT_GET_URL % __model__ + "&isActive=%s&type=%s",
        (isInbuilt,) : DEFAULT_GET_URL % __model__ + "&isInbuilt=%s",
        }

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()
