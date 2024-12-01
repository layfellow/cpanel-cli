..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``addons``
==================================================

`Leer en español </es/latest/reference/addons.html>`_

- **list addons**
- **list addon instances ADDON**
- **get addon instance UNIQUEID**

**COMMANDS**


**list addons**

List all the available addons for this cPanel server.

Addons are identified by their names listed on the “module” field in the
returned JSON data.

*Example*

.. code:: sh

    $ cpanel list addons

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_available_addons/

**list addon instances ADDON**

List all the deployed instances of an ADDON identified by its name.

Unique instances are identified by their “unique_id” fields in the
returned JSON data.

Use ‘cpanel list addons’ to get a list of ADDON names.

*Example*

.. code:: sh

    $ cpanel list addon instances 'cPanel::Blogs::WordPressX'

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_addon_instances/

**get addon instance UNIQUEID**

Get the settings of a deployed instance of an addon identified by its UNIQUEID.

Use ‘cpanel list addon instances’ to get a list of UNIQUEIDs.

*Example*

.. code:: sh

    $ cpanel get addon instance 'cPanel::Blogs::WordPressX.0.1486754861'

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_instance_settings/


