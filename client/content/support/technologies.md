---
title: Technologies
description: The technologies which this project utilises.
---

Here are some quick and minimal information about what the technologies are and how they are used.

## Frontend

You can find this under the `client/` folder.

Vue is a modern frontend framework to build user interfaces. It is very similar to React in nature,
just that I personally prefer using Vue. Nuxt is an extension on top of Vue for structure and
modularity, making the code boilerplate free.

This is a crucial part of this project, and I would say that a lot of things are not possible
without the use of Vue. As a slightly more complex website, the advantage of SPA is clear in keeping
the app fast and interactive. There is a lot of state involved on the website, especially the
dashboard. Vue keeps the UI in sync with this state stored in Vuex.

Furthermore, it also makes development easier and more delightful in this more complex project. The
level of abstraction and architectural pattern in Vue helps to accomplish this. As opposed to that,
Jinja would make this very messy and difficult, while losing all the other features such as workflow
and structure.

## Backend

The backend is written in Python and Flask. I think that further explanations on those technologies
are not necessary. There are also a bunch of Flask extensions used to make the work easier. Gunicorn
is used for production.

### Diesel

I hope that the inclusion of this tool does not bring too much confusion. It is actually a Rust
database ORM library which I really love. It also handles migrations very well and neatly, that is
why I am using it for database migrations in this project. The relevant Python libraries are
generally much more difficult to use.

## Database

There are two databases used in this project.

### PostgreSQL

This is the main relational database used for storing persistent data. It is much faster than
SQLite, and more importantly, a lot more scalable. With the load required on the database and also
concurrency from multiple workers, a client-server database is necessary. For this, PostgreSQL is
usually more go-to choice.

### Redis

This is an in-memory database for storing cache. It is also an important part to keep the backend
fast. The most crucial part is to avoid a database call for every API request for the purpose of
authentication. It also helps to reduce queries to the database

## DevOps and others

There are also some technologies involved in this section, such as Docker, Nginx, and other tools
for workflow in both frontend and backend parts. I would not mention them here since they are less
important.
