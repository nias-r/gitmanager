#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import FlushError
from termcolor import colored, cprint
import delegator
import git
from models import engine, Repo
from multiprocessing import Process, Queue

COLOURS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
ON_COLOURS = ['on_{colour}'.format(colour=colour) for colour in COLOURS]
NUM_COLOURS = len(COLOURS)


class GitManager(object):
    def __init__(self):
        self.db = sessionmaker(bind=engine)()
        self.longest_name = max(len(repos.name) for repos in self.repos)

    @property
    def repos(self):
        return self.db.query(Repo)

    @property
    def num_repos(self):
        return self.repos.count()

    @staticmethod
    def _get_name(repo_path):
        return os.path.basename(os.path.normpath(repo_path)).upper()

    @staticmethod
    def _get_path(directory):
        return os.path.realpath(os.path.join(os.getcwd(), directory))

    @classmethod
    def _get_path_and_name(cls, p):
        return cls._get_path(p), cls._get_name(p)

    @staticmethod
    def _get_branch(repo_path):
        r = git.Repo(repo_path)
        try:
            branch = r.active_branch.name
        except ValueError:
            branch = 'unknown'

        diffs = len(r.index.diff(None))
        return branch, diffs

    @staticmethod
    def _pull_repo(repo_path):
        return delegator.run('git -C {0} pull'.format(repo_path), block=False)

    @staticmethod
    def _list_branches(repo_path):
        return delegator.run('git -C {0} branch'.format(repo_path), block=False)

    @staticmethod
    def _checkout_branch(repo_path, branch='master'):
        return delegator.run('git -C {0} checkout {1}'.format(repo_path, branch), block=False)

    @staticmethod
    def _get_results(output_queue, num_repos):
        results = []
        while True:
            string = output_queue.get()
            results.append(string)
            if len(results) == num_repos:
                break
        return sorted(results)

    def _get_repo(self, repo_path):
        return self.repos.filter(Repo.path == repo_path)

    def _add_repo(self, repo_path, name):
        repo = Repo(name=name, path=repo_path)
        self.db.add(repo)
        try:
            self.db.commit()
            self._longest_name = 0
            return True
        except FlushError:
            self.db.rollback()
            return False

    def _delete_repo(self, repo_path):
        result = self._get_repo(repo_path).delete()
        self.db.commit()
        self._longest_name = 0
        return result

    def _format_branch(self, repo, output_queue, index):
        branch, diffs = self._get_branch(repo.path)
        text = '{name}{branch}{status}'.format(name=repo.name.ljust(self.longest_name + 10),
                                               branch=branch.ljust(20),
                                               status='⦿' * diffs)
        output_queue.put(colored(text, COLOURS[index % NUM_COLOURS]))

    def _call_function(self, f, *args, **kwargs):
        processes = [(f(repo.path, *args, **kwargs), repo.name) for repo in self.repos]

        for index, (p, name) in enumerate(processes):
            p.block()
            cprint(name, COLOURS[index % NUM_COLOURS])
            print(p.out)

    def register(self, directory):
        repo_path, name = self._get_path_and_name(directory)

        if not os.path.exists(os.path.join(directory, '.git')):
            cprint('{repo_path} is not a git repository!'.format(repo_path=repo_path), 'red')
            return

        if self._add_repo(repo_path, name):
            cprint('Added {name} ({repo_path}) to Git Manager'.format(name=name, repo_path=repo_path), 'green')
        else:
            cprint(('{name} ({repo_path}) has not been added '
                    'because it is already registered!').format(name=name, repo_path=repo_path), 'green')

    def deregister(self, directory):
        repo_path, name = self._get_path_and_name(directory)

        if self._delete_repo(repo_path):
            cprint('Removed {name} ({repo_path}) from Git Manager'.format(name=name, repo_path=repo_path), 'red')
        else:
            cprint(('{name} ({repo_path}) has not been removed '
                    'because it is not registered!').format(name=name, repo_path=repo_path), 'red')

    def status_check(self):
        num_repos = self.num_repos
        output_queue = Queue()

        processes = [Process(target=self._format_branch, kwargs=dict(repo=repo, output_queue=output_queue, index=index))
                     for index, repo in enumerate(self.repos)]

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        output = self._get_results(output_queue, num_repos)
        print '\n'.join(output)

    def pull_all(self):
        self._call_function(self._pull_repo)

    def list_branches(self):
        self._call_function(self._list_branches)

    def checkout_master(self):
        self._call_function(self._checkout_branch, branch='master')
