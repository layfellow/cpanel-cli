..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``features``
==================================================

`Leer en español </es/latest/reference/features.html>`_

- **list features**
- **get feature details**
- **has feature FEATURE**

**COMMANDS**


**list features**

List a cPanel account’s features.

*Example*

.. code:: sh

    $ cpanel list features

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_features/

**get feature details**

Get details for all available features. Details include whether the
feature is a plug-in or an add-on, and a long name.

*Example*

.. code:: sh

    $ cpanel get feature details

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_feature_metadata/

**has feature FEATURE**

Return ‘1’ if a cPanel account has FEATURE, ‘0’ if it doesn’t.
If FEATURE is an invalid name, return ‘null’.
For a list of valid FEATURE names, see ‘cpanel list features’.

*Example*

.. code:: sh

    $ cpanel has feature autossl


