..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``mailman``
==================================================

`Leer en español </es/latest/reference/mailman.html>`_

- **add mailman list LISTNAME@DOMAIN PASSWORD [private]**
- **delete mailman list LISTNAME@DOMAIN**
- **count mailman lists**
- **list mailman lists**
- **add mailman delegates LISTNAME@DOMAIN EMAIL...**
- **delete mailman delegate LISTNAME@DOMAIN EMAIL...**
- **list mailman delegates LISTNAME@DOMAIN**
- **check mailman delegate EMAIL**
- **generate mailman password LISTNAME@DOMAIN**
- **set mailman password LISTNAME@DOMAIN PASSWORD**
- **get mailman usage**
- **set mailman private LISTNAME@DOMAIN**
- **set mailman public LISTNAME@DOMAIN**

**COMMANDS**


**add mailman list LISTNAME@DOMAIN PASSWORD [private]**

Create a new mailing list named LISTNAME for DOMAIN, using PASSWORD.
By default, a mailing list is public, i.e, anyone can subscribe and
read the archives. If ‘private’ is passed as an option, then make
the mailing list private, so that subscriptions need to be approved
by an administrator and only subscribed members can access the archives.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Examples*

.. code:: sh

    $ cpanel add mailman list private-list@example.com tiger private
    $ cpanel add mailman list public-list@example.com tiger

**delete mailman list LISTNAME@DOMAIN**

Delete the mailing list identified by LISTNAME@DOMAIN.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel delete mailman list private-list@example.com

**count mailman lists**

Count the number of mailing lists associated to your cPanel account.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel count mailman lists

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/count_lists/

**list mailman lists**

List the mailing lists of your cPanel account, along with detailed
information of each mailing list.

*Example*

.. code:: sh

    $ cpanel list mailman lists

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_lists/

**add mailman delegates LISTNAME@DOMAIN EMAIL...**

Add one or more delegate EMAILS to the mailing list identified by
LISTNAME@DOMAIN.

A delegate is a subscriber to the mailing list with administrative
privileges.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel add mailman delegates private-list@example.com \ 
          scott@example.com larry@example.com

**list mailman delegates LISTNAME@DOMAIN**

List the delegates of the mailing list identified by LISTNAME@DOMAIN.

A delegate is a subscriber to the mailing list with administrative
privileges.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel list mailman delegates private-list@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_mailman_delegates/

**delete mailman delegates LISTNAME@DOMAIN EMAIL...**

Delete one or more delegate EMAILS from the mailing list identified by
LISTNAME@DOMAIN.

A delegate is a subscriber to the mailing list with administrative
privileges.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel delete mailman delegates private-list@example.com \ 
          scott@example.com larry@example.com

**check mailman delegate EMAIL**

Return 1 if EMAIL is a delegate in any mailing list.

A delegate is a subscriber to the mailing list with administrative
privileges.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel check mailman delegate scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/has_delegated_mailman_lists/

**generate mailman password LISTNAME@DOMAIN**

Generate a one-time password for the mailing list identified by
LISTNAME@DOMAIN. This password will expire after one use.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel generate mailman password private-list@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/generate_mailman_otp/

**set mailman password LISTNAME@DOMAIN PASSWORD**

Set a new PASSWORD for the mailing list identified by LISTNAME@DOMAIN.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel set mailman password private-list@example.com tiger

**get mailman usage**

Return the total disk usage of all mailing lists associated to your
cPanel account.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel get mailman usage

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_lists_total_disk_usage/

**set mailman private LISTNAME@DOMAIN**

Make a mailing list identified by LISTNAME@DOMAIN private.
In a a private mailing list subscriptions need to be approved by an
administrator and only subscribed members can access the archives.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel set mailman private private-list@example.com

**set mailman public LISTNAME@DOMAIN**

Make a mailing list identified by LISTNAME@DOMAIN public.
In a public mailing list anyone can subscribe and archives are
publicly accesible, even to non-subscribers.

Mailing lists are managed using the Mailman application. For further
information on Mailman see https://wiki.list.org/DOC/Home

*Example*

.. code:: sh

    $ cpanel set mailman public public-list@example.com


