# Saasu Integration Setup

Adlibre TMS supports integration with the [Saasu](http://www.saasu.com "Saasu Online Accounting") API

To configure Saasu integration first  generate a key from _Settings > Web Services_ within Saasu. This is used to configure TMS, currently configured in _local_settings.py_

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/webservices_setup_saasu.png" />

## Customer and Service Linking

The next step is to link your customer and services to the appropriate accounts in Saasu as shown below.

Click on the Saasu field to popup a list of customers and services directly from Saasu.

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/link_customer_saasu.png" />

<img src="https://github.com/adlibre/Adlibre-TMS/raw/master/docs/link_service_saasu.png" />

After this is done you will be able to export timesheet and expense entries directly to Saasu.