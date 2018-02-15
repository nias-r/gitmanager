gitmanager
----------

A simple way to keep track of multiple git projects.


Usage
-----

Install with `pipsi`:

.. code-block::
    $ pipsi install gitmanager


Install with `pip`:

.. code-block::
    $ pip install gitmanager --user

Add a repo:

.. code-block::
    $ cd my-repo
    $ gim add .

Remove a repo:

.. code-block::
    $ gim rm ~/my-repo

Check the current status (uncommitted changes, current branch) of all repos:

.. code-block::
    $ gim status

or

.. code-block::
    $ gim

Run `git pull` on all repos:

.. code-block::
    $ gim pull

Check local branches:

.. code-block::
    $ gim branch

Check out master in all repos:

.. code-block::
    $ gim master

Works with Python 3, untested with Python 2.x.
