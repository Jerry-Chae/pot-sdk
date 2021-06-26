import requests
import pathlib
from argparse import ArgumentParser


def send_file_to_pam(argspec):
    session = requests.session()
    url = argspec.address

    bot = open(str(pathlib.Path(argspec.bot)), 'rb')
    d = {'fileName': 'Scenario.json', 'md5': '15cd10cb69213cdfcf3b3c6817fbe352'}
    endpoint = '{}:{}{}'.format(url, argspec.port, '/api/v1.0/pam')
    result = session.post(endpoint, data=d, files={'file': bot})
    if 200 != result.status_code:
        return 1

    endpoint = '{}:{}{}'.format(url, argspec.port, '/api/v1.0/pam/0/start')
    session.post(endpoint)
    if 200 != result.status_code:
        return 1
    return 0


if __name__ == '__main__':
    # proc 192.168.10.1 bot_file_path
    # proc 192.168.10.1 -p 8012 bot_file_path

    parser = ArgumentParser()
    parser.add_argument('address', type=str)
    parser.add_argument('bot', type=str, help="ARGOS-LABS BOT File path")
    parser.add_argument('-p', '--port', type=str, default="8012")
    spec = parser.parse_known_args()[0]
    send_file_to_pam(spec)
