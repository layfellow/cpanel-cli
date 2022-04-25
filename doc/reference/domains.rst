..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``domains``
==================================================

`Leer en español </es/latest/reference/domains.html>`_

- **list domains**
- **list domain data**
- **get domain data DOMAIN**
- **get domain aliases**

**COMMANDS**


**list domains**

List domains for the cPanel account’s.

*Example*

.. code:: sh

    $ cpanel list domains

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_domains/

**list domain data**

Get hosting data for all the cPanel account’s domains.

*Example*

.. code:: sh

    $ cpanel list domain data

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/domains_data/

**get domain data DOMAIN**

Get hosting data for DOMAIN. Use ‘cpanel list domains’
to get a list of domains.

*Example*

.. code:: sh

    $ cpanel get domain data example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/single_domain_data/

**get domain aliases**

List the built-in subdomain aliases for an account’s main domain.

*Example*

.. code:: sh

    $ cpanel get domain aliases

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/main_domain_builtin_subdomain_aliases/


