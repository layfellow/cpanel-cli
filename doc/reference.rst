=================
Command Reference
=================

`Leer en español </es/latest/reference.html>`_

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

Module: ``accounts``
====================

**list accounts**
    List basic information of the main cPanel account. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list accounts

**get account**
    Show detailed information of the main account. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get account

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

        $ cpanel get subaccount EXAMPLE1:EXAMPLE.COM:564CD663:FE50072F2620B50988EA4E5F46022546FBE6BDDE3C36C2F2534F4967C661EC37

Module: ``backup``
==================

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

Module: ``cache``
=================

See https://api.docs.cpanel.net/openapi/cpanel/operation/CacheBuster-read/
for information on cache IDs.

**update cache**
    Create web browser cached file override ID. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel update cache

**read cache**
    Return web browser cached file override ID. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel read cache

Module: ``locale``
==================

**list locales**
    List all the available locales (language and conventions) for the cPanel user
    interface. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list locales

**get locale**
    Return the current locale (language and conventions) used for the cPanel user
    interface. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get locale

**set locale LOCALE**
    Set the cPanel user interface locale (language and conventions) to LOCALE.
    Use ``cpanel list locales`` for a list of available locales.
    In general terms, a LOCALE corresponds to a ISO 639-1 two-letter language code.

    *Example*

    .. code:: sh

        $ cpanel set locale bg  # Set UI to Bulgarian

Module: ``styles``
==================

A style is a variation of a user interface theme for cPanel. For example, the
Paper Lantern theme has four styles: ``basic``, ``dark``, ``light`` and ``glass``.

**list styles**
    Return all the available user interface styles. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list styles

**get style**
    Return the current user interface style. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get style

**set style NAME**
    Set the current user interface style to NAME.
    NAME must be one of ``basic``, ``dark``, ``light`` or ``glass``.

    *Example*

    .. code:: sh

        $ cpanel set style dark

**default style NAME**
    Set the default user interface style to NAME.
    NAME must be one of ``basic``, ``dark``, ``light`` or ``glass``.

    *Example*

    .. code:: sh

        $ cpanel default style basic

Module: ``themes``
==================

A theme is a customized look and feel for the cPanel user interface. The default
cPanel theme is Jupiter; another popular theme is Paper Lantern.

**list themes**
    Return all the available themes. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list themes

**get theme**
    Return the current theme. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get theme

**set theme NAME**
    Set the current theme to NAME.
    NAME must be one the available themes reported by ``cpanel list themes``.

    *Example*

    .. code:: sh

        $ cpanel set theme paper_lantern


Module: ``directory``
=====================

Indexing commands
-----------------

The *indexing* of a remote directory controls how to present that directory
to a web browser if no default HTML index page is found.

There are four possible index settings:

- ``inherit``: Use the parent directory’s setting.
- ``disabled``: a.k.a. *No Indexing*, do not list the directory contents.
- ``standard``: a.k.a. *Show Filename Only*, list only the directory’s file names.
- ``fancy``: a.k.a. *Show Filename and Description*, list the directory’s file names,
  sizes and types.

cPanel uses a ``.htaccess`` directive in the remote directory to control the
index settings. For instance, for ``fancy``, it adds the following to ``.htaccess``:

.. code:: sh

    Options +Indexes
    IndexOptions +HTMLTable +FancyIndexing

See https://docs.cpanel.net/cpanel/advanced/indexes/ for further information.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., ``/public_html`` corresponds to
``<remote login directory>/public_html``.

**list dir indexing PATH**
    List the index settings for remote PATH and its subdirectories (children).
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list dir indexing /public_html

**get dir indexing PATH**
    Get the index setting for remote PATH only. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel get dir indexing /public_html

**set dir indexing PATH TYPE**
    Set the index setting for remote PATH. Possible values for TYPE are
    ``inherit``, ``disabled``, ``standard`` or ``fancy``.

    *Example*

    .. code:: sh

        $ cpanel set dir indexing /public_html fancy

Privacy commands
----------------

cPanel can password-protect remote directories for privacy. Any attempt to
access a private directory using a web browser will prompt for a
username and password.

The actual underlying authentication method is Basic HTTP authentication;
these users and passwords are local to the directory, they are *not* cPanel users.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., ``/public_html`` corresponds to
``<remote login directory>/public_html``.

**list dir privacy PATH**
    List the privacy settings for remote PATH and its subdirectories (children).
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list dir privacy /public_html

**get dir privacy PATH**
    Get the privacy settings for remote PATH only. Output is JSON-formatted.
    You can enable or disable password protection using
    ``cpanel enable dir privacy`` or ``cpanel disable dir privacy`` (see below).

    *Example*

    .. code:: sh

        $ cpanel get dir privacy /public_html

**enable dir privacy PATH**
    Enable password protection for PATH. Note that you need to add users
    using ``cpanel add dir user`` (see below) to grant access to PATH.

    *Example*

    .. code:: sh

        $ cpanel enable dir privacy /public_html

**disable dir privacy PATH**
    Disable password protection for PATH.

    *Example*

    .. code:: sh

        $ cpanel disable dir privacy /public_html

User management commands
------------------------

cPanel grants access to remote password-protected directories using
ad hoc users and passwords specific to every directory. Use the
commands below to manage these users.

cPanel stores the credentials in a ``.htpasswd`` file.
See https://en.wikipedia.org/wiki/.htpasswd for further information.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., ``/public_html`` corresponds to
``<remote login directory>/public_html``.

**add dir user PATH USER PASSWORD**
    Add USER with corresponding PASSWORD to the list of allowed users
    for PATH.

    *Example*

    .. code:: sh

        $ cpanel add dir user /public_html scott tiger

**delete dir user PATH USER**
    Remove USER from the list of allowed users for PATH.

    *Example*

    .. code:: sh

        $ cpanel delete dir user /public_html scott

**list dir users PATH**
    List allowed users for PATH. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list users /public_html

Leech protection commands
-------------------------

*Leech protection* adds some basic measures against the abuse of
password-protected directories. The system allows a maximum number of
logins per hour for a leech-protected directory.

See https://docs.cpanel.net/cpanel/security/leech-protection/ for further information.

**list dir protection PATH**
    List leech protection status for PATH and its subdirectories (children).
    Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list dir protection /public_html

Module: ``mail``
================

**list mail accounts**
    List cPanel email accounts. Output is JSON-formatted.

    *Example*

    .. code:: sh

        $ cpanel list mail accounts

**list mail filters ACCOUNT**
    List mail filters associated to ACCOUNT. Output is a JSON-formatted
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
