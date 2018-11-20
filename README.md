# ckanext-ed

This is the main repo for the US Department of Education ckan-based project. This documentation covers all of the development aspects.

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Getting started](#getting-started)
  - [Requirements](#requirements)
  - [Setup environment](#setup-environment)
  - [Start development server](#start-development-server)
- [Development](#development)
  - [Running unit tests](#running-unit-tests)
  - [Running E2E tests](#running-e2e-tests)
  - [Working with static files](#working-with-static-files)
  - [Working with i18n](#working-with-i18n)
  - [Testing email notifications](#testing-email-notifications)
  - [Generating data.json](#generating-datajson)
  - [Log into the container](#log-into-the-container)
  - [Updating docker images](#updating-docker-images)
  - [Reseting docker](#reseting-docker)
  - [Generating TOC](#generating-toc)
- [Troubleshooting](#troubleshooting)
  - [The admin credentials don't work](#the-admin-credentials-dont-work)
- [References](#references)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Getting started

### Requirements

Please follow installation instructions of the software below if needed. The following steps require:
- `docker`
- `docker-compose`
- `nvm/Node.js` (optional)
- `/etc/hosts` contains the `127.0.0.1 ckan-dev` line

### Setup environment

Clone the `docker-ckan-ed` repository (assuming that we're inside our `projects` directory):

```bash
$ git clone git@github.com:CivicActions/docker-ckan-ed.git
$ cd docker-ckan-ed
```

This is a docker compose setup for local development. It's designed to support live development of extensions which are stored inside the `src` directory.

Clone the `ckanext-ed` repository to the `src` folder (we also can create a symbolic link back to the `projects` directory):

```bash
$ cd src
$ git clone git@github.com:CivicActions/ckanext-ed.git
$ cd ckanext-ed
```

Now we have cloned all the required repositories and we're located in our main working directory `docker-ckan-ed/src/ckanext-ed`

For running commands and building static files, we can use `npm`. Let's enable a Node.js environment:

> You have to have `nvm` installed or you can use any other way to get Node.js prepared - system setup etc

```bash
$ nvm install 10
$ nvm use 10
$ npm install
```

### Start development server

> Take a look inside `package.json` to understand what's going on under the hood. Or if you don't have Node.js installed.

To start a development server, we have to build docker images:

```bash
$ npm run docker:build
```

Let's start the development server:

> For live development the first option is recommended to be launched in another terminal window

```bash
$ npm run docker:up # Option 1: to see logs at the same window
$ npm run docker:up -- -d # Option 2: to start as a deamon; requires understanding how to manage a docker container
```

You can work on the `ckanext-ed` codebase having it running. On every change to the codebase, the server will be reloaded automatically. It's important to mention that the ckan configuration and other things like `cron/patches/etc` are managed inside the `docker-ckan-ed` repo. If you want to update it you have to restart the server.

Now we can visit our local ckan instance at:

```
http://ckan-dev:5000/
```

To log in as an admin:
- user: `ckan_admin`
- pass: `test1234`

## Development

### Running unit tests

We write and store unit tests inside the `ckanext/ed/tests` directory. See CKAN documentation for more information regarding how to write tests. To run unit tests we have to stop development server and start testing server:

```bash
$ npm run docker:up
# It's running so we use CTRL-C to stop
$ npm run docker:up:test
```

In another terminal window run the test command:

```bash
$ npm run test:unit
```

### Running E2E tests

We write and store acceptance E2E tests inside the top-level `tests` directory. For running it we also have to switch to the test server:

```bash
$ npm run docker:up
# It's running so we use CTRL-C to stop
$ npm run docker:up:test
```

In another terminal window run the test command:

```bash
$ npm install nightwatch --no-save # Install test runner
$ npm run test:e2e
```

See the `how to write E2E tests` guide:
- http://nightwatchjs.org/guide

### Working with static files

Put your scripts/fonts/etc inside the `ckanext/ed/fanstatic` folder and images inside the `ckanext/ed/public` folder. It can be used as usual ckan `fanstatic` and `public` contents.

At the same time, we use CSS preprocessor (LESS) to build our styles. Put your styles inside the `ckanext/ed/less` and build it:

```bash
$ npm run static:build # Option 1: one-time build
$ npm run static:watch # Option 2: build on every change
```

Processed styles will be put to the `ckanext/ed/fanstatic/css` folder.

### Working with i18n

To extract i18n messages and compile the catalog we have to have our development server running.

In another terminal window run these commands:

```
$ npm run i18n:extract
$ npm run i18n:compile
```

See CKAN documentation for more on i18n management.

### Testing email notifications

We use a fake SMTP server to test email notifications:

- log into https://mailtrap.io/inboxes
- select `Demo Inbox`
- copy SMTP credentials
- past to `docker-ckan-ed:.env` (mail service connection section)
- restart the development server

Now all email sent by `from ckan.lib.mailer import mail_user` should be sent to the `Demo Inbox` at Mailtrap.

### Generating data.json

See the "Open Data" reference:
https://project-open-data.cio.gov/v1.1/schema/

See the metadata analysis regarding the project:
https://docs.google.com/spreadsheets/d/1ZPRXxKCMST-z5Exvvuf0MxDVjE2l-4jC1oKWOnpDz9M/edit#gid=44728761

We generate `data.json` using our fork of `ckanext-datajson` at https://github.com/okfn/ckanext-datajson/tree/ed (the `ed` branch).

To update the translation map (`package -> data.json`) edit `export_map/export.map.json`. It uses a self-explanatory structure. Our focus is mostly on `field` and `extra` fields. We use `ckanext-scheming` so `extra` should be `false` for all relevant fields.

### Log into the container

To issue commands inside a running container (after `$ npm run docker:up`):

```
$ npm run docker:bash
```

Now you can tweak the running `ckan-dev` docker container from inside. Please take into account that all changes will be lost after the next container restart.

### Updating docker images

Sometimes we need to update the base docker images `ckan/ckan-dev`. We can do it using:

```bash
$ npm run docker:pull
$ npm run docker:build
```

### Reseting docker

If you want to start everything from scratch there is a way to prune your docker environment:

> It will destroy all your projects inside docker!!!

```
$ docker system prune -a --volumes
```

### Generating TOC

To update this readme table of contents run:

```bash
$ npm run toc
```

## Troubleshooting

### The admin credentials don't work

There had been a bug in `ckan-dev` that was fixed. Run the following commands to update your ckan image:

```bash
$ npm run docker:pull
$ npm run docker:build
```

## References

- CKAN Documentation - https://docs.ckan.org/en/2.8/
- Deploying staging/production - see the corresponding documentation on GitLab
