# ckanext-ed

This is the main repo for the US Deparment of Education ckan-based project. This documentation covers all of the development aspects.

## Getting started

### Requirements

Please follow installation instructions of the software below if needed. The following steps require:
- `docker`
- `docker-compose`
- `nvm/Node.js` (optional)
- `/etc/hosts` contains `127.0.0.1 ckan-dev` line

### Setup environment

Clone the `docker-ckan-ed` repository (assuming that we're inside our projects directory):

```bash
$ git clone git@github.com:CivicActions/docker-ckan-ed.git
$ cd docker-ckan-ed
```

This is a docker compose setup for local development. It's designed to support live extensions development which are stored inside the `src` directory.

Clone the `ckanext-ed` repository to the `src` folder (we also can create a symbolic link to our projects directory for the `ckanext-ed` directory):

```bash
$ cd src
$ git clone git@github.com:CivicActions/ckanext-ed.git
$ cd ckanext-ed
```

Now we have cloned all the required repositories and we're located in our main working directory `docker-ckan-ed/src/ckanext-ed`

For running managing commands and building static files we can use `npm`. Let's enable a Node.js environment:

> You have to have `nvm` installed or you can use any other way to get Node.js prepared - system setup etc

```bash
$ nvm install 10
$ nvm user 10
$ npm install
```

### Start development server

> Take a look inside `package.json` to understand what's going on under the hood. Or if you don't have Node.js installed.

To start a development server we have to build docker images:

```bash
$ npm run docker:build
```

Let's start the development server:

> For live development the first option is recommended to be started in another terminal window

```bash
$ npm run docker:up # Option 1: to see logs at the same window
$ npm run docker:up -- -d # Option 2: to start as a deamon; requires understanding how to manage a docker container
```

You can work on the `ckanext-ed` codebase having it running. On every change to the codebase the server will be reloaded automatically. It's important to mention that the ckan configuration and other things like cron/patches/etc are manages inside the `docker-ckan-ed` repo. If you want to update it you have to restart the server.

Now we can visit our local ckan instance at:

```
http://ckan-dev:5000/
```

To login as an admin:
- user: `ckan_admin`
- pass: `test1234`

## Development

### Running unit tests

We write and store unit tests inside the `ckanext-ed/tests` directory. See CKAN documentation for more information regarding how to write tests. To run unit tests we have to stop development server:

```bash
$ npm run docker:up
# It's running so we use CTRL-C to stop
```

Then we need to start testing server:

```bash
$ npm run docker:up:test
```

In another terminal window run the test command:

```bash
$ npm run test:unit
```

### Running user tests

### Working with static files

Put your scripts/fonts/etc inside the `ckanext/ed/fanstatic` folder and images inside the `ckanext/ed/public` folder. It can be used as usual ckan `fanstatic` and `public` contents.

At the same time we use CSS preprocessor (SCSS) to build our styles. Put your styles inside the `ckanext/ed/scss` and build it:

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

### Log into container

To issue commands inside a running container (after `$ npm run docker:up`):

```
$ npm run docker:bash
```

### Updating docker images

Sometimes we need to update the base docker images `ckan/ckan-dev`. We can do it using:

```bash
$ npm run docker:pull
$ npm run docker:build
```

### Reseting docker

If you want to start everytning from scratch there is a way to prune your docker environment:

> It will destroy all your projects inside docker!!!

```
$ docker system prune -a --volumes
```

## References

- CKAN Documentation - https://docs.ckan.org/en/2.8/
