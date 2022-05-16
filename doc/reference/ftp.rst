..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``ftp``
==================================================

`Leer en español </es/latest/reference/ftp.html>`_

- **create ftp USER\@DOMAIN PASSWORD QUOTA [DIRECTORY]**
- **check ftp USER\@DOMAIN**
- **get ftp USER\@DOMAIN**
- **get ftp quota USER\@DOMAIN**
- **set ftp quota USER\@DOMAIN QUOTA**
- **set ftp dir USER\@DOMAIN DIR**
- **set ftp password USER\@DOMAIN PASSWORD**
- **list ftp accounts**
- **list ftp sessions**
- **kill ftp session USER\@DOMAIN**
- **delete ftp USER\@DOMAIN**
- **get ftp port**
- **get ftp server**
- **enable ftp anon [incoming]**
- **disable ftp anon [incoming]**
- **get ftp anon [incoming]**
- **get ftp welcome**
- **set ftp welcome MESSAGE**

**COMMANDS**


**create ftp USER\@DOMAIN PASSWORD QUOTA [DIRECTORY]**

Create a new FTP account using USER\@DOMAIN and PASSWORD.
The DOMAIN must be a domain owned by your cPanel user.
The newly created user will be allocated QUOTA megabytes of space;
use ‘0’ for QUOTA to set an unlimited quota.

Optionally, you can provide the FTP account’s home DIRECTORY to
create. If you don’t provide a DIRECTORY, <DOMAIN>_ftp will be
used. You can later change this using ‘cpanel set ftp dir’ (see below).

Note that DIRECTORY is not an absolute path, but a path relative to
the cPanel user’s remote login directory, i.e., /my_ftp corresponds
to <remote login directory>/my_ftp.

*Example*

.. code:: sh

    $ cpanel create ftp scott@example.com 'tiger' 1024
    $ cpanel create ftp scott@example.com 'tiger' 1024 my_ftp

Access the account using an FTP client:

- FTP host:     ftp.example.com
- FTP username: scott@example.com
- FTP password: tiger

**check ftp USER\@DOMAIN**

Check whether the FTP account identified by USER\@DOMAIN exists.
Return ‘OK’ if it exists, or an error if it doesn’t.

*Example*

.. code:: sh

    $ cpanel check ftp scott@example.com

**get ftp USER\@DOMAIN**

Get information about FTP account USER\@DOMAIN.

*Example*

.. code:: sh

    $ cpanel get ftp scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_ftp_with_disk/

**get ftp quota USER\@DOMAIN**

Return the disk quota in megabytes allocated to FTP USER\@DOMAIN,
or ‘unlimited’ if it has no quota.

*Example*

.. code:: sh

    $ cpanel get ftp quota scott@example.com

**set ftp quota USER\@DOMAIN QUOTA**

Set the disk quota in megabytes allocated to FTP USER\@DOMAIN;
use ‘0’ for QUOTA to set an unlimited quota.

*Examples*

.. code:: sh

    $ cpanel set ftp quota scott@example.com 2048
    $ cpanel set ftp quota scott@example.com 0

**set ftp dir USER\@DOMAIN DIRECTORY**

Set the home DIRECTORY for FTP account USER\@DOMAIN. If DIRECTORY
doesn’t exist, it is created.

Note that DIRECTORY is not an absolute path, but a path relative to
the cPanel user’s remote login directory, i.e., /my_ftp corresponds
to <remote login directory>/my_ftp.

To get the current home directory for USER\@DOMAIN, use
‘cpanel get ftp’ (see above).

To list all the directories in cPanel user’s remote login directory,
use ‘cpanel list files / | jq .[].fullpath’

*Example*

.. code:: sh

    $ cpanel set ftp dir scott@example.com my_ftp

**set ftp password USER\@DOMAIN PASSWORD**

Change the PASSWORD of FTP USER\@DOMAIN.

*Examples*

.. code:: sh

    $ cpanel set ftp password scott@example.com 'tiger'

**list ftp accounts**

List all the FTP accounts on the cPanel server, along with disk
usage information and other data.

*Example*

.. code:: sh

    $ cpanel list ftp accounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_ftp_with_disk/

**list ftp sessions**

List the active FTP sessions.

*Example*

.. code:: sh

    $ cpanel list ftp sessions

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_sessions/

**kill ftp session USER\@DOMAIN**

Kill the active FTP session associated to USER\@DOMAIN.
Use ‘cpanel list ftp sessions’ to list all active sessions.
Use ‘all’ to kill all active sessions.

*Examples*

.. code:: sh

    $ cpanel kill ftp session all
    $ cpanel kill ftp session scott@example.com

**delete ftp USER\@DOMAIN**

Delete the FTP account identified by USER\@DOMAIN.
Be advised that the USER’s FTP directory on the cPanel will also
be deleted.

*Example*

.. code:: sh

    $ cpanel delete ftp scott@example.com

**get ftp port**

Return the FTP port open on the server.

*Example*

.. code:: sh

    $ cpanel get ftp port

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_port/

**get ftp server**

Return information about the FTP server software.

*Example*

.. code:: sh

    $ cpanel get ftp server

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_ftp_daemon_info/

**enable ftp anon [incoming]**

Enable anonymous FTP users to download files. If ‘incoming’ is passed,
also enable the anonymous user to upload files.

*Examples*

.. code:: sh

    $ cpanel enable ftp anon
    $ cpanel enable ftp anon incoming

Assuming your cPanel domain is ‘example.com’, then an anonymous user
can access your FTP server using the following (no password required):

- FTP host:     ftp.example.com
- FTP username: anonymous@example.com

If ‘incoming’ is enabled, the anonymous user can also upload files
to the /incoming directory.

For further information, see:
https://docs.cpanel.net/cpanel/files/anonymous-ftp/

**disable ftp anon [incoming]**

Disable anonymous FTP users to download files. If ‘incoming’ is passed,
also disable the anonymous user to upload files.

See ‘cpanel enable ftp anon’ above for further details.

*Examples*

.. code:: sh

    $ cpanel disable ftp anon
    $ cpanel disable ftp anon incoming

**get ftp anon [incoming]**

Return whether anonymous FTP users are allowed. If ‘incoming’ is passed,
return whether the anonymous FTP user is allowed to upload files.

See ‘cpanel enable ftp anon’ above for further details.

*Examples*

.. code:: sh

    $ cpanel get ftp anon
    $ cpanel get ftp anon incoming

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/allows_anonymous_ftp/

**get ftp welcome**

Return the FTP welcome message for anonymous users.

*Example*

.. code:: sh

    $ cpanel get ftp welcome

**get ftp welcome MESSAGE**

Set the FTP welcome message for anonymous users.

*Example*

.. code:: sh

    $ cpanel set ftp welcome 'Welcome to the FTP server!'

