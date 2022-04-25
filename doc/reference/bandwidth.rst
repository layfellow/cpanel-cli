..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``bandwidth``
==================================================

`Leer en español </es/latest/reference/bandwidth.html>`_

- **get bandwidth services**
- **get bandwidth retention**

For further information see:
https://docs.cpanel.net/cpanel/metrics/bandwidth/

**COMMANDS**


**get bandwidth services**

Return a list of services (by protocol) being monitored in bandwidth data.

*Example*

.. code:: sh

    $ cpanel get bandwidth services

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_enabled_protocols/

**get bandwidth retention**

Get the collection interval and retention periods for bandwidth data.

*Example*

.. code:: sh

    $ cpanel get bandwidth services

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_retention_periods/


