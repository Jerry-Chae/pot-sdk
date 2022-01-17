import os
import venv
import datetime
from pathlib import Path


def make_venv():
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    venv_d = os.path.join(str(Path.home()), '.argos-rpa.venv', now)
    venv.create(venv_d, with_pip)


if __name__ == '__main__':
    make_venv()
