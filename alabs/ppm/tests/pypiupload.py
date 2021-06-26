# noinspection PyPackageRequirements
import urllib3
from alabs.ppm.pypiuploader.commands import main as pu_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def do_test(url, user, passwd, wheel):
    cmd = [
        'files',
        '--index-url',
        url,
        '--username', user,
        '--password', passwd,
        wheel,
    ]
    return pu_main(argv=cmd)


if __name__ == '__main__':
    kwargs = {
        'url': 'https://pypi-test.argos-labs.com/simple',
        'user': 'argos',
        'passwd': 'argos_01',
        'wheel': 'W:/crpa/src/alabs-common/dist/alabs.ppm-1.523.1818-py3-none-any.whl',
    }
    do_test(**kwargs)
