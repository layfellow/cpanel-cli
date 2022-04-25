..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``styles``
==================================================

`Leer en español </es/latest/reference/styles.html>`_

- **list styles**
- **get style**
- **set style NAME**
- **default style NAME**

**COMMANDS**


A style is a variation of a user interface theme for cPanel. For example, the
‘paper lantern’ theme has four styles: ‘basic’, ‘dark’, ‘light’ and ‘glass’.

**list styles**

Return all the available user interface styles.

*Example*

.. code:: sh

    $ cpanel list styles

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list/

**get style**

Return the current user interface style.

*Example*

.. code:: sh

    $ cpanel get style

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/current/

**set style NAME**

Set the current user interface style to NAME.
NAME must be one of ‘basic’, ‘dark’, ‘light’ or ‘glass’

*Example*

.. code:: sh

    $ cpanel set style dark

**default style NAME**

Set the default user interface style to NAME.
NAME must be one of ‘basic’, ‘dark’, ‘light’ or ‘glass’

*Example*

.. code:: sh

    $ cpanel default style basic


