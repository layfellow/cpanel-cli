..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``mysql``
==================================================

`Leer en español </es/latest/reference/mysql.html>`_

- **create mysql user USERNAME PASSWORD**
- **list mysql users**
- **rename mysql user OLDUSERNAME NEWUSERNAME**
- **set mysql password USERNAME NEWPASSWORD**
- **delete mysql user USERNAME**

**COMMANDS**


**create mysql user USERNAME PASSWORD**

Create a new MySQL user with USERNAME and PASSWORD.

*Example*

.. code:: sh

    $ cpanel create mysql user "scott" 'tiger'

**list mysql users**

List all MySQL users associated to the cPanel account.

*Example*

.. code:: sh

    $ cpanel list mysql users

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Mysql-list_users/

**rename mysql user OLDUSERNAME**

Rename MySQL user from OLDUSERNAME to NEWUSERNAME.

*Example*

.. code:: sh

    $ cpanel rename mysql user "scott" "larry"

**set mysql password USERNAME NEWPASSWORD**

Change the password for MySQL user USERNAME to NEWPASSWORD.

*Example*

.. code:: sh

    $ cpanel set mysql password "scott" 'panther'

**delete mysql user USERNAME**

Delete MySQL user USERNAME.

*Example*

.. code:: sh

    $ cpanel delete mysql user "scott"

