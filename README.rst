gitmanager
----------

A simple way to keep track of multiple git projects.


Usage
-----

Install with `pipsi`:

    $ pipsi install gitmanager

Install with `pip`:

    $ pip install gitmanager

Add a repo:

    $ cd my-repo
    $ gim add .

Remove a repo:

    $ gim rm ~/my-repo

Check the current status (uncommitted changes, current branch) of all repos:

    $ gim status

or

    $ gim status

Run `git pull` on all repos:

    $ gim pull

Check local branches:

    $ gim branch

Check out master in all repos:

    $ gim master

Works with Python 3, untested with Python 2.x.
