=============================
cPanel Command Line Interface
=============================

`Leer en español </es/latest/index.html>`_

A command line interface for the cPanel Unrestricted API.

Quickly execute commands in a terminal to manage a website instead of logging
into `cPanel`_ and clicking your way around the web interface. You can also use
this utility in scripting jobs.

.. _cPanel: https://en.wikipedia.org/wiki/CPanel

Some examples
=============

- Print help:

  .. code:: sh

      $ cpanel help

- Print help on implemented modules:

  .. code:: sh

      $ cpanel help modules

- Print help on module ``mail``:

  .. code:: sh

      $ cpanel help mail

- List cPanel email accounts:

  .. code:: sh

      $ cpanel list mail accounts

- Get a description of email filter ``spamkiller`` associated to email
  account ``scott@example.com``:

  .. code:: sh

      $ cpanel get mail filter scott@example.com spamkiller

The output is generally JSON, so it’s easily parsable using, e.g., `jq`_

.. _jq: https://stedolan.github.io/jq/

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
