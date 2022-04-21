=================
Command Reference
=================

`Leer en español </es/latest/reference.html>`_

Module: ``features``
==================================================

- **list features**


List a cPanel account’s features.

*Example*

.. code:: sh

    $ cpanel list features

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_features/


Module: ``quota``
==================================================

- **get quota**


Get the cPanel account’s total disk quota information in megabytes.

*Example*

.. code:: sh

    $ cpanel get quota

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_quota_info/


Module: ``usage``
==================================================

- **get usage**


Show resource usage and some statistics, like bandwidth, number of subdomains,
disk usage, number of mail filters, etc.

*Example*

.. code:: sh

    $ cpanel get usage

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_usages/


Module: ``stats``
==================================================

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


Module: ``accounts``
==================================================

- **list accounts**

- **get account**


**COMMANDS**


**list accounts**

List basic information of the main cPanel account.

*Example*

.. code:: sh

    $ cpanel list accounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_accounts/

**get account**

Show detailed information of the main account.

*Example*

.. code:: sh

    $ cpanel get account

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Variables-get_user_information/


Module: ``subaccounts``
==================================================

- **list subaccounts**

- **get subaccount GUID**


**COMMANDS**


**list subaccounts**

List the sub-accounts of the main cPanel account, along with detailed information
of each sub-account.

*Example*

.. code:: sh

    $ cpanel list subaccounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/UserManager-list_users/

**get subaccount GUID**

Show detailed information of a sub-account, identified by its GUID. To get
this GUID, use ‘cpanel list subaccounts’. Note that only sub-accounts with a
sub_account_exists flag set to 1 can be queried.

*Example*

.. code:: sh

    $ cpanel get subaccount EXAMPLE1:EXAMPLE.COM:564CD663:FE50072F2620B50988EA4E5F46022546FBE6BDDE3C36C2F2534F4967C661EC37

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/lookup_user/


Module: ``backup``
==================================================

- **create backup home [EMAIL]**

- **create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**

- **create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**

- **list backups**


**COMMANDS**


All ‘create backup’ commands create a backup tarball (a .tar.gz file) of
the user’s home directory along with other account data, such as the crontab,
API tokens, log files and DB data. The backup tarball’s name is
backup-MM.DD.YYYY_HH-MM-SS_USERNAME.tar.gz.

If you pass an optional EMAIL argument, the backup engine will send a
confirmation email after it completes the backup.

**create backup home [EMAIL]**

Create a backup tarball and store it in the user’s home directory itself.

**create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**

Create a backup tarball and store it on a remote FTP server.

HOST is the hostname of the remote FTP server.
USERNAME and PASSWORD are the credentials to log in to it.
Optional DIRECTORY is the destination directory on the remote server;
by default use the remote user’s login directory. Note that DIRECTORY
is not an absolute path, but a path relative to the login directory, i.e.,
/public corresponds to <remote login directory>/public.

**create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**

Create a backup tarball and store it on a remote SCP server.

USERNAME, PASSWORD, HOST and DIRECTORY are the same as for ‘create backup ftp’.

*Examples*

.. code:: sh

    $ cpanel backup home
    $ cpanel backup home scott@example.com
    $ cpanel backup ftp scott tiger ftp.example.com
    $ cpanel backup ftp scott tiger ftp.example.com /backup
    $ cpanel backup scp scott tiger ssh.example.com /backup scott@example.com

**list backups**

List the account’s backup files.

*Example*

.. code:: sh

    $ cpanel list backups

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_backups/


Module: ``cache``
==================================================

- **update cache**

- **read cache**


**COMMANDS**


**update cache**

Create web browser cached file override ID.

*Example*

.. code:: sh

    $ cpanel update cache

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/update/

**read cache**

Return web browser cached file override ID.

*Example*

.. code:: sh

    $ cpanel read cache

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/CacheBuster-read/


Module: ``locales``
==================================================

- **list locales**

- **get locale**

- **set locale LOCALE**


**COMMANDS**


**list locales**

List all the available locales (language and conventions) for the cPanel user
interface.

*Example*

.. code:: sh

    $ cpanel list locales

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_locales/

**get locale**

Return the current locale (language and conventions) used for the cPanel user
interface.

*Example*

.. code:: sh

    $ cpanel get locale

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_attributes/

**set locale LOCALE**

Set the cPanel user interface locale (language and conventions) to LOCALE.
Use ‘cpanel list locales’ for a list of available locales.
In general terms, a LOCALE corresponds to a ISO 639-1 two-letter language code.

