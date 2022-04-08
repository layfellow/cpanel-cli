==========================
Complete Command Reference
==========================

Module: ``features``
====================

**list features**
    List a cPanel account’s features. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list features

Module: ``quota``
====================

**get quota**
    Get the cPanel account’s total disk quota information in megabytes.
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get quota

Module: ``usage``
====================

**get usage**
    Show resource usage and some statistics, like bandwidth, number of subdomains,
    disk usage, number of mail filters, etc.
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get usage

Module: ``stats``
====================

**get stats STAT...**
    Show detailed data and statistics, like hostname, file usage, database usage,
    dedicated IPs, etc. Output is JSON-formatted.

    STAT is the name of the statistic you want, you can provide a list of STATs to
    be displayed. For a complete list of STAT names, see ‘display parameters’ at:
    https://api.docs.cpanel.net/openapi/cpanel/operation/get_stats/

    *Examples*

    .. code:: sh

        $ cpanel get stats hostname
        $ cpanel get stats machinetype cpanelversion

Module: ``mail``
================

**list mail accounts**
    Lists cPanel email accounts. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list mail accounts

**list mail filters ACCOUNT**
    Lists mail filters associated to ACCOUNT. Output is a JSON-formatted
    array of filter names.

    ACCOUNT is the name of a cPanel email account, usually user@domain

    *Example*

    .. code:: sh

        $ cpanel list mail filters scott@example.com

**get mail filter ACCOUNT FILTERNAME**
    Return a JSON-formatted description of email filter FILTERNAME associated
    to email ACCOUNT. To get a list of current filter names, use
    ``cpanel list mail filters ACCOUNT``

    *Example*

    .. code:: sh

        $ cpanel get mail filter scott@example.com spamkiller

**set mail filter ACCOUNT FILE**
    Create or update an email filter associated with email ACCOUNT.
    If the filter already exists, it updates it; otherwise, it creates a new filter.
    Use a JSON FILE to describe the filter rules. This JSON FILE has the same
    textual format as the output from ``cpanel get mail filter``, so the easiest way
    to create a new filter is to dump an existing filter into a ``filter.json`` file,
    edit it and then upload it with ``cpanel set mail filter``.
    See the example below.

    *Example*

    .. code:: sh

        $ cpanel get mail filter scott@example.com spamkiller > filter.json

        # Edit filter.json, and then run:
        $ cpanel set mail filter scott@example.com filter.json

**delete mail filter ACCOUNT FILTERNAME**
    Delete email filter FILTERNAME associated to ACCOUNT. To get a list of current
    filter names, use ``cpanel list mail filters ACCOUNT``

    *Example*

    .. code:: sh

        $ cpanel delete mail filter scott@example.com spamkiller
