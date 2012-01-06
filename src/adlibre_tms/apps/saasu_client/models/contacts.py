# -*- coding: utf-8 -*-

import xml_models

from saasu_client import DEFAULT_GET_URL
from saasu_client.models.base import BaseModel, CollectionField

__all__ = ['Contact', 'ContactList']


class PostalAddress(xml_models.Model):
    """ Postal Address Entity """

    street = xml_models.CharField(xpath="/postalAddress/street") 
    city = xml_models.CharField(xpath="/postalAddress/city") 
    postCode = xml_models.CharField(xpath="/postalAddress/postCode") 
    state = xml_models.CharField(xpath="/postalAddress/state") 
    country = xml_models.CharField(xpath="/postalAddress/country") 

    
class Contact(BaseModel):
    """ Contact Entity """

    __model__ = 'Contact'
    template_name = 'saasu_client/contact_model.xml'

    uid = xml_models.IntField(xpath="/contactResponse/contact/@uid", default=0) 
    lastUpdatedUid = xml_models.CharField(xpath="/contactResponse/contact/@lastUpdatedUid")
    # A.K.A "Title" values; Mr., Mrs., Ms., Dr., Prof.
    salutation = xml_models.CharField(xpath="/contactResponse/contact/salutation")
    # A.K.A "First Name".
    givenName = xml_models.CharField(xpath="/contactResponse/contact/givenName") 
    # A.K.A. "Initial".
    middleInitials = xml_models.CharField(xpath="/contactResponse/contact/middleInitials") 
    # A.K.A "Last Name".
    familyName = xml_models.CharField(xpath="/contactResponse/contact/familyName") 
    # A.K.A. "Company".
    organizationName = xml_models.CharField(xpath="/contactResponse/contact/organizationName") 
    # A.K.A. "Business Number".
    organizationAbn = xml_models.CharField(xpath="/contactResponse/contact/organizationAbn") 
    # The organisation/company website url.
    organizationWebsite = xml_models.CharField(xpath="/contactResponse/contact/organizationWebsite") 
    organizationPosition = xml_models.CharField(xpath="/contactResponse/contact/organizationPosition") 

    # This is your own contact ID, different to Saasu's Contact Uid.
    contactID = xml_models.CharField(xpath="/contactResponse/contact/contactID")
    websiteUrl = xml_models.CharField(xpath="/contactResponse/contact/websiteUrl") 
    email = xml_models.CharField(xpath="/contactResponse/contact/email") 
    mainPhone = xml_models.CharField(xpath="/contactResponse/contact/mainPhone") 
    homePhone = xml_models.CharField(xpath="/contactResponse/contact/homePhone") 
    fax = xml_models.CharField(xpath="/contactResponse/contact/fax") 
    mobilePhone = xml_models.CharField(xpath="/contactResponse/contact/mobilePhone") 
    otherPhone = xml_models.CharField(xpath="/contactResponse/contact/otherPhone")
    # Separate multiple tags by comma. Max. length per tag is 35 characters.
    tags = xml_models.CharField(xpath="/contactResponse/contact/tags") 

    postalAddress = xml_models.OneToOneField(PostalAddress, xpath='/contactResponse/contact/postalAddress')	 	 	 
    otherAddress = xml_models.OneToOneField(PostalAddress, xpath='/contactResponse/contact/postalAddress')	 	 	 

    # Default: True
    isActive = xml_models.BoolField(xpath="/contactResponse/contact/isActive", default=True) 

    acceptDirectDeposit = xml_models.BoolField(xpath="/contactResponse/contact/acceptDirectDeposit") 
    directDepositAccountName = xml_models.CharField(xpath="/contactResponse/contact/directDepositAccountName") 
    directDepositBsb = xml_models.CharField(xpath="/contactResponse/contact/directDepositBsb") 
    directDepositAccountNumber = xml_models.CharField(xpath="/contactResponse/contact/directDepositAccountNumber") 

    acceptCheque = xml_models.BoolField(xpath="/contactResponse/contact/acceptCheque") 
    chequePayableTo = xml_models.CharField(xpath="/contactResponse/contact/chequePayableTo") 

    customField1 = xml_models.CharField(xpath="/contactResponse/contact/customField1") 
    customField2 = xml_models.CharField(xpath="/contactResponse/contact/customField2") 

    twitterID = xml_models.CharField(xpath="/contactResponse/contact/twitterID") 
    skypeID = xml_models.CharField(xpath="/contactResponse/contact/skypeID") 

    finders = {
        (uid,): DEFAULT_GET_URL % __model__ + "&uid=%s",
        }