*Example*

.. code:: sh

    $ cpanel set locale bg


Module: ``styles``
==================================================

- **list styles**

- **get style**

- **set style NAME**

- **default style NAME**


**COMMANDS**


A style is a variation of a user interface theme for cPanel. For example, the
‘paper lantern’ theme has four styles: ‘basic’, ‘dark’, ‘light’ and ‘glass’.

**list styles**

Return all the available user interface styles.

*Example*

.. code:: sh

    $ cpanel list styles

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list/

**get style**

Return the current user interface style.

*Example*

.. code:: sh

    $ cpanel get style

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/current/

**set style NAME**

Set the current user interface style to NAME.
NAME must be one of ‘basic’, ‘dark’, ‘light’ or ‘glass’

*Example*

.. code:: sh

    $ cpanel set style dark

**default style NAME**

Set the default user interface style to NAME.
NAME must be one of ‘basic’, ‘dark’, ‘light’ or ‘glass’

*Example*

.. code:: sh

    $ cpanel default style basic


Module: ``themes``
==================================================

- **list themes**

- **get theme**

- **set theme NAME**


A theme is a customized look and feel for the cPanel user interface. The default
cPanel theme is ‘jupiter’; another popular theme is ‘paper lantern’.

**COMMANDS**


**list themes**

Return all the available themes.

*Example*

.. code:: sh

    $ cpanel list themes

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Themes::list/

**get theme**

Return the current theme.

*Example*

.. code:: sh

    $ cpanel get theme

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_theme_base/

**set theme NAME**

Set the current theme to NAME.
NAME must be one the available themes reported by ‘cpanel list themes’.

*Example*

.. code:: sh

    $ cpanel set theme paper_lantern


Module: ``dir``
==================================================

- **list dir indexing PATH**

- **get dir indexing PATH**

- **set dir indexing PATH TYPE**

- **list dir privacy PATH**

- **get dir privacy PATH**

- **enable dir privacy PATH**

- **disable dir privacy PATH**

- **add dir user PATH USER PASSWORD**

- **delete dir user PATH USER**

- **list dir users PATH**

- **list dir protection PATH**


**INDEXING COMMANDS**


The indexing of a remote directory controls how to present that directory
to a web browser if no default HTML index page is found.

There are four possible index settings:

- ‘inherit’: Use the parent directory’s setting.
- ‘disabled’ (No Indexing): do not list the directory contents.
- ‘standard’ (Show Filename Only): list only the directory’s file names.
- ‘fancy’: (Show Filename and Description) list the directory’s file names, sizes and types.

cPanel uses a .htaccess directive in the remote directory to control the
index settings. For instance, for ‘fancy’, it adds the following to htaccess:

Options +Indexes
IndexOptions +HTMLTable +FancyIndexing

See https://docs.cpanel.net/cpanel/advanced/indexes/ for further information.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., /public_html corresponds to
<remote login directory>/public_html.

**list dir indexing PATH**

List the index settings for remote PATH and its subdirectories (children).

*Example*

.. code:: sh

    $ cpanel list dir indexing /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/DirectoryIndexes-list_directories/

**get dir indexing PATH**

Get the index setting for remote PATH only.

*Example*

.. code:: sh

    $ cpanel get dir indexing /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_indexing/

**set dir indexing PATH TYPE**

Set the index setting for remote PATH. Possible values for TYPE are
‘inherit’, ‘disabled’, ‘standard’ or ‘fancy’.

*Example*

.. code:: sh

    $ cpanel set dir indexing /public_html fancy

**PRIVACY COMMANDS**


cPanel can password-protect remote directories for privacy. Any attempt to
access a private directory using a web browser will prompt for a
username and password.

The actual underlying authentication method is Basic HTTP authentication;
these users and passwords are local to the directory, they are not cPanel users.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., /public_html corresponds to
<remote login directory>/public_html.

**list dir privacy PATH**

List the privacy settings for remote PATH and its subdirectories (children).

*Example*

.. code:: sh

    $ cpanel list dir privacy /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/DirectoryPrivacy-list_directories/

**get dir privacy PATH**

Get the privacy settings for remote PATH only.
You can enable or disable password protection using
‘cpanel enable dir privacy’ or ‘cpanel disable dir privacy’ (see below).

*Example*

.. code:: sh

    $ cpanel get dir privacy /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/is_directory_protected/

**enable dir privacy PATH**

Enable password protection for PATH. Note that you need to add users
using ‘cpanel add dir user’ (see below) to grant access to PATH.

*Example*

