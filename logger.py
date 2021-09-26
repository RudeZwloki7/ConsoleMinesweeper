import os
import sys
import uuid

from logic import repo_root

filename = str(uuid.uuid4())


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.filename = os.path.join(repo_root, '.saves', f'{filename}.txt')

    def write(self, message):
        self.terminal.write(message)

        with open(self.filename, 'a') as f:
            f.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass
