..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``webmail``
==================================================

`Leer en español </es/latest/reference/webmail.html>`_

- **get webmail settings [ACCOUNT]**
- **list webmail apps**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

**COMMANDS**


**get webmail settings [ACCOUNT]**

Return the settings for the Web Mail app used for ACCOUNT.
If no ACCOUNT is provided, the default mail account is used.

*Examples*

.. code:: sh

    $ cpanel get webmail settings
    $ cpanel get webmail settings scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_webmail_settings/

**list webmail apps**

Return a list of available Web Mail apps.

*Example*

.. code:: sh

    $ cpanel list webmail apps

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/listwebmailapps/


