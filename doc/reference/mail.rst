..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``mail``
==================================================

`Leer en español </es/latest/reference/mail.html>`_


``accounts``
==================================================

- **count mail accounts**
- **list mail accounts**

**COMMANDS**


**count mail accounts**

Count the number of cPanel email accounts.

*Example*

.. code:: sh

    $ cpanel count mail accounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/count_pops/

**list mail accounts**

List cPanel email accounts.

*Example*

.. code:: sh

    $ cpanel list mail accounts

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_pops/



``settings``
==================================================

- **get mail settings ACCOUNT**

Get an ACCOUNT’s email settings.

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

*Example*

.. code:: sh

    $ cpanel get mail settings scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_client_settings/



``boxes``
==================================================

- **list mail boxes [ACCOUNT] [DIR]**

List the mailboxes (directories and files) for ACCOUNT.
If no ACCOUNT is passed, list the mailboxes for all mail accounts.
Optionally, you can restrict the listing to directory DIR.

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

*Examples*

.. code:: sh

    $ cpanel list mail boxes
    $ cpanel list mail boxes scott@example.com
    $ cpanel list mail boxes scott@example.com .Sent
    $ cpanel list mail boxes scott@example.com .spam

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/browse_mailbox/



``autoresponders``
==================================================

- **list mail autoresponders DOMAIN**
- **count mail autoresponders**
- **get mail autoresponder ACCOUNT**
- **set mail autoresponder ACCOUNT [FROM] [SUBJECT] [BODY] [START] [STOP]**
- **delete mail autoresponder ACCOUNT**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

**COMMANDS**


**list mail autoresponders DOMAIN**

List the autoresponders of all email accounts in DOMAIN.

*Example*

.. code:: sh

    $ cpanel list mail autoresponders example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_auto_responders/

**count mail autoresponders**

Return the number of autoresponders for all email accounts.

*Example*

.. code:: sh

    $ count mail autoresponders

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/count_auto_responders/

**count get mail autoresponder ACCOUNT**

Retrieve autoresponder information corresponding to ACCOUNT.

*Example*

.. code:: sh

    $ count get mail autoresponder scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_auto_responder/

**set mail autoresponder ACCOUNT [FROM] [SUBJECT] [BODY] [START] [STOP]**

Create an autoresponder for ACCOUNT.

FROM is the sender’s name; by default, the ACCOUNT email name is used.

SUBJECT is the subject of the autoresponse email; the default subject is
“This is an automatic message”

BODY is the text of the autoresponse email; the default body is
“I’m currently unavailable.”

START is when to enable the autoresponder; you can use a readable
expression parsable as a time and date, e.g., “now”, “tomorrow 9 AM”,
“December 20, 2022 19:00”, etc.
For more examples, see https://github.com/bear/parsedatetime
The default START time is “now”, meaning the autoresponder will be
immediately enabled.

STOP is when to disable the autoresponder; you can use a readable
expression as for START.
The default STOP time is a date far in the future, meaning the
autoresponder will be effectively enabled until you manually
disable it using ‘cpanel delete mail autoresponder’

*Examples*

.. code:: sh

    $ cpanel set mail autoresponder scott@example.com

    $ cpanel set mail autoresponder \ 
          scott@example.com \ 
          "Bruce Scott" \ 
          "Auto-response"

    $ cpanel set mail autoresponder \ 
          scott@example.com \ 
          "Bruce Scott" \ 
          "This is an automatic message" \ 
          "I’m currently unavailable, please contact my boss." \ 
          "Tomorrow 6 PM" \ 
          "December 15, 8:00 AM"

**delete mail autoresponder ACCOUNT**

Delete an autoresponder for ACCOUNT.

*Example*

.. code:: sh

    $ cpanel delete mail autoresponder scott@example.com



``filters``
==================================================

- **list mail filters ACCOUNT**
- **get mail filter ACCOUNT FILTERNAME**
- **set mail filter ACCOUNT FILE**
- **delete mail filter ACCOUNT FILTERNAME**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

**COMMANDS**


**list mail filters ACCOUNT**

List mail filters associated to ACCOUNT.

*Example*

.. code:: sh

    $ cpanel list mail filters scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_filters/

**get mail filter ACCOUNT FILTERNAME**

Return a JSON-formatted description of email filter FILTERNAME associated
to email ACCOUNT. To get a list of current filter names, use
‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel get mail filter scott@example.com spamkiller

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_filter/

**set mail filter ACCOUNT FILE**

Create or update an email filter associated with email ACCOUNT.
If the filter already exists, it updates it; otherwise, it creates a new filter.
Use a JSON FILE to describe the filter rules. This JSON FILE has the same
textual format as the output from ‘cpanel get mail filter’, so the easiest way
to create a new filter is to dump an existing filter into a filter.json file,
edit it and then upload it with ‘cpanel set mail filter’.
See the EXAMPLE below.

*Example*

.. code:: sh

    $ cpanel get mail filter scott@example.com spamkiller > filter.json
    $ cpanel set mail filter scott@example.com filter.json

**delete mail filter ACCOUNT FILTERNAME**

Delete email filter FILTERNAME associated to ACCOUNT. To get a list of current
filter names, use ‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel delete mail filter scott@example.com spamkiller


