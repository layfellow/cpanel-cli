=================
Command Reference
=================

`Leer en español <../es/reference.html>`_

Module: ``features``
====================

**list features**
    List a cPanel account’s features. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list features

Module: ``quota``
=================

**get quota**
    Get the cPanel account’s total disk quota information in megabytes.
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get quota

Module: ``usage``
=================

**get usage**
    Show resource usage and some statistics, like bandwidth, number of subdomains,
    disk usage, number of mail filters, etc.
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get usage

Module: ``stats``
=================

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

Module: ``subaccounts``
=======================

**list subaccounts**
    List the sub-accounts of the main cPanel account, along with detailed information
    of each sub-account. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list subaccounts

**get subaccount GUID**
    Show detailed information of a sub-account, identified by its GUID. To get
    this GUID, use ``cpanel list subaccounts``. Note that only sub-accounts with a
    ``sub_account_exists`` flag set to 1 can be queried. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ get subaccount EXAMPLE1:EXAMPLE.COM:564CD663:FE50072F2620B50988EA4E5F46022546FBE6BDDE3C36C2F2534F4967C661EC37

Module: ``backups``
===================

All ``create backup`` commands create a backup tarball (a ``.tar.gz`` file) of the user’s home
directory along with other account data, such as the crontab, API tokens, log files and DB data.
The backup tarball’s name is ``backup-MM.DD.YYYY_HH-MM-SS_USERNAME.tar.gz``.

If you pass an optional EMAIL argument, the backup engine will send a confirmation email
after it completes the backup.

**cpanel create backup home [EMAIL]**
    Create a backup tarball and store it in the user’s home directory itself.

**cpanel create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**
    Create a backup tarball and store it on a remote FTP server.

    HOST is the hostname of the remote FTP server.

    USERNAME and PASSWORD are the credentials to log in to it.

    Optional DIRECTORY is the destination directory on the remote server; by default use the
    remote user’s login directory. Note that DIRECTORY is not an absolute path, but a path
    relative to the login directory, i.e., ``/public`` corresponds to
    ``<remote login directory>/public``.

**cpanel create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**
    Create a backup tarball and store it on a remote SCP server.

    USERNAME, PASSWORD, HOST and DIRECTORY are the same as for ``create backup ftp``.

    *Examples*

    .. code:: sh

        $ cpanel backup home
        $ cpanel backup home scott@example.com
        $ cpanel backup ftp scott tiger ftp.example.com
        $ cpanel backup ftp scott tiger ftp.example.com /backup
        $ cpanel backup scp scott tiger ssh.example.com /backup scott@example.com

**cpanel list backups**
    List the account’s backup files. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list backups

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
