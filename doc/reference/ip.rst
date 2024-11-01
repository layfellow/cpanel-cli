..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``ip``
==================================================

`Leer en español </es/latest/reference/ip.html>`_

- **block ip IPRANGE**
- **unblock ip IPRANGE**

IPRANGE can be a single address, a CDIR, or a hostname. See:
https://api.docs.cpanel.net/openapi/cpanel/operation/blockip-add-ip/
for a list of supported formats.

For a list of currently blocked IP ranges, you can use:

*Example*

.. code:: sh

    $ cpanel cat file /public_html/.htaccess | grep 'deny from'

**COMMANDS**


**block ip IPRANGE**

Block a range of IP addresses from accessing your account’s hosts.

*Example*

.. code:: sh

    $ cpanel block ip 192.168.0.1-192.168.0.58

**unblock ip IPRANGE**

Allow a range of IP addresses access to your account’s hosts.

*Example*

.. code:: sh

    $ cpanel unblock ip 192.168.0.1-192.168.0.58


