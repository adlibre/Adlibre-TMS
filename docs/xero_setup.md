# Xero Integration Setup

Adlibre TMS supports integration with the [Xero](https://www.xero.com "Accounting Software & Online Bookkeeping | Xero") API

Xero instalation manual can be found on [HERE](http://developer.xero.com/documentation/getting-started/public-applications/).

Statements from there:
Any Xero user can register a public application. If you do not already have a Xero user account, [sign up](https://www.xero.com/signup) for a free account.

* Login to the [Xero Developer portal](https://api.xero.com/)
* Go to the My Applications > Add Application screen to add your application.
* Select “Public” and enter a name for your application and the URL of your company. [Find out more here](http://xerodev.wpengine.com/documentation/getting-started/api-application-setup/).
* Optionally you can enter a callback domain. This will be used to verify the callback url you specify when authorising is allowed.
* Choose save. You’ll now be shown your OAuth credentials.

This is used to configure TMS, currently configured in _.env_ file during build process

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/xero_register_app.png" />

## Xero data bindings

The next step is to link your Xero items, users accounts and contacts to the appropriate accounts in TMS as shown below.

Click on the Xero search button near a field to popup a list of binding data objects directly fetched directly from Xero.

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/xero_customer_binding.png" />

* Customer. Note here you need to set the currency. It is required for Xero only (Currently) Currency code must match the Xero currency code. E.g. Currency with code AUD in Xero -> AUD in TMS.

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/xero_employee_binding.png" />

* Employee required for logging on expenses only. Expenses in TMS -> Expense claims in Xero.

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/xero_service_binding.png" />

* Service required for binding invoice items with price set in Xero itself. So you just bind Xero services and do not set their price in TMS.

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/xero_expense_binding.png" />

* Expense type must contain the account code for proper Expense Claims logging to Xero.

After this is done you will be able to export timesheet and expense entries directly to Xero.

### Xero Exporting process

* TODO:!!!