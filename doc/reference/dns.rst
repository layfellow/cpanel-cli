..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``dns``
==================================================

`Leer en español </es/latest/reference/dns.html>`_

- **check dns DOMAIN**
- **authoritative dns DOMAIN**
- **lookup dns**
- **list dynamic dns**
- **create dynamic dns SUBDOMAIN [DESCRIPTION]**
- **recreate dynamic dns ID**
- **update dynamic dns ID DESCRITPION**
- **delete dynamic dns ID**

**COMMANDS**


**check dns DOMAIN**

Check if DOMAIN resolves to the cPanel server.

*Example*

.. code:: sh

    $ cpanel check dns example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/ensure_domains_reside_only_locally/

**check authoritative dns DOMAIN**

Tell if cPanel server is the authoritative server for DOMAIN.

*Example*

.. code:: sh

    $ cpanel authoritative dns example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/has_local_authority/

**lookup dns DOMAIN**

Return DNS zone information about DOMAIN.

*Example*

.. code:: sh

    $ cpanel lookup dns DOMAIN

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dns-lookup/

**list dynamic dns**

List the Dynamic DNS domains for your cPanel user.

*Example*

.. code:: sh

    $ cpanel list dynamic dns

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dynamicdns-list/

**create dynamic dns SUBDOMAIN [DESCRIPTION]**

Create a new Dynamic DNS entry attached to SUBDOMAIN.
Optionally include a human-readable DESCRIPTION.
Return an ID which you can later use in a web call
https://example.com/cpanelwebcall/<ID>.

For further information see:
https://docs.cpanel.net/cpanel/domains/dynamic-dns/

*Examples*

.. code:: sh

    $ cpanel create dynamic dns homeserver.example.com
    $ cpanel create dynamic dns homeserver.example.com "A home server with variable IP"

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dynamicdns-create/

**recreate dynamic dns ID**

Delete and create again a Dynamic DNS entry identified by ID.
Return a new ID. Use ‘cpanel list dynamic dns’ to get a list of IDs and
associated subdomains.

*Example*

.. code:: sh

    $ cpanel recreate dynamic dns gziugyxxjwnamqtwysgmvrurplmafxpj

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dynamicdns-recreate/

**update dynamic dns ID DESCRIPTION**

Update the DESCRIPTION of Dynamic DNS entry identified by ID.

*Example*

.. code:: sh

    $ cpanel update dynamic dns gziugyxxjwnamqtwysgmvrurplmafxpj "A home server with variable IP"

**delete dynamic dns ID**

Delete a Dynamic DNS entry identified by ID. Use ‘cpanel list dynamic dns’
to get a list of IDs and associated subdomains.

*Example*

.. code:: sh

    $ cpanel delete dynamic dns gziugyxxjwnamqtwysgmvrurplmafxpj


