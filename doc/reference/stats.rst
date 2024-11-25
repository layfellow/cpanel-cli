..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``stats``
==================================================

`Leer en español </es/latest/reference/stats.html>`_

- **list stats domains**
- **get stats bandwidth**
- **get stats DOMAIN [ENGINE] [PROTOCOL]**
- **get stats STAT...**

**COMMANDS**


**list stats domains**

List all the valid domains to get stats from.

*Example*

.. code:: sh

    $ cpanel list stats domains

**get stats bandwidth**

Return monthly bandwidth usage for all domains.

*Example*

.. code:: sh

    $ cpanel get stats bandwidth

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_bandwidth/

**get stats DOMAIN [ENGINE] [PROTOCOL]**

Return a HTML page with traffic stats for DOMAIN.

ENGINE is the traffic analyzer, it's either ‘analog’ or ‘webalizer’ (default).
PROTOCOL is the traffic protocol, it's either ‘ftp’ or ‘http’ (default).

Use ‘cpanel list stats domains’ to get a list of valid DOMAINs.

*Examples*

.. code:: sh

    $ cpanel get stats example.com
    $ cpanel get stats example.com analog
    $ cpanel get stats example.com webalizer ftp

**get stats STAT...**

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


