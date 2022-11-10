# Book Manager Demo

This django application exists to test the `django-book-manager` module.

## Setting up to run the demo

The demo runs in Docker, so you will need Docker Desktop or equivalent installed
on your development machine.

### Build the Docker image

```bash
make build
```

### Run the service, and initialize the database

```bash
make dev-detached
make exec
> ./manage.py migrate
```

This will migrate all schema, and load fixtures for some users as well as ~ 1000
books and dependent models.

There are no real views defined in this Django application, but you can
investigate the data by using the `shell_plus` interactive Django shell:

```bash
make dev-detached
make exec
> ./manage.py shell_plus
```

### Getting to the demo app in your browser

You should now be able to browse to the demo app on https://localhost/ .

### Fixtures

There are two users in the system, loaded from `demo/users/fixtures/users.json`:

* `root`, a superuser, whose password is `password`
* `testy` a normal user, whose password is `testy`

The `demo/core/fixtures/books.json` that is loaded during `./manage.py migrate`
creates `book_manager.Reading` instances associated with the `testy` user.
