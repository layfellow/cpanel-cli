=================
How to contribute
=================

`Leer en español </es/latest/contributing.html>`_

To contribute, just fork this repository, start a new branch and open a `pull request`_.

.. _`pull request`: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

``cpanel-cli`` is written in Python 3.9. I organized the code into a standard tree::

    cpanel-cli
    ├── CONTRIBUTING.rst
    ├── cpanel
    │   ├── cli.py
    │   ├── core.py
    │   ├── __init__.py
    │   └── __main__.py
    ├── doc
    │   ├── conf.py
    │   ├── index.rst
    │   ├── locale
    │   │   └── es
    │   │       └── LC_MESSAGES
    │   │           └── index.po
    │   └── requirements.txt
    ├── LICENSE
    ├── Makefile
    ├── README.rst
    ├── .readthedocs.yaml
    ├── requirements-dev.txt
    ├── requirements.txt
    ├── setup.py
    ├── test
    │   ├── cpanelrc.test.example
    │   └── test_core.py
    └── tox.ini

``cpanel-cli`` contains the main source code.

``doc`` contains the documentation sources, written in `reStructuredText`_ and processed using `Sphinx`_.
The main configuration file for Sphinx is ``doc/conf.py``. The Sphinx version and theme used
to build the documentation are in ``doc/requirements.txt``.

``.readthedocs.yaml`` is a `configuration file for Read the Docs`_. The remote Sphinx build system
uses this file.

.. _`configuration file for Read the Docs`: https://docs.readthedocs.io/en/stable/config-file/index.html
.. _`reStructuredText`: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _Sphinx: https://www.sphinx-doc.org/

I maintain a Spanish translation of the documentation, generated using strings from a
catalog file ``locale/es/LC_MESSAGES/index.po``.

I’m using a ``Makefile`` to automate all phases of the development life cycle. (`Make and Makefiles are awesome`_.)

.. _`Make and Makefiles are awesome`: https://mplanchard.com/posts/make-and-makefiles-are-awesome.html

``requirements-dev.txt`` contains the required packages for the Python `Development environment`_,
while ``requirements.txt`` contains the runtime dependencies.

``setup.py`` is the main script for `setuptools`_, used for packaging and distributing this project.
I know that the use of ``setup.py`` is currently discouraged, so I will probably replace it
with a more modern packaging system like `Poetry`_, but I’m being conservative here and sticking
with ``setup.py`` for now. (But notice I’m calling it indirectly using ``python -m build``,
as `recommended`_.)

.. _setuptools: https://setuptools.pypa.io/en/latest/userguide/quickstart.html
.. _Poetry: https://python-poetry.org/
.. _recommended: https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html

``test`` contains a set of unit API tests. They’re written using the `tox automation framework`_.
The code driving the tests is in ``test/test_core.py``; the main tox configuration file is ``tox.ini``.
These are *not* simple standalone unit tests, but API tests running against
a *live* cPanel instance. See `Running tests`_ below for further details.

.. _`tox automation framework`: https://tox.wiki/en/latest/index.html

Development environment
=======================

I developed ``cpanel-cli`` on Ubuntu Linux 21.10 “Impish Indri”. There are no
special requirements, so any Linux distro or macOS version supporting at least
Python 3.9 should work.

*On macOS “Catalina” or higher*

Install Python 3.9:

.. code:: sh

    $ brew install python@3.9

Then add the following to your ``PATH``:

.. code:: sh

    PATH="$PATH:/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin"
    export $PATH

Install GNU Make:

.. code:: sh

    $ brew install make

*On Ubuntu Linux 21.04 or higher*

Install Python 3.9:

.. code:: sh

    $ sudo apt install python3.9 python3-pip python3.9-venv

GNU Make is installed by default on Ubuntu. Check its availability using:

.. code:: sh

    $ make --version

*Other Linux distros*

Use your distro’s package manager to install Python 3.9 (or higher) and GNU Make.

Building a local ``cpanel-cli`` package from source
===================================================

You can build and install a local ``cpanel-cli`` package using:

.. code:: sh

    $ make install

This will:

1. Create a new virtual Python 3 environment in a ``venv`` directory

2. Install on it the required development packages listed in ``requirements-dev.txt``

3. Build a local Python package ``cpanel-cli``

Running the local executable
============================

To run the executable from the locally installed package, first activate the virtual environment
(you need to run this only once per session):

.. code:: sh

    $ source venv/bin/activate

Then you can execute the ``cpanel`` utility:

.. code:: sh

    $ cpanel --help

If you edit the sources, simply run ``make install`` to build and reinstall the local package.

Running the (optional) type checker
===================================

The Python sources are in the ``cpanel`` directory. You will notice they’re annotated using type
hints. I use them because IMHO they add clarity and robustness to Python
code. Read the `Python Type Checking Guide`_ for a good introduction to type checking in Python.

.. _`Python Type Checking Guide`: https://realpython.com/python-type-checking/

Since type hints are not actually checked by Python itself, you need an additional utility: a
*type checker*. (You can think of the type checker as another kind of linter.) My type checker
of choice for Python is Pyright_.

Running the type checker is optional — you can ignore this step.

To run Pyright, install it first:

.. code:: sh

    $ pip3 install --user pyright

Then run it using:

.. code:: sh

    $ make typecheck

.. _`Pyright`: https://github.com/Microsoft/pyright

Running tests
=============

I’m using the `tox automation framework`_ for a series of unit API tests.
The main code driving the tests is in ``test/test_core.py``; the main tox configuration file is
``tox.ini``.

