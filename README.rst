gitmanager
----------

A simple way to keep track of multiple git projects.


Usage
-----

Install with `pipsi`:

.. code-block:: bash
    $ pipsi install gitmanager


Install with `pip`:

.. code-block:: bash
    $ pip install gitmanager --user

Add a repo:

.. code-block:: bash
    $ cd my-repo
    $ gim add .

Remove a repo:

.. code-block:: bash
    $ gim rm ~/my-repo

Check the current status (uncommitted changes, current branch) of all repos:

.. code-block:: bash
    $ gim status

or

.. code-block:: bash
    $ gim

Run `git pull` on all repos:

.. code-block:: bash
    $ gim pull

Check local branches:

.. code-block:: bash
    $ gim branch

Check out master in all repos:

.. code-block:: bash
    $ gim master

Works with Python 3, untested with Python 2.x.
