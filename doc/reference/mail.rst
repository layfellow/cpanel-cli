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



``incoming``
==================================================

- **suspend mail incoming ACCOUNT**
- **unsuspend mail incoming ACCOUNT**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

**COMMANDS**


**suspend mail incoming ACCOUNT**

Suspend incoming mail for ACCOUNT, so that no new mail is accepted.
The user will still be able to log in to the ACCOUNT.
See also ‘cpanel unsuspend mail incoming’.

*Example*

.. code:: sh

    $ cpanel suspend mail incoming scott@example.com

**unsuspend mail incoming ACCOUNT**

Reenable incoming mail for ACCOUNT, so that new mails are accepted.

*Example*

.. code:: sh

    $ cpanel unsuspend mail incoming scott@example.com



``outgoing``
==================================================

- **suspend mail outgoing ACCOUNT**
- **unsuspend mail outgoing ACCOUNT**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

**COMMANDS**


**suspend mail outgoing ACCOUNT**

Suspend outgoing (SMTP) mail for ACCOUNT, so that no mail can be sent.
The user will still be able to log in to the ACCOUNT.
See also ‘cpanel unsuspend mail outgoing’.

*Example*

.. code:: sh

    $ cpanel suspend mail outgoing scott@example.com

**unsuspend mail outgoing ACCOUNT**

Reenable outgoing (SMTP)  mail for ACCOUNT, so that mails can be sent.

*Example*

.. code:: sh

    $ cpanel unsuspend mail outgoing scott@example.com



``login``
==================================================

- **suspend mail login ACCOUNT**
- **unsuspend mail login ACCOUNT**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Use ‘cpanel list mail accounts’ to get a list of valid ACCOUNTS.

**COMMANDS**


**suspend mail login ACCOUNT**

Suspend ACCOUNT, so that the user cannot log in.
Note that the account is not deleted, so that new mail will still
be received and stored in it.
See also ‘cpanel unsuspend mail login’.

*Example*

.. code:: sh

    $ cpanel suspend mail login scott@example.com

**unsuspend mail login ACCOUNT**

Reenable ACCOUNT, so that the user can log in again.

*Example*

.. code:: sh

    $ cpanel unsuspend mail login scott@example.com



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

    $ cpanel count mail autoresponders

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/count_auto_responders/

**get mail autoresponder ACCOUNT**

Retrieve autoresponder information corresponding to ACCOUNT.

*Example*

.. code:: sh

    $ cpanel get mail autoresponder scott@example.com

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



``forwarders``
==================================================

- **list mail forwarders [DOMAIN]**
- **add mail forwarder DOMAIN FORWARDHERE**
- **add mail forwarder EMAIL FORWARDHERE**
- **count mail forwarders**
- **delete mail forwarder DOMAIN**
- **delete mail forwarder EMAIL**

**COMMANDS**


**list mail forwarders [DOMAIN]**

List all current mail forwarders. If optional argument DOMAIN is passed, list only
the forwarders for DOMAIN.

*Examples*

.. code:: sh

    $ cpanel list mail forwarders
    $ cpanel list mail forwarders example.com

See a sample of the JSON result for all forwarders data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_forwarders/

See a sample of the JSON result for DOMAIN forwarders data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_domain_forwarders/

**add mail forwarder DOMAIN FORWARDHERE**

Forward all email sent to all accounts in DOMAIN to FORWARDHERE domain.

*Example*

.. code:: sh

    $ cpanel add mail forwarder example.com forwarded.com

**add mail forwarder EMAIL FORWARDHERE**

Forward all mail sent to EMAIL address to FORWARDHERE email address.

*Example*

.. code:: sh

    $ cpanel add mail forwarder scott@example.com larry@example.com

**count mail forwarders**

Return the total number of mail forwarders for all accounts.

*Example*

.. code:: sh

    $ cpanel count mail forwarders

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/count_forwarders/

**delete mail forwarder DOMAIN**

Delete email forwarder for DOMAIN.

*Example*

.. code:: sh

    $ cpanel delete mail forwarder example.com

**delete mail forwarder EMAIL**

Delete email forwarder for EMAIL address.

*Example*

.. code:: sh

    $ cpanel delete mail forwarder scott@example.com



``filters``
==================================================

- **list mail filters ACCOUNT**
- **count mail filters**
- **get mail filter ACCOUNT FILTERNAME**
- **set mail filter ACCOUNT FILE**
- **enable mail filter ACCOUNT FILTERNAME**
- **disable mail filter ACCOUNT FILTERNAME**
- **delete mail filter ACCOUNT FILTERNAME**
- **move mail filter ACCOUNT FILTERNAME up|down [N]**
- **move mail filter ACCOUNT FILTERNAME top|bottom**
- **move mail filter ACCOUNT FILTERNAME N**
- **trace mail filter ACCOUNT TESTMESSAGE**
- **list filter domains**

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

