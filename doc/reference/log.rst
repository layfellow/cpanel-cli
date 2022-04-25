..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``log``
==================================================

`Leer en español </es/latest/reference/log.html>`_

- **get log settings**
- **set log settings SETTING...**
- **unset log settings SETTING...**
- **list log archives**

cPanel log archival settings are:

- ‘archive’
- ‘prune’

If ‘archive’ is set, log files will be archived to your home directory
after the system processes statistics.

If ‘prune’ is set, cPanel will remove the previous month’s archived logs
at the end of every month.

**COMMANDS**


**get log settings**

Get the account’s log archival settings.

*Example*

.. code:: sh

    $ cpanel get log settings

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_settings/

**set log settings SETTING...**

Set the account’s log archival settings.
SETTING is ‘archive’ or ‘prune’.

*Examples*

.. code:: sh

    $ cpanel set log settings archive
    $ cpanel set log settings prune
    $ cpanel set log settings archive prune

**unset log settings SETTING...**

Unset the account’s log archival settings.
SETTING is ‘archive’ or ‘prune’.

*Examples*

.. code:: sh

    $ cpanel unset log settings archive
    $ cpanel unset log settings prune
    $ cpanel unset log settings archive prune

**list log archives**

List the account’s archived log files.

*Example*

.. code:: sh

    $ cpanel list log archives

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_archives/


