# Adlibre TMS

Adlibre TMS is a Timesheet and Expense tracking system for the cloud and online business.
Designed with contractors and consultants in mind, yet it is flexible enough to bend to fit almost any business.
It uses a three dimensional paradigm of "Consultant", "Client" and "Service" to describe work activity. This is flexible to adjust to your needs,
without being too complex or convoluted to configure.

## Features

* Interfaces - Engineered specifically to provide (web service) interfaces to popular SaaS accounting packages. (Currently [Saasu](http://www.saasu.com "Saasu Online Accounting") are supported)
    - Point and click invoicing
    - Point and click expense claims
    - Plugs into Adlibre DMS for storing the supporting documentation for expenses. (Coming soon)
* Reports - 4 standard reports are available. It's easy to extend and to write your own in Python/HTML.
* Skinable, brandable, integrate it into your other web applications. Intranet ready.
* Pony powered with Python and Django.
* Open Source - hackable...

### Saasu Integration

More information regarding the Saasu setup can be found in [docs/saasu_setup.md](https://github.com/adlibre/Adlibre-TMS/blob/master/docs/saasu_setup.md).

## Screenshots

![Adlibre Timesheet Management System - Login](https://github.com/adlibre/Adlibre-TMS/raw/master/docs/tms_1.jpg)
![Adlibre Timesheet Management System - Timesheets](https://github.com/adlibre/Adlibre-TMS/raw/master/docs/tms_2.jpg)
![Adlibre Timesheet Management System - Expenses](https://github.com/adlibre/Adlibre-TMS/raw/master/docs/tms_3.jpg)

## Online Demo

There is an online demonstration site available. The site refreshes every 60 minutes, so feel free to make changes:

* http://tmsdemo.adlibre.com.au Login: demo, Password: demo.

## Installation

Within a clean virtualenv run the following command to install Adlibre TMS and all required packages:

Production:

    pip install git+git://github.com/adlibre/Adlibre-TMS.git

Development:

    pip install -e git+git://github.com/adlibre/Adlibre-TMS.git#egg=tms-dev

For detailed in installation instructions read [INSTALL.md](https://github.com/adlibre/Adlibre-TMS/blob/master/INSTALL.md).

## Support

Adlibre TMS is developed and commercially supported by [Adlibre](http://www.adlibre.com.au/ "Adlibre Open Source Consulting").

More information is available at:

* http://www.adlibre.com.au/adlibre-tms/
