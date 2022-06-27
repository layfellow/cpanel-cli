============
Installation
============

`Leer en español </es/latest/installation.html>`_

Requirements
============

- Linux or macOS; it might work `on Windows`_
- Python 3.9 or later

.. _`on Windows`: #what-about-installing-on-windows

Installation on Linux
=====================

Install Python 3.9 or later using your distro’s package manager.

Then run:

.. code:: sh

    $ python3 -m pip install --user cpanel-cli

Test the installation using:

.. code:: sh

    $ cpanel --version

Tested on Ubuntu 21.10 “Impish Indri”, but it has no specific Ubuntu requirements, so any
Linux distro with Python 3.9 or later should work.

Installation on macOS
=====================

Install Python 3.9 or later using `Homebrew <https://brew.sh/>`_.

Then run:

.. code:: sh

    $ python3 -m pip install --user cpanel-cli

Test the installation using:

.. code:: sh

    $ cpanel --version

Tested on macOS 10.15.7 “Catalina”; should also work on “Big Sur” or later.

What about installing on Windows?
=================================

I suspect this should work on Windows 10/11 using `WSL 2`_ (Windows Subsystem for Linux).

.. _`WSL 2`: https://docs.microsoft.com/en-us/windows/wsl/about

Unfortunately, I don’t have access to a Windows system, so I can’t confirm this.
Pull requests are very much welcome in case anyone wants to try out it and contribute.

Authentication
==============

To authenticate against your cPanel instance, the recommended way is to create a
``.cpanelrc`` file in your ``$HOME`` directory with the following contents:

.. code:: sh

    hostname=example.com
    username=scott
    utoken=ABCDEFGHIJKLMNOPQSRTUVWXYZ012345

- ``hostname`` is the hostname of your cPanel instance
- ``username`` is your user name on your instance
- ``utoken`` is an API token associated with ``username``. See `How to use cPanel API tokens`_ for
  further information on how to create tokens.

.. _`How to use cPanel API tokens`: https://docs.cpanel.net/knowledge-base/security/how-to-use-cpanel-api-tokens/

Alternatively, you can set the following environmental variables in your shell:

- ``CPANEL_HOSTNAME``
- ``CPANEL_USERNAME``
- ``CPANEL_UTOKEN``

For example:

.. code:: sh

    $ export CPANEL_HOSTNAME=example.com
    $ export CPANEL_USERNAME=scott
    $ export CPANEL_UTOKEN=ABCDEFGHIJKLMNOPQSRTUVWXYZ012345
    $ cpanel list features
  
Or you can pass the credentials directly on the command line using the ``-H``, ``-U`` and
``-T`` options. For example:

.. code:: sh

    $ cpanel -H example.com -U scott -T ABCDEFGHIJKLMNOPQSRTUVWXYZ012345 list features

Options passed on the command line override environmental variables, which in turn override
``.cpanelrc`` values.
