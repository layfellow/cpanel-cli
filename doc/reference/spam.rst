..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``spam``
==================================================

`Leer en español </es/latest/reference/spam.html>`_

- **get spam settings**
- **enable spam assassin**
- **disable spam assassin**
- **enable spam box**
- **clear spam box**
- **disable spam box**
- **set spam score SCORE**
- **add spam denylist EMAIL...**
- **delete spam denylist EMAIL...**
- **add spam allowlist EMAIL...**
- **delete spam allowlist EMAIL...**
- **set spam autodelete score SCORE**
- **disable spam autodelete**
- **list spam rules**
- **set spam rule score RULE SCORE**

**COMMANDS**


**get spam settings**

List the current SpamAssassin settings for all email accounts on the server.

*Example*

.. code:: sh

    $ cpanel get spam settings

This command shows a combined output of the JSON result data from the
following two API calls:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_spam_settings/
https://api.docs.cpanel.net/openapi/cpanel/operation/get_user_preferences/

**enable spam assassin**

Enable the SpamAssassin spam filter.
Use ‘cpanel get spam settings’ to see the current SpamAssassin settings.

*Example*

.. code:: sh

    $ cpanel enable spam assassin

**disable spam assassin**

Disable the SpamAssassin spam filter.
Use ‘cpanel get spam settings’ to see the current SpamAssassin settings.

*Example*

.. code:: sh

    $ cpanel disable spam assassin

**enable spam box**

Enable the spam mail boxes for every email account on the server;
messages marked by SpamAssassin will be sent to these boxes.
Use ‘cpanel get spam settings’ to see the current SpamAssassin settings.

*Example*

.. code:: sh

    $ cpanel enable spam box

**clear spam box**

Clear the contents of the spam boxes for every email account on the server.

*Example*

.. code:: sh

    $ cpanel clear spam box

**disable spam box**

Disable the spam mail boxes for every email account on the server;
messages marked by SpamAssassin will still be flagged as such but sent
to the inboxes.
Use ‘cpanel get spam settings’ to see the current SpamAssassin settings.

*Example*

.. code:: sh

    $ cpanel disable spam box

**set spam score SCORE**

Set the required SpamAssassin SCORE for a message to be marked as spam.
SCORE is a number between 1.0 and 15.0; the higher the number,
the less likely a message will be marked as spam.
A SCORE higher than 10.0 is considered very lenient, and many spam
messages might still get through, while a SCORE lower than 3.0 is
considered aggressive and legitimate messages might be marked as spam.
You may set it to 5.0 for a good starting point.
Use ‘cpanel get spam settings’ to get the current required score.

*Example*

.. code:: sh

    $ cpanel set spam score 5.0

**add spam denylist EMAIL...**

Add one or more EMAIL addresses to the SpamAssassin deny list.
Messages from these addresses will always be marked as spam, regardless
of the content or calculated score.
Use ‘cpanel get spam settings’ to see the deny list (blacklist_from).

*Examples*

.. code:: sh

    $ cpanel add spam denylist scott@example.com
    $ cpanel add spam denylist scott@example.com root@eruditorum.org

**delete spam denylist EMAIL...**

Delete one or more EMAIL addresses from the SpamAssassin deny list.
Use ‘cpanel get spam settings’ to see the deny list (blacklist_from).
See also ‘cpanel add spam denylist’.

*Examples*

.. code:: sh

    $ cpanel delete spam denylist scott@example.com
    $ cpanel delete spam denylist scott@example.com root@eruditorum.org

**add spam allowlist EMAIL...**

Add one or more EMAIL addresses to the SpamAssassin allow list.
Messages from these addresses will always get through, regardless
of the content or calculated score.
Use ‘cpanel get spam settings’ to see the allow list (whitelist_from).

*Examples*

.. code:: sh

    $ cpanel add spam allowlist scott@example.com
    $ cpanel add spam allowlist scott@example.com root@eruditorum.org

**delete spam allowlist EMAIL...**

Delete one or more EMAIL addresses from the SpamAssassin allow list.
Use ‘cpanel get spam settings’ to see the allow list (whitelist_from).
See also ‘cpanel add spam allowlist’.

*Examples*

.. code:: sh

    $ cpanel delete spam allowlist scott@example.com
    $ cpanel delete spam allowlist scott@example.com root@eruditorum.org

**set spam autodelete score SCORE**

Set the threshold SCORE for SpamAssassin to automatically delete messages,
bypassing the spam mail boxes. SCORE is a number between 1.0 and 15.0;
the higher the number, the less likely a message will be deleted.
You should use a rather high and lenient score to avoid accidentally
deleting legitimate messages. You may set it to 10.0 for a good starting
point; or, better yet, disable it completely.
Use ‘cpanel get spam settings’ to check the current autodelete settings
(spam_auto_delete and spam_auto_delete_score).
Use ‘cpanel disable spam autodelete’ to disable autodelete.
See also ‘cpanel enable spam box’.

*Example*

.. code:: sh

    $ cpanel set spam autodelete score 10.0

**disable spam autodelete**

Disable the autodelete feature of SpamAssassin. When disabled, spam
messages marked by SpamAssassin will be sent to the spam mail boxes
instead of being automatically deleted.
Use ‘cpanel get spam settings’ to check the current autodelete settings
(spam_auto_delete and spam_auto_delete_score).

*Example*

.. code:: sh

    $ cpanel disable spam autodelete

**list spam rules**

List the rules (a.k.a. symbolic tests) and their partial scores used by
SpamAssassin to evaluate messages and calculate the aggregated spam score.
For a list of rules and their definitions, see the source code at:
https://github.com/apache/spamassassin/tree/trunk/rules
In general, you should not need to modify these rules.

*Example*

.. code:: sh

    $ cpanel list spam rules

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/get_symbolic_test_names/

**set spam rule score RULE SCORE**

Set the partial SCORE assigned to a RULE (a.k.a. a symbolic test) used
by SpamAssassin to calculate the aggregated spam score.
For a list of rules and their definitions, see the souce code at:
https://github.com/apache/spamassassin/tree/trunk/rules
To get a list of the current rules and their scores, use:
‘cpanel list spam rules’.
In general, you should not need to modify these rules.

*Example*

.. code:: sh

    $ cpanel set spam rule score MONEY_FREEMAIL 0.695


