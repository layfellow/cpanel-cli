..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``themes``
==================================================

`Leer en español </es/latest/reference/themes.html>`_

- **list themes**
- **get theme**
- **set theme NAME**

A theme is a customized look and feel for the cPanel user interface. The default
cPanel theme is ‘jupiter’; another popular theme is ‘paper lantern’.

**COMMANDS**


**list themes**

Return all the available themes.

*Example*

.. code:: sh

    $ cpanel list themes

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Themes::list/

**get theme**

Return the current theme.

*Example*

.. code:: sh

    $ cpanel get theme

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_theme_base/

**set theme NAME**

Set the current theme to NAME.
NAME must be one the available themes reported by ‘cpanel list themes’.

*Example*

.. code:: sh

    $ cpanel set theme paper_lantern


