# -*- coding: utf-8 -*-

"""
legit.cli
~~~~~~~~~

This module povides the CLI interface to legit.
"""

import sys

from clint import args
from clint.eng import join as eng_join
from clint.textui import colored, indent, puts, columns

from .core import __version__
from .scm import *


def main():

    if args.get(0) in cmd_map:

        arg = args.get(0)
        args.remove(arg)

        cmd_map.get(arg).__call__(args)
        sys.exit()

    elif args.contains(('-h', '--help')):
        display_info()
        sys.exit(1)

    elif args.contains(('-v', '--version')):
        display_version()
        sys.exit(1)

    else:
        display_info()
        sys.exit(1)


def status_log(func, message, *args, **kwargs):

    print message
    log = func(*args, **kwargs)

    if log:
        out = []

        for line in log.split('\n'):
            if not line.startswith('#'):
                out.append(line)
        print colored.black('\n'.join(out))


def cmd_switch(args):

    to_branch = args.get(0)

    if not to_branch:
        display_available_branches()
        sys.exit()

    if to_branch not in get_branch_names():
        print 'Branch not found.'
        sys.exit(1)
    else:
        if repo.is_dirty:
            status_log(stash_for_switch, 'Saving local changes.')

        status_log(checkout_branch, 'Switching branch.', to_branch)
        status_log(unstash_for_switch, 'Restoring local changes.')


def cmd_sync(args):

    branch = repo.head.ref.name

    status_log(fetch, 'Fetching changes.')

    status_log(stash_for_sync, 'Saving local changes.')

    status_log(pull, 'Pulling commits from the server.', branch=branch)

    # TODO: check if branch is published.
    status_log(push, 'Pushing commits to the server.', branch=branch)

    status_log(unstash_for_sync, 'Restoring local changes.')



def display_available_branches():

    branches = get_branches()

    branch_col = len(max([b.name for b in branches], key=len)) + 1

    for branch in branches:

        marker = '*' if (branch.name == repo.head.ref.name) else ' '
        pub = '(published)' if branch.is_published else '(unpublished)'

        print columns(
            [colored.red(marker), 2],
            [colored.yellow(branch.name), branch_col],
            [colored.black(pub), 14]
        )




def display_info():

    puts('{0}. {1}\n'.format(
        colored.red('legit'),
        colored.black(u'A Kenneth Reitz Project™')
    ))
    # puts('https://github.com/kennethreitz/legit\n')
    # puts('\n')
    puts('Usage: {0}'.format(colored.blue('legit <command>')))
    puts('Commands: {0}.\n'.format(
        eng_join(
            [str(colored.green(c)) for c in sorted(cmd_map.keys())]
        )
    ))


def display_version():
    puts('{0} v{1}'.format(
        colored.yellow('legit'),
        __version__
    ))




cmd_map = dict(
    switch=cmd_switch,
    sync=cmd_sync,
    branch=cmd_switch,
    publish=cmd_switch,
    unpublish=cmd_switch
)