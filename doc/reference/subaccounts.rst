..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``subaccounts``
==================================================

`Leer en español </es/latest/reference/subaccounts.html>`_

- **list subaccounts**
- **get subaccount GUID**

**COMMANDS**


**list subaccounts**

List the sub-accounts of the main cPanel account, along with detailed information
of each sub-account.

*Example*

.. code:: sh

    $ cpanel list subaccounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/UserManager-list_users/

**get subaccount GUID**

Show detailed information of a sub-account, identified by its GUID. To get
this GUID, use ‘cpanel list subaccounts’. Note that only sub-accounts with a
sub_account_exists flag set to 1 can be queried.

*Example*

.. code:: sh

    $ cpanel get subaccount EXAMPLE1:EXAMPLE.COM:564CD663:FE50072F2620B50988EA4E5F46022546FBE6BDDE3C36C2F2534F4967C661EC37

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/lookup_user/