.. code:: sh

    $ cpanel enable dir privacy /public_html

**disable dir privacy PATH**

Disable password protection for PATH.

*Example*

.. code:: sh

    $ cpanel disable dir privacy /public_html

**USER MANAGEMENT COMMANDS**


cPanel grants access to remote password-protected directories using
ad hoc users and passwords specific to every directory. Use the
commands below to manage these users.

cPanel stores the credentials in a .htpasswd file.
See https://en.wikipedia.org/wiki/.htpasswd for further information.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., /public_html corresponds to
<remote login directory>/public_html.

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

List allowed users for PATH.

*Example*

.. code:: sh

    $ cpanel list users /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/DirectoryPrivacy::list_users/

**LEECH PROTECTION COMMANDS**


Leech protection adds some basic measures against the abuse of
password-protected directories. The system allows a maximum number of
logins per hour for a leech-protected directory.

See https://docs.cpanel.net/cpanel/security/leech-protection/ for further information.

033[1mlist dir protection PATH033[00m
List leech protection status for PATH and its subdirectories (children).

*Example*

.. code:: sh

    $ cpanel list dir protection /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/DirectoryProtection-list_directories/


Module: ``dns``
==================================================

- **check dns DOMAIN**

- **authoritative dns DOMAIN**

- **lookup dns**

- **list dynamic dns**

- **create dynamic dns SUBDOMAIN [DESCRIPTION]**

- **recreate dynamic dns ID**

- **update dynamic dns ID DESCRITPION**

- **delete dynamic dns ID**


**COMMANDS**


**check dns DOMAIN**

Check if DOMAIN resolves to the cPanel server.

*Example*

.. code:: sh

    $ cpanel check dns example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/ensure_domains_reside_only_locally/

**check authoritative dns DOMAIN**

Tell if cPanel server is the authoritative server for DOMAIN.

*Example*

.. code:: sh

    $ cpanel authoritative dns example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/has_local_authority/

**lookup dns DOMAIN**

Return DNS zone information about DOMAIN.

*Example*

.. code:: sh

    $ cpanel lookup dns DOMAIN

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dns-lookup/

**list dynamic dns**

List the Dynamic DNS domains for your cPanel user.

*Example*

.. code:: sh

    $ cpanel list dynamic dns

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dynamicdns-list/

**create dynamic dns SUBDOMAIN [DESCRIPTION]**

Create a new Dynamic DNS entry attached to SUBDOMAIN.
Optionally include a human-readable DESCRIPTION.
Return an ID which you can later use in a web call
https://example.com/cpanelwebcall/<ID>.

For further information see:
https://docs.cpanel.net/cpanel/domains/dynamic-dns/

*Examples*

.. code:: sh

    $ cpanel create dynamic dns homeserver.example.com
    $ cpanel create dynamic dns homeserver.example.com "A home server with variable IP"

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dynamicdns-create/

**recreate dynamic dns ID**

Delete and create again a Dynamic DNS entry identified by ID.
Return a new ID. Use ‘cpanel list dynamic dns’ to get a list of IDs and
associated subdomains.

*Example*

.. code:: sh

    $ cpanel recreate dynamic dns gziugyxxjwnamqtwysgmvrurplmafxpj

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/dynamicdns-recreate/

**update dynamic dns ID DESCRIPTION**

Update the DESCRIPTION of Dynamic DNS entry identified by ID.

*Example*

.. code:: sh

    $ cpanel update dynamic dns gziugyxxjwnamqtwysgmvrurplmafxpj "A home server with variable IP"

**delete dynamic dns ID**

Delete a Dynamic DNS entry identified by ID. Use ‘cpanel list dynamic dns’
to get a list of IDs and associated subdomains.

*Example*

.. code:: sh

    $ cpanel delete dynamic dns gziugyxxjwnamqtwysgmvrurplmafxpj


Module: ``domains``
==================================================

- **list domains**

- **list domain data**

- **get domain data DOMAIN**

- **get domain aliases**


**COMMANDS**


**list domains**

List domains for the cPanel account’s.

*Example*

.. code:: sh

    $ cpanel list domains

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_domains/

**list domain data**

Get hosting data for all the cPanel account’s domains.

*Example*

.. code:: sh

    $ cpanel list domain data

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/domains_data/

**get domain data DOMAIN**

Get hosting data for DOMAIN. Use ‘cpanel list domains’
to get a list of domains.

*Example*

.. code:: sh

    $ cpanel get domain data example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/single_domain_data/

**get domain aliases**

List the built-in subdomain aliases for an account’s main domain.

*Example*

.. code:: sh

    $ cpanel get domain aliases

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/main_domain_builtin_subdomain_aliases/


Module: ``log``
==================================================

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


Module: ``bandwidth``
==================================================

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


Module: ``files``
==================================================

- **list files [DIRECTORY]**

- **glob files PARTIALPATH**

- **get file info PATH**

- **cat file FILE**

- **write file FILE**

- **upload file DIRECTORY LOCALFILE**

- **delete file trash [DAYS]**


Arguments:

- Optional DIRECTORY is a remote directory
- PATH can refer to either a remote directory or a remote file
- PARTIALPATH is an incomplete remote PATH
- FILE is a remote file
- LOCALFILE is a local file

Use ‘/’ to separate subdirectory components in DIRECTORY, PATH,
PARTIALPATH or FILE. For example, a DIRECTORY could be
public_html/images or a PATH could be public_ftp/.htacccess.

All the remote arguments are relative to the remote user’s login
directory, e.g., public corresponds to <remote login directory>/public.

**COMMANDS**


**list files DIRECTORY**

Return a list of files and subdirectories in DIRECTORY

*Example*

.. code:: sh

    $ cpanel list files public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_files/

**glob files PARTIALPATH**

Return a list of files and subdirectories whose names start
with PARTIALPATH. For instance, /public matches /public_html and
/public_ftp.

*Example*

.. code:: sh

    $ cpanel glob files /public

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/autocompletedir/

**get file info PATH**

Return file information about PATH.

*Examples*

.. code:: sh

    $ cpanel get file info ssl
    $ cpanel get file info .bashrc
    $ cpanel get file info public_html/.htaccess

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_file_information/

**cat file FILE**

Return the contents of FILE. Note that only UTF-8 encoded files are supported.

*Examples*

.. code:: sh

    $ cpanel cat file .mysqlhistory
    $ cpanel cat file public_html/.htaccess

**write file FILE CONTENTS**

Write CONTENTS as a remote text FILE.
Note that only UTF-8 encoded content is supported.
Escape codes, such as ``\n``, ``\t`` and others, are supported.

*Examples*

.. code:: sh

    $ cpanel write file public_html/index.txt "Hallo\nTschüss\n"

**upload file DIRECTORY LOCALFILE**

Upload a LOCALFILE to remote DIRECTORY .
If the remote DIRECTORY doesn’t exist, it will be created.

*Examples*

.. code:: sh

    $ cpanel upload file public_html index.html

**delete file trash [DAYS]**

Delete the contents of the .trash directory in the user’s home.
Optional DAYS will only delete files older than DAYS days.
By default, all files are deleted.

*Examples*

.. code:: sh

    $ cpanel delete file trash
    $ cpanel delete file trash 31


Module: ``mail``
==================================================

- **list mail accounts**

- **list mail filters ACCOUNT**

- **get mail filter ACCOUNT FILTERNAME**

- **set mail filter ACCOUNT FILE**

- **delete mail filter ACCOUNT FILTERNAME**


**COMMANDS**


**list mail accounts**

List cPanel email accounts.

*Example*

.. code:: sh

    $ cpanel list mail accounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_pops/

**list mail filters ACCOUNT**

List mail filters associated to ACCOUNT. Output is a JSON-formatted
array of filter names.
ACCOUNT is the name of a cPanel email account, usually user@domain

*Example*

.. code:: sh

    $ cpanel list mail filters scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_filters/

**get mail filter ACCOUNT FILTERNAME**

Return a JSON-formatted description of email filter FILTERNAME associated
to email ACCOUNT. To get a list of current filter names, use
‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel get mail filter scott@example.com spamkiller

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_filter/

**set mail filter ACCOUNT FILE**

Create or update an email filter associated with email ACCOUNT.
If the filter already exists, it updates it; otherwise, it creates a new filter.
Use a JSON FILE to describe the filter rules. This JSON FILE has the same
textual format as the output from ‘cpanel get mail filter’, so the easiest way
to create a new filter is to dump an existing filter into a filter.json file,
edit it and then upload it with ‘cpanel set mail filter’.
See the EXAMPLE below.

*Example*

.. code:: sh

    $ cpanel get mail filter scott@example.com spamkiller > filter.json
    $ cpanel set mail filter scott@example.com filter.json

**delete mail filter ACCOUNT FILTERNAME**

Delete email filter FILTERNAME associated to ACCOUNT. To get a list of current
filter names, use ‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel delete mail filter scott@example.com spamkiller