class ContactListItem(xml_models.Model):
    """ Contact List Item Entity """
    
    contactUid = xml_models.IntField(xpath="/contactListItem/contactUid") 
    utcFirstCreated = xml_models.CharField(xpath="/contactListItem/utcFirstCreated") 
    utcLastModified = xml_models.CharField(xpath="/contactListItem/utcLastModified") 
    lastUpdatedUid = xml_models.CharField(xpath="/contactListItem/lastUpdatedUid") 
    salutation = xml_models.CharField(xpath="/contactListItem/salutation") 
    givenName = xml_models.CharField(xpath="/contactListItem/givenName") 
    middleInitials = xml_models.CharField(xpath="/contactListItem/middleInitials") 
    familyName = xml_models.CharField(xpath="/contactListItem/familyName") 
    dateOfBirth = xml_models.DateField(xpath="/contactListItem/dateOfBirth", date_format="%Y-%m-%d") 

    organisation = xml_models.CharField(xpath="/contactListItem/organisation")
    organisationName = xml_models.CharField(xpath="/contactListItem/organisationName")
    organisationAbn = xml_models.CharField(xpath="/contactListItem/organisationAbn")
    abn = xml_models.CharField(xpath="/contactListItem/abn") 

    organizationWebsite = xml_models.CharField(xpath="/contactListItem/organizationWebsite") 
    organizationPosition = xml_models.CharField(xpath="/contactListItem/organizationPosition") 
    emailAddress = xml_models.CharField(xpath="/contactListItem/emailAddress") 
    websiteUrl = xml_models.CharField(xpath="/contactListItem/websiteUrl") 
    isActive = xml_models.BoolField(xpath="/contactListItem/isActive", default=True) 

    mainPhone = xml_models.CharField(xpath="/contactListItem/mainPhone") 
    homePhone = xml_models.CharField(xpath="/contactListItem/homePhone") 
    mobilePhone = xml_models.CharField(xpath="/contactListItem/mobilePhone") 
    otherPhone = xml_models.CharField(xpath="/contactListItem/otherPhone") 
    fax = xml_models.CharField(xpath="/contactListItem/fax") 

    street = xml_models.CharField(xpath="/contactListItem/street") 
    city = xml_models.CharField(xpath="/contactListItem/city") 
    state = xml_models.CharField(xpath="/contactListItem/state") 
    postCode = xml_models.CharField(xpath="/contactListItem/postCode") 
    country = xml_models.CharField(xpath="/contactListItem/country") 

    otherStreet = xml_models.CharField(xpath="/contactListItem/otherStreet") 
    otherCity = xml_models.CharField(xpath="/contactListItem/otherCity") 
    otherState = xml_models.CharField(xpath="/contactListItem/otherState") 
    otherPostCode = xml_models.CharField(xpath="/contactListItem/otherPostCode") 

    contactID = xml_models.CharField(xpath="/contactListItem/contactID") 

    acceptDirectDeposit = xml_models.BoolField(xpath="/contactListItem/acceptDirectDeposit") 
    directDepositAccountName = xml_models.CharField(xpath="/contactListItem/directDepositAccountName") 
    directDepositBsb = xml_models.CharField(xpath="/contactListItem/directDepositBsb") 
    directDepositAccountNumber = xml_models.CharField(xpath="/contactListItem/directDepositAccountNumber") 

    acceptCheque = xml_models.BoolField(xpath="/contactListItem/acceptCheque") 
    chequePayableTo = xml_models.CharField(xpath="/contactListItem/chequePayableTo") 

    # Separate multiple tags by comma. Max. length per tag is 35 characters.
    tags = xml_models.CharField(xpath="/contactListItem/tags") 

    customField1 = xml_models.CharField(xpath="/contactListItem/customField1") 
    customField2 = xml_models.CharField(xpath="/contactListItem/customField2") 


class ContactList(BaseModel):
    """ List of Contact Items """

    __model__ = 'ContactList'
    template_name = 'saasu_client/contactlist_model.xml'
    
    items = CollectionField(ContactListItem, xpath='/contactListResponse/contactList/contactListItem')

    isActive = xml_models.BoolField(xpath="/contactListResponse/contactList/contactListItem/isActive", default=True) 

    finders = {
        (isActive,) : DEFAULT_GET_URL % __model__ + "&isActive=%s",
        }

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return self.items.__iter__()
