.. image:: https://img.shields.io/pypi/v/cpanel-cli
    :alt: PyPI
    :target: https://pypi.org/project/cpanel-cli/

.. image:: https://img.shields.io/pypi/pyversions/cpanel-cli
    :alt: Python version
    :target: https://pypi.org/project/cpanel-cli/

.. image:: https://readthedocs.org/projects/cpanel-cli/badge/?version=latest
    :alt: Documentation Status
    :target: https://cpanel-cli.readthedocs.io/en/latest/?badge=latest

=============================
cPanel Command Line Interface
=============================

|cpanel_cli_icon|

`LÉAME en español <#interfaz-de-linea-de-comandos-para-cpanel>`_

A command line interface for the cPanel Unrestricted API.

Quickly execute commands in a terminal to manage a website instead of logging
into `cPanel`_ and clicking your way around the web interface. You can also use
this utility in scripting jobs.

.. _cPanel: https://en.wikipedia.org/wiki/CPanel

.. |cpanel_cli_icon| image:: https://raw.githubusercontent.com/layfellow/cpanel-cli/master/doc/_static/cpanel-cli-salmon.svg
   :width: 100
   :align: bottom

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

For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/

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

Install Python 3.9 or later using Homebrew_.

.. _Homebrew: https://brew.sh/

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

Contributing
============

See `CONTRIBUTING <https://github.com/layfellow/cpanel-cli/blob/main/CONTRIBUTING.rst>`_

----

.. image:: https://img.shields.io/pypi/v/cpanel-cli
    :alt: PyPI
    :target: https://pypi.org/project/cpanel-cli/

.. image:: https://img.shields.io/pypi/pyversions/cpanel-cli
    :alt: Versión de Python
    :target: https://pypi.org/project/cpanel-cli/

.. image:: https://readthedocs.org/projects/cpanel-cli/badge/?version=latest
    :alt: Status de la documentación
    :target: https://cpanel-cli.readthedocs.io/es/latest/?badge=latest

=========================================
Interfaz de línea de comandos para cPanel
=========================================

|cpanel_cli_icon|

`README in English <#cpanel-command-line-interface>`_

Una interfaz de línea de comandos para la Unrestricted API de cPanel.

Ejecute rápidamente comandos en un terminal en lugar de iniciar sesión en la interfaz
web de `cPanel`_. También puede usar este utilitario para trabajos de *scripting*.

Algunos ejemplos
================

- Imprime la ayuda:

  .. code:: sh

      $ cpanel help

- Imprime la ayuda de los módulos implementados:

  .. code:: sh

      $ cpanel help modules

- Imprime la ayuda del módulo ``mail``:

  .. code:: sh

      $ cpanel help mail

- Lista las cuentas de correo de cPanel:

  .. code:: sh

      $ cpanel list mail accounts

- Obtiene la description del filtro de correo ``spamkiller`` asociado a la cuenta de
  de correo ``scott@example.com``:

  .. code:: sh

      $ cpanel get mail filter scott@example.com spamkiller

La salida es generalmente JSON, por lo que es fácilmente analizable utilizando, por ejemplo, `jq`_

Guía del usuario
================

La guía del usuario completa se encuentra en: https://cpanel-cli.readthedocs.io/es/latest/

Requisitos
==========

- Linux o macOS; tal vez podría funcionar `en Windows`_
- Python 3.9 o superior

.. _`en Windows`: #se-puede-instalar-en-windows

Instalación en Linux
====================

Instale Python 3.9 o superior usando el gestor de paquetes de su distribución.

Luego ejecute:

.. code:: sh

    $ python3 -m pip install --user cpanel-cli

Pruebe la instalación con:

.. code:: sh

    $ cpanel --version

Probado en Ubuntu 21.10 “Impish Indri”, pero no tiene requisitos específicos de Ubuntu,
por lo que cualquier distribución de Linux con Python 3.9 o posterior debería funcionar.

Instalación en macOS
====================

Instale Python 3.9 o posterior usando Homebrew_.

Luego ejecute:

.. code:: sh

    $ python3 -m pip install --user cpanel-cli

Pruebe la instalación con:

.. code:: sh

    $ cpanel --version

Probado en macOS 10.15.7 “Catalina”; también debería funcionar en “Big Sur” o posterior.

¿Se puede instalar en Windows?
==============================

Sospecho que esto debería funcionar en Windows 10/11 usando `WSL 2`_ (Windows Subsystem for Linux).

Desafortunadamente, no tengo acceso a un sistema Windows, así que no puedo confirmarlo.
Los pull requests son bienvenidos en caso de que alguien quiera probarlo y contribuir.

Cómo contribuir
===============

Véase `CONTRIBUTING en español <https://github.com/layfellow/cpanel-cli/blob/main/CONTRIBUTING.rst#como-contribuir>`_
