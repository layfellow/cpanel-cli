..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``files``
==================================================

`Leer en español </es/latest/reference/files.html>`_

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
Escape codes, such as ‘\n’, ‘\t’ and others, are supported.

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


