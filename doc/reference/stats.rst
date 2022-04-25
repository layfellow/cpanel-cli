..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``stats``
==================================================

`Leer en español </es/latest/reference/stats.html>`_

- **get stats STAT...**

Show detailed data and statistics, like hostname, file usage, database usage,
dedicated IPs, etc.

STAT is the name of the statistic you want, you can provide a list of STATs to
be displayed. For a complete list ot STAT names, see ‘display parameters’ at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_stats/

*Examples*

.. code:: sh

    $ cpanel get stats hostname
    $ cpanel get stats machinetype cpanelversion

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_stats/


