#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy.orm import sessionmaker
from termcolor import colored, cprint
import delegator
import git
from .models import engine, Repo

COLOURS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
ON_COLOURS = ['on_{colour}'.format(colour=colour) for colour in COLOURS]
NUM_COLOURS = len(COLOURS)


class GitManager(object):
    @staticmethod
    def get_name(path):
        return os.path.basename(os.path.normpath(path)).upper()

    @staticmethod
    def get_path(directory):
        return os.path.realpath(os.path.join(os.getcwd(), directory))

    def __init__(self):
        self.db = sessionmaker(bind=engine)()

    def list_all(self):
        print '\n'.join([row.name for row in self.db.query(Repo, Repo.name)])

    def get_longest_name_length(self):
        return sorted([len(row.name) for row in self.db.query(Repo, Repo.name)])[-1]

    def register(self, dir):
        path = self.get_path(dir)
        name = self.get_name(path)
        if not os.path.exists(os.path.join(dir, '.git')):
            cprint('{path} is not a git repository!'.format(path=path), 'red')
            return
        result = self.db.query(Repo).filter(Repo.path == path).count()
        if result == 0:
            repo = Repo(name=name, path=path)
            self.db.add(repo)
            cprint('Adding {name} ({path}) to Git Manager'.format(name=name, path=path), 'green')
            self.db.commit()
        else:
            cprint('{name} ({path}) has not been added because it is already registered!'.format(name=name,
                                                                                                 path=path), 'green')

    def deregister(self, dir):
        path = self.get_path(dir)
        name = self.get_name(path)
        result = self.db.query(Repo).filter(Repo.path == path).delete()
        if result > 0:
            cprint('Removing {name} ({path}) from Git Manager'.format(name=name, path=path), 'red')
        else:
            cprint('{name} ({path}) has not been removed because it is not registered!'.format(name=name,
                                                                                               path=path), 'red')
        self.db.commit()

    def status_check(self):
        output = ['GIT STATUS']
        for index, repo in enumerate(self.db.query(Repo)):
            path = repo.path
            name = repo.name.ljust(self.get_longest_name_length() + 10)
            r = git.Repo(path)
            try:
                branch = r.active_branch.name.ljust(20)
            except Exception, e:
                print 'error in repo {0}\n{1}'.format(name, e)
                branch = 'unknown'.ljust(20)

            diffs = len(r.index.diff(None))
            text = '{cname}{cbranch}{status}'.format(
                cname=colored(
                    name,
                    color=COLOURS[index % NUM_COLOURS]
                ),

                cbranch=colored(
                    branch,
                    color=COLOURS[index % NUM_COLOURS],
                ),

                status='{pips}'.format(pips='⦿' * diffs)
            )

            output.append(text)
        print '\n'
        print '\n'.join(output)
        print '\n'

    def pull_all(self):
        procs = []
        for repo in self.db.query(Repo):
            path = repo.path
            procs.append((delegator.run('git -C {0} pull'.format(path), block=False), repo.name))
        for index, (r, name) in enumerate(procs):
            r.block()
            cprint(name, COLOURS[index % NUM_COLOURS])
            print(r.out)
        print('')

    def list_branches(self):
        procs = []
        for repo in self.db.query(Repo):
            path = repo.path
            procs.append((delegator.run('git -C {0} branch'.format(path), block=False), repo.name))
        for index, (r, name) in enumerate(procs):
            r.block()
            cprint(name, COLOURS[index % NUM_COLOURS])
            print(r.out)
        print('')
