#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy.orm import sessionmaker
from termcolor import colored, cprint
import envoy
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
            name = repo.name.ljust(20)
            r = git.Repo(path)
            try:
                branch = r.active_branch.name.ljust(20)
            except Exception, e:
                print 'error in repo {0}\n{1}'.format(name, e)
                branch = 'unknown'.ljust(20)

            diffs = len(r.index.diff(None))
            text = '{cname}{arrow_one}{cbranch}{arrow_two}{status}'.format(
                cname=colored(
                    name,
                    color='grey',
                    on_color=ON_COLOURS[index % NUM_COLOURS]
                ),

                arrow_one=colored(
                    ' ',
                    color=COLOURS[index % NUM_COLOURS],
                    on_color=ON_COLOURS[(index + 1) % NUM_COLOURS]),

                cbranch=colored(
                    branch,
                    color='grey',
                    on_color=ON_COLOURS[(index + 1) % NUM_COLOURS]),

                arrow_two=colored(
                    ' ',
                    color=COLOURS[(index + 1) % NUM_COLOURS]),

                status='{pips}'.format(pips='⦿' * diffs)
            )

            output.append(text)
        print '\n'
        print '\n'.join(output)
        print '\n'

    def pull_all(self):
        for index, repo in enumerate(self.db.query(Repo)):
            path = repo.path
            name = repo.name
            r = envoy.run('git -C {0} pull'.format(path))
            cprint(name, COLOURS[index % NUM_COLOURS])
            print(r.std_out)
        print('')

    def list_branches(self):
        for index, repo in enumerate(self.db.query(Repo)):
            path = repo.path
            name = repo.name
            r = envoy.run('git -C {0} branch'.format(path))
            cprint(name, COLOURS[index % NUM_COLOURS])
            print(r.std_out)
        print('')
