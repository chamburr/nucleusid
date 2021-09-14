---
title: Issues
description: Potential problems in this project.
---

There are some problems involved in this project. I am mentioning them not to reduce my marks but
just for clarification and future.

## Performance

It is very inefficient that updating multiple rows would be necessary whenever there is a change in
password, and also a change in whether a folder is shared. The current state could be vulnerable to
DDoS and abuse. I should either properly rate limit this or avoid the need for updating multiple
rows somehow.


## Abuse

Rate limit is currently questionable and not well tested. There should be more logic to prevent
spamming of accounts and such by device and user account, instead of just IP address.

## User account

It is not possible to recover password currently. However, there should be an option to download a
backup code, or allow a permanent deletion of the encrypted data in the account. This is also a
problem that when people use someone else's email, the owner cannot gain access to it even if they
can prove that they are the owner.

## Authentication logic

Token refresh is not yet implemented. This means the user needs to log in again every 7 days. It
should automatically refresh instead.

The remember me functionality is not well implemented. Instead of just storing the token inside the
session storage, the token should also expire more quickly.
