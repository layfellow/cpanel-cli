..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``backup``
==================================================

`Leer en español </es/latest/reference/backup.html>`_

- **create backup home [EMAIL]**
- **create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**
- **create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]**
- **list backups**
- **restore backup TARBALL**

**COMMANDS**


All ‘create backup’ commands create a backup TARBALL (a .tar.gz file) of
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

    $ cpanel create backup home
    $ cpanel create backup home scott@example.com
    $ cpanel create backup ftp scott tiger ftp.example.com
    $ cpanel create backup ftp scott tiger ftp.example.com /backup
    $ cpanel create backup scp scott tiger ssh.example.com /backup scott@example.com

**list backups**

List the account’s backup files.

*Example*

.. code:: sh

    $ cpanel list backups

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_backups/

**restore backup TARBALL**

Restore a full backup of the user’s home directory in TARBALL.
This TARBALL must have been previously created with a ‘cpanel create backup ...’ command
and *it must be already placed in the user’s home directory*.

*Example*

.. code:: sh

    $ cpanel restore backup backup-3.6.2022_11-35-42_scott.tar.gz