These are *not* simple unit tests, but unit API tests running against a *live* cPanel instance.
To run the tests, you need access to a cPanel instance running on another host reachable from
the host you’re running the tests on.

To set the remote hosts credentials, make a copy of the provided ``cpanelrc.test.example`` file
and name it ``cpanelrc.test`` (keep in the ``test`` directory):

.. code:: sh

    $ cp test/cpanelrc.test.example test/cpanelrc.test

Then edit ``cpanelrc.test`` and set:

- The hostname of your cPanel instance
- The username of your cPanel account
- An `API token`_ associated to that username

**Token-based authentication is the only supported authentication method.**

.. _`API token`: https://docs.cpanel.net/knowledge-base/security/how-to-use-cpanel-api-tokens/

To run the tests, use:

.. code:: sh

    $ make test

The above command will hit the `cPanel UAPI REST interface`_ with most of the functions
implemented in ``cpanel-cli``. The remote state of cPanel is left unchanged, i.e.,
the tests are strictly non-destructive.

.. _`cPanel UAPI REST interface`: https://documentation.cpanel.net/display/DD/Use+WHM+API+to+Call+cPanel+API+and+UAPI

Packaging
=========

Packaging is done via good old ``setup.py``, which is the main script used as a backend for `setuptools`_.
This script is called indirectly via ``python -m build``. (I will probably replace it with
a more modern ``pyproject.toml`` soon.)

To run the packager, use:

.. code:: sh

    $ make package

The above command should generate the following two distribution files in the temporary ``dist`` directory:

.. code:: sh

    cpanel_cli-<version>-py3-none-any.whl
    cpanel-cli-<version>.tar.gz

where ``<version>`` is the release number set in ``cpanel/__init__.py``.

The tarball is the source archive; the wheel file is the built distribution archive. These files
are ready to be uploaded to the `Python Package Index`_.

.. _`Python Package Index`: https://pypi.org/

Building the documentation
==========================

The API documentation source files are in the ``doc`` directory. These comprise `reStructuredText`_
(``.rst``) files which are processed using `Sphinx`_ into groups of static HTML trees.

To build the documentation, use:

.. code:: sh

    $ make doc

The above command will generate several static HTML trees in ``doc/build/html``.
For example, it generates the default English documentation in ``doc/build/html/en`` —
the start page is a conventional ``index.html`` file.

This GitHub repository is currently connected to my `Read the Docs`_ account, so that
any committed (or merged) change that updates the documentation sources will automatically
trigger a remote Sphinx rebuild. The resulting updated HTML documentation will always be available at
`<https://cpanel-cli.readthedocs.io/en/latest/>`_

.. _`Read the Docs`: https://readthedocs.org/

The main configuration file for Sphinx is ``doc/conf.py``. The Sphinx version and theme used
to build the documentation are in ``doc/requirements.txt``.

Translations
============

The English language ``*.rst`` files in ``doc`` are the source documentation files. Any
translation is based on these documents. Translation is done on a string-by-string basis,
using the original English string as a key (``msgid``), and the corresponding translated
string as a value (``msgstr``). For example, for Spanish:

.. code::

    msgid "To be, or not to be, that is the question"
    msgstr "Ser o no ser, he ahí el dilema"

These ``msgid`` and ``msgstr`` pairs are kept in a *catalog* file (``*.po``), which is a
simple text file. These catalog files are stored in the ``doc/locale`` subdirectory.

I personally maintain a Spanish translation of the documentation in catalog files 
``doc/locale/es/LC_MESSAGES/*.po``.

Catalog ``.po`` files are compiled into ``.mo`` files using the Sphinx internationalization
utility. These compiled ``.mo`` files are later used to compose translated versions when
`Building the documentation`_.

Adding a translation
--------------------

To add a new translation:

1. Create a new catalog using:

   .. code:: sh

       $ make locale iso=<language code>

   where ``<language code>`` is the `ISO 639-1 code`_ corresponding to the new language. For
   example, to add a French translation you would use:

   .. code:: sh

       $ make locale iso=fr

   This would add a new ``locale/fr/LC_MESSAGES`` directory with several ``.po`` files in it.

2. Edit the ``.po`` files created in step 1 and insert the translated strings as
   ``msgstr`` fields. For example:

   .. code::

       msgid "Indices and tables"
       msgstr "Indices et tableaux"

3. Rebuild the documentation:

   .. code:: sh

       $ make doc

   The above command will create a new static HTML tree in ``doc/build/html/<language code>``.
   For example, for French, it will create a new tree in ``doc/build/html/fr``.

Correcting and expanding an existing translation
------------------------------------------------

If you edit the original ``doc/*.rst`` source documentation files, you need to update the
translations as well:

1. Run the following to update the catalog files:

   .. code:: sh

       $ make locale iso=<language code>

   where ``<language code>`` is the `ISO 639-1 code`_. You need to run it for every
   translated language.

2. The previous step will emit a report telling you which ``.po`` files need to be updated,
   for example:

   .. code::

       Update: doc/locale/es/LC_MESSAGES/reference.po +5, -2
       Update: doc/locale/es/LC_MESSAGES/contributing.po +9, -0

   Open the mentioned ``.po`` files and edit or add new ``msgstr`` strings. Be advised that some
   entries might get annotated as ``#, fuzzy``, which means the internationalization
   engine is not sure if there already exists a translation for the entry because of similarities
   with another entry. Just edit the ``msgstr`` text and delete the ``fuzzy`` line.

For further information, see the `Internationalization Guide`_

.. _`ISO 639-1 code`: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
.. _`Internationalization Guide`: https://www.sphinx-doc.org/en/master/usage/advanced/intl.html
