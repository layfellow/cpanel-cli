..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``locales``
==================================================

`Leer en español </es/latest/reference/locales.html>`_

- **list locales**
- **get locale**
- **set locale LOCALE**

**COMMANDS**


**list locales**

List all the available locales (language and conventions) for the cPanel user
interface.

*Example*

.. code:: sh

    $ cpanel list locales

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_locales/

**get locale**

Return the current locale (language and conventions) used for the cPanel user
interface.

*Example*

.. code:: sh

    $ cpanel get locale

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_attributes/

**set locale LOCALE**

Set the cPanel user interface locale (language and conventions) to LOCALE.
Use ‘cpanel list locales’ for a list of available locales.
In general terms, a LOCALE corresponds to a ISO 639-1 two-letter language code.

*Example*

.. code:: sh

    $ cpanel set locale bg


