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
- **create mysql database DBNAME**
- **list mysql databases**
- **rename mysql database OLDDBNAME NEWDBNAME**
- **delete mysql database DBNAME**
- **check mysql database DBNAME**
- **repair mysql database DBNAME**
- **set mysql privileges USERNAME DBNAME PRIVILEGES**
- **list mysql privileges USERNAME DBNAME**
- **delete mysql privileges USERNAME DBNAME**
- **list mysql routines [USERNAME]**
- **get mysql schema DBNAME**
- **add mysql host HOST**
- **annotate mysql host HOST**
- **list mysql hosts**
- **delete mysql host HOST**
- **get mysql server**
- **get mysql restrictions**

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

**rename mysql user OLDUSERNAME NEWUSERNAME**

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

**create mysql database DBNAME**

Create a new MySQL database with name DBNAME.

*Example*

.. code:: sh

    $ cpanel create mysql database 'northwind'

**list mysql databases**

List existing MySQL databases.

*Example*

.. code:: sh

    $ cpanel list mysql databases

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_databases/

**rename mysql database OLDDBNAME NEWDBNAME**

Rename MySQL database from OLDDBNAME to NEWDBNAME.

*Example*

.. code:: sh

    $ cpanel rename mysql database 'northwind' 'southgale'

**delete mysql database DBNAME**

Delete MySQL database named DBNAME.

*Example*

.. code:: sh

    $ cpanel delete mysql database 'northwind'

**check mysql database DBNAME**

Check the integrity of MySQL database DBNAME.

*Example*

.. code:: sh

    $ cpanel check mysql database 'northwind'

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Mysql-check_database/

**repair mysql database DBNAME**

Try to repair MySQL database DBNAME.
See ‘cpanel check mysql database’ above.

*Example*

.. code:: sh

    $ cpanel repair mysql database 'northwind'

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/repair_database/

**set mysql privileges USERNAME DBNAME PRIVILEGES**

Set the privileges of MySQL user USERNAME on database DBNAME
to PRIVILEGES.

To add full privileges, use 'ALL PRIVILEGES'.
To add individual privileges, use a comma-separated list.

For a list of individual privileges see:
https://api.docs.cpanel.net/openapi/cpanel/operation/set_privileges_on_database/

For a description of the scope of individual privileges see:
https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html

*Examples*

.. code:: sh

    $ cpanel set mysql privileges 'scott' 'northwind' 'ALL PRIVILEGES'

    $ cpanel set mysql privileges 'scott' 'northwind' \ 
          'DELETE, INSERT, REFERENCES, SELECT, SHOW VIEW'

**list mysql privileges USERNAME DBNAME**

List privileges granted to MySQL user USERNAME on database DBNAME.

*Example*

.. code:: sh

    $ cpanel list mysql privileges 'scott' 'northwind'

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Mysql-get_privileges_on_database/

**delete mysql privileges USERNAME DBNAME**

Revoke all privileges granted to MySQL user USERNAME on database DBNAME.

*Example*

.. code:: sh

    $ cpanel delete mysql privileges 'scott' 'northwind'

**list mysql routines [USERNAME]**

List routines (stored procedures and functions) associated to MySQL
user USERNAME. If not provided, list routines from all users.

*Examples*

.. code:: sh

    $ cpanel list mysql routines
    $ cpanel list mysql routines 'scott'

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_routines/

**get mysql schema DBNAME**

Dump schema of MySQL database DBNAME.
The schema is a SQL script that can later be used to recreate the
database.

*Example*

.. code:: sh

    $ cpanel get mysql schema 'northwind'

**add mysql host HOST**

Add HOST to the list of authorized hosts that can connect to MySQL.

HOST can be a hostname, an IP address, or a range with ‘%’ wildcards.

*Examples*

.. code:: sh

    $ cpanel add mysql host client.example.com
    $ cpanel add mysql host '192.168.0.1'
    $ cpanel add mysql host '192.168.%.%'

**annotate mysql host HOST NOTE**

Add a short description NOTE to existing authorized host HOST.
See ‘cpanel add mysql host’ above.

*Example*

.. code:: sh

    $ cpanel annotate mysql host '192.168.0.1' 'My home PC'

**list mysql hosts**

List authorized hosts that can connect to MySQL.
See ‘cpanel add mysql host’ above.

*Example*

.. code:: sh

    $ cpanel list mysql hosts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_host_notes/

**delete mysql host HOST**

Delete HOST from list of authorized.
See ‘cpanel add mysql host’ above.

*Example*

.. code:: sh

    $ cpanel delete mysql host '192.168.0.1'

**get mysql server**

Return server information and version from MySQL.

*Example*

.. code:: sh

    $ cpanel get mysql server

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_server_information/

**get mysql restrictions**

Return MySQL object name length and prefix restrictions.

*Example*

.. code:: sh

    $ cpanel get mysql restrictions

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_restrictions/


