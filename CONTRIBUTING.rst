=================
How to contribute
=================

Development environment
=======================

``cpanel-cli`` was developed on Ubuntu Linux 21.07 “Hirsute Hippo”. There are no
special requirements, so a standard install on any Linux distro or macOS version
supporting at least Python 3.9 should work.

To prepare the development environment, follow the instructions below depending
on your OS:

macOS “Catalina” or higher
--------------------------

.. code:: sh
    
    $ brew install python@3.9

Then add the following paths to your ``PATH``:

.. code:: sh

    PATH="$PATH:/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin"
    export $PATH


Ubuntu Linux 21.04 or higher
----------------------------

.. code:: sh

    $ sudo apt install python3.9 python3-pip python3.9-venv
