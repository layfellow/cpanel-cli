..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``subaccounts``
==================================================

`Leer en español </es/latest/reference/subaccounts.html>`_

- **list subaccounts**
- **get subaccount GUID**
- **get service account USERNAME TYPE**
- **check subaccount conflicts USERNAME**

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

**get service subaccount USERNAME TYPE**

Show detailed information of a service subaccount, identified by its USERNAME.
TYPE is the type of service subaccount, it's either ‘ftp’, ‘email’ or ‘webdisk’.

Use ‘cpanel list subaccounts’ to get a list of full subaccount usernames.

*Example*

.. code:: sh

    $ cpanel get service subaccount ftp@example.com ftp

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/lookup_service_account/

**check subaccount conflicts USERNAME**

Check if a subaccount identified by USERNAME conflicts with any other subaccount.
Look for a “conflict”:1 in the returned JSON data.

Use ‘cpanel list subaccounts’ to get a list of full subaccount usernames.

*Example*

.. code:: sh

    $ cpanel check subaccount conflicts ftp@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/check_account_conflicts/


