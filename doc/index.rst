=============================
cPanel Command Line Interface
=============================

`Leer en español </es/stable/index.html>`_

A command line interface for the cPanel Unrestricted API.

Swiftly execute commands in a terminal to manage a website, bypassing the need to log
into `cPanel`_ and navigate through its web interface. This utility can also be
seamlessly integrated into scripting tasks.

.. _cPanel: https://en.wikipedia.org/wiki/CPanel

A portion of the cPanel UAPI (Unrestricted API) is implemented, enabling you to
perform a wide array of functions with ease.

Some examples:

- Create a backup of the account and store it in the remote user's home directory:

  .. code:: sh

      $ cpanel create backup home scott@example.com

- Directly write files to the remote user's home directory:

  .. code:: sh

      $ cpanel write file public_html/index.txt "Hallo\nTschüss\n"

- Create a new FTP user with a quota and personal directory:

  .. code:: sh

      $ cpanel create ftp bill@example.com 'password' 1024 my_ftp

- Create an email autoresponder:

  .. code:: sh

      $ cpanel set mail autoresponder \
        scott@example.com \
        "Bruce Scott" \
        "This is an automatic message" \
        "I’m currently unavailable, please contact my boss." \
        "Tomorrow 6 PM" \
        "December 15, 8:00 AM"

- Set the cPanel user interface language to French:

  .. code:: sh

      $ cpanel set locale fr

- List cPanel available features:

  .. code:: sh

      $ cpanel list features

      {
          "addoncgi": 0,
          "addondomains": 1,
          "agora": 1,
          . . .
          "webmail": 1,
          "webprotect": 1,
          "zoneedit": 1
      }

- List cPanel email accounts:

  .. code:: sh

      $ cpanel list mail accounts

        [
            {
            "email": "scott@example.com",
            . . .
            }
        ]

And many more things. I intend to eventually fully cover the 500+ API
functions available.

The output is JSON, so it’s easily parsable using a `CLI JSON processor, like jq`_

.. _`CLI JSON processor, like jq`: https://stedolan.github.io/jq/

See the User’s `Guide`_ for a complete reference of the implemented API
functions.

.. _`Guide`: https://cpanel-cli.readthedocs.io/en/stable/

Quick Start Guide
=================

**cpanel-cli** works on Linux and macOS (it might work on `Windows`_) and
requires Python 3.11 or later.

For Linux, install Python 3.11 or later using your distro’s package manager.

For macOS, install Python 3.11 or later using Homebrew_.

.. _`Windows`: installation.html#what-about-windows

.. _Homebrew: https://brew.sh/

Create a ``.cpanelrc`` file in your ``$HOME`` directory with the following contents:

    .. code:: sh

        hostname=example.com
        username=scott
        utoken=ABCDEFGHIJKLMNOPQSRTUVWXYZ012345

- ``hostname`` is the hostname of your cPanel instance
- ``username`` is your username in your instance
- ``utoken`` is an API token associated with ``username``. See `How to create an API token`_.

.. _`How to create an API token`: https://docs.cpanel.net/knowledge-base/security/how-to-use-cpanel-api-tokens/#create-an-api-token

Then run:

.. code:: sh

    $ python3 -m pip install --user cpanel-cli


Test the installation using:

.. code:: sh

    $ cpanel --version

For further instructions, see the `Installation`_ section of the User’s Guide.

.. _`Installation`: installation.html


User’s Guide
============

.. toctree::
   :maxdepth: 2

   installation
   reference

For developers
==============

.. toctree::
   :maxdepth: 2

   contributing

License
=======

cPanel CLI

`GNU General Public License v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_
