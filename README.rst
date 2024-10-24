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

Swiftly execute commands in a terminal to manage a website, bypassing the need to log
into `cPanel`_ and navigate through its web interface. This utility can also be
seamlessly integrated into scripting tasks.

.. _cPanel: https://en.wikipedia.org/wiki/CPanel

A portion of the cPanel UAPI (Unrestricted API) is implemented, enabling you to
perform a wide array of functions with ease.

.. |cpanel_cli_icon| image:: https://raw.githubusercontent.com/layfellow/cpanel-cli/master/doc/_static/cpanel-cli-salmon.svg
   :width: 100
   :align: bottom

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

.. _`Windows`: #what-about-windows

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

User’s Guide
============

See the User’s Guide at  https://cpanel-cli.readthedocs.io/en/stable/ for detailed
installation and configuration instructions, as well as a complete reference of the
implemented API functions.


Contributing
============

Pull requests are more than welcome. See `CONTRIBUTING`_ for a detailed guide on
how to collaborate with this project.

.. _`CONTRIBUTING`: https://github.com/layfellow/cpanel-cli/blob/main/CONTRIBUTING.rst

What about Windows?
===================

**cpanel-cli** should work on Windows 10/11 using `WSL 2`_ (Windows Subsystem for Linux).

.. _`WSL 2`: https://docs.microsoft.com/en-us/windows/wsl/about

Unfortunately I don’t have access to a Windows system, so I can’t confirm this.


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

Ejecute comandos rápidamente en una terminal para gestionar un sitio web,
evitando la necesidad de iniciar sesión en `cPanel`_ y navegar por su interfaz
web. Esta utilidad también se puede integrar sin problemas en tareas de scripting.

Se implementa una parte de la UAPI (API sin restricciones) de cPanel, lo que
le permite realizar una amplia gama de funciones con facilidad.

Algunos ejemplos:

- Crear una copia de seguridad de la cuenta y almacenarla en el directorio home del usuario remoto:

  .. code:: sh

      $ cpanel create backup home scott@example.com

- Escribir directamente archivos en el directorio home del usuario remoto:

  .. code:: sh

      $ cpanel write file public_html/index.txt "Hallo\nTschüss\n"

- Crear un nuevo usuario FTP con una cuota y un directorio personal:

  .. code:: sh

      $ cpanel create ftp bill@example.com 'password' 1024 my_ftp

- Crear una respuesta automática de correo electrónico:

  .. code:: sh

      $ cpanel set mail autoresponder \
        scott@example.com \
        "Bruce Scott" \
        "Este es mensaje automático" \
        "No estoy disponible por el momento, por favor contacte a mi jefe." \
        "Tomorrow 6 PM" \
        "December 15, 8:00 AM"

- Cambiar a francés el idioma de la interfaz de usuario de cPanel:

  .. code:: sh

      $ cpanel set locale fr

- Listar las características disponibles de cPanel:

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

- Listar las cuentas de correo electrónico de  cPanel:

  .. code:: sh

      $ cpanel list mail accounts

        [
            {
            "email": "scott@example.com",
            . . .
            }
        ]


Y muchas cosas más. Con el tiempo espero cubrir completamente las más de 500
funciones disponibles en el API.

La salida es JSON, por lo que es fácilmente analizable utilizando
un `procesador CLI de JSON, como por ejemplo jq`_

.. _`procesador CLI de JSON, como por ejemplo jq`: https://stedolan.github.io/jq/

Consulte la `Guía`_ del usuario para una referencia completa de las
funciones implementadas de la API.

.. _`Guía`: https://cpanel-cli.readthedocs.io/es/stable/

Guía rápida
===========

**cpanel-cli** funciona en Linux y macOS (podría funcionar `en Windows`_) y
requiere Python 3.11 o posterior.

Para Linux, instale Python 3.11 o posterior utilizando el gestor de paquetes
de su distro.

Para macOS, instale Python 3.11 o posterior usando Homebrew_.

.. _`en Windows`: #se-puede-usar-en-windows

Cree un archivo ``.cpanelrc`` en su directorio ``$HOME`` con el siguiente contenido:

    .. code:: sh

        hostname=example.com
        username=scott
        utoken=ABCDEFGHIJKLMNOPQSRTUVWXYZ012345

- ``hostname`` es el nombre de host su instancia de cPanel
- ``username`` es su nombre de usuario en la instancia
- ``utoken`` es un token API asociado con el ``username``. Lea `cómo crear un token API`_.

.. _`cómo crear un token API`: https://docs.cpanel.net/knowledge-base/security/how-to-use-cpanel-api-tokens/#create-an-api-token

A continuación, ejecute:

.. code:: sh

    $ python3 -m pip install --user cpanel-cli


Pruebe la instalación:

.. code:: sh

    $ cpanel --version

Guía del usuario
================

Consulte la Guía del usuario en https://cpanel-cli.readthedocs.io/es/stable/
para instrucciones detalladas de instalación y configuración, así
como una referencia completa de las funciones implementadas del API.


Cómo contribuir
===============

Los pull requests son más que bienvenidos. Consulte `CONTRIBUTING en español`_
para una guía detallada de cómo colaborar con este proyecto.

.. _`CONTRIBUTING en español`: https://github.com/layfellow/cpanel-cli/blob/main/CONTRIBUTING.rst#como-contribuir

¿Se puede usar en Windows?
==========================

**cpanel-cli** debería funcionar en Windows 10/11 vía `WSL 2`_ (Windows Subsystem for Linux).

Desafortunadamente no tengo acceso a un sistema Windows, así que no puedo confirmarlo.