**count mail filters**

Return the total number of mail filters for all accounts.

*Example*

.. code:: sh

    $ cpanel count mail filters

**get mail filter ACCOUNT FILTERNAME**

Return a JSON-formatted description of email filter FILTERNAME associated
to email ACCOUNT. To get a list of filters, use
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

**enable mail filter ACCOUNT FILTERNAME**

Enable FILTERNAME associated to ACCOUNT. To get a list of filters, use
‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel enable mail filter scott@example.com spamkiller

**disable mail filter ACCOUNT FILTERNAME**

Disable FILTERNAME associated to ACCOUNT. To get a list of filters, use
‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel disable mail filter scott@example.com spamkiller

**delete mail filter ACCOUNT FILTERNAME**

Delete the email filter FILTERNAME associated to ACCOUNT. To get a list of filters,
use ‘cpanel list mail filters ACCOUNT’

*Example*

.. code:: sh

    $ cpanel delete mail filter scott@example.com spamkiller

**move mail filter ACCOUNT FILTERNAME up|down [N]**

Move the email filter FILTERNAME associated to ACCOUNT up or down the filter list.
(Filters are executed in order from top to bottom.)
To get a list of filters, use ‘cpanel list mail filters ACCOUNT’.
If N is specified, move the filter N positions up or down.

*Examples*

.. code:: sh

    $ cpanel move mail filter scott@example.com spamkiller up
    $ cpanel move mail filter scott@example.com spamkiller down
    $ cpanel move mail filter scott@example.com spamkiller up 5
    $ cpanel move mail filter scott@example.com spamkiller down 5

**move mail filter ACCOUNT FILTERNAME top|bottom**

Move the email filter FILTERNAME associated to ACCOUNT to the top or bottom
position on the filter list.
(Filters are executed in order from top to bottom.)
To get a list of filters, use ‘cpanel list mail filters ACCOUNT’

*Examples*

.. code:: sh

    $ cpanel move mail filter scott@example.com spamkiller top
    $ cpanel move mail filter scott@example.com spamkiller bottom

**move mail filter ACCOUNT FILTERNAME N**

Move the email filter FILTERNAME associated to ACCOUNT to the N-th position on the
filter list.
(Filters are executed in order from top to bottom.)
To get a list of filters, use ‘cpanel list mail filters ACCOUNT’

*Examples*

.. code:: sh

    $ cpanel move mail filter scott@example.com spamkiller 2
    $ cpanel move mail filter scott@example.com spamkiller 4

**trace mail filter ACCOUNT TESTMESSAGE**

Run a TESTMESSAGE email body against all filters and report what filters
would be triggered. This command is useful to test the effect of a new filter.
(Filters are executed in order from top to bottom.)
To get a list of filters, use ‘cpanel list mail filters ACCOUNT’
This command does not output JSON, but a trace run.

*Example*

.. code:: sh

    $ cpanel trace mail filter scott@example.com "Spam and eggs!"

**list filter domains**

List all the domains with email filters.

*Example*

.. code:: sh

    $ cpanel list filter domains

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/list_filters_backups/



``quota``
==================================================

- **get mail quota ACCOUNT**
- **set mail quota ACCOUNT QUOTA**
- **get mail quota default**
- **get mail quota max**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

**COMMANDS**


**get mail quota ACCOUNT**

Return the email quota in megabytes allocated to ACCOUNT,
or "unlimited" if there’s no quota.

*Example*

.. code:: sh

    $ cpanel get mail quota scott@example.com

**set mail quota ACCOUNT QUOTA**

Set the email QUOTA in megabytes allocated to ACCOUNT;
use ‘0’ or ‘unlimited’ to set an unlimited quota.

*Examples*

.. code:: sh

    $ cpanel set mail quota scott@example.com 1024
    $ cpanel set mail quota scott@example.com 0
    $ cpanel set mail quota scott@example.com unlimited

**get mail quota max**

Return the maximum email quota in megabytes allowed in cPanel.

*Example*

.. code:: sh

    $ cpanel get mail quota max

**get mail quota default**

Return the default email quota in megabytes allocated in cPanel.

*Example*

.. code:: sh

    $ cpanel get mail quota default



``usage``
==================================================

- **get mail usage ACCOUNT**

ACCOUNT is the name of a cPanel email account, usually in the
form user@domain.com

Return the disk space in megabytes used by ACCOUNT.

*Example*

.. code:: sh

    $ cpanel get mail usage scott@example.com

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_disk_usage/


