..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``dir``
==================================================

`Leer en español </es/latest/reference/dir.html>`_


``indexing``
==================================================

- **list dir indexing PATH**
- **get dir indexing PATH**
- **set dir indexing PATH TYPE**

The indexing of a remote directory controls how to present that directory
to a web browser if no default HTML index page is found.

There are four possible index settings:

- ‘inherit’: Use the parent directory’s setting.
- ‘disabled’ (No Indexing): do not list the directory contents.
- ‘standard’ (Show Filename Only): list only the directory’s file names.
- ‘fancy’: (Show Filename and Description) list the directory’s file names, sizes and types.

cPanel uses a .htaccess directive in the remote directory to control the
index settings. For instance, for ‘fancy’, it adds the following code to .htaccess:

Options +Indexes
IndexOptions +HTMLTable +FancyIndexing

See https://docs.cpanel.net/cpanel/advanced/indexes/ for further information.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., /public_html corresponds to
<remote login directory>/public_html.

**COMMANDS**


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



``privacy``
==================================================

- **list dir privacy PATH**
- **get dir privacy PATH**
- **enable dir privacy PATH**
- **disable dir privacy PATH**

cPanel can password-protect remote directories for privacy. Any attempt to
access a private directory using a web browser will prompt for a
username and password.

The actual underlying authentication method is Basic HTTP authentication;
these users and passwords are local to the directory, they are not cPanel users.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., /public_html corresponds to
<remote login directory>/public_html.

**COMMANDS**


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



``user``
==================================================

- **add dir user PATH USER PASSWORD**
- **delete dir user PATH USER**
- **list dir users PATH**

cPanel grants access to remote password-protected directories using
ad hoc users and passwords specific to every directory. Use the
commands below to manage these users.

cPanel stores the credentials in a .htpasswd file.
See https://en.wikipedia.org/wiki/.htpasswd for further information.

Note that the PATH in all commands below is not absolute, but relative to the
remote login directory, i.e., /public_html corresponds to
<remote login directory>/public_html.

**COMMANDS**


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

    $ cpanel list dir users /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/DirectoryPrivacy::list_users/



``protection``
==================================================

- **list dir protection PATH**

Leech protection adds some basic measures against the abuse of
password-protected directories. The system allows a maximum number of
logins per hour for a leech-protected directory.

See https://docs.cpanel.net/cpanel/security/leech-protection/ for further information.

**list dir protection PATH**

List leech protection status for PATH and its subdirectories (children).

*Example*

.. code:: sh

    $ cpanel list dir protection /public_html

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/DirectoryProtection-list_directories/


