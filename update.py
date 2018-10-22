from http_utils import *
import zipfile


def check_update():
    version = open('version', 'r')
    local_version = version.read()
    version.close()
    print('version' + local_version)
    print('register https://console.bonuscloud.io/signUp?refer=264a1ce0d14511e894a05731b778d621')
    print('https://bbs.bihe.one/thread-1445.htm')
    try:
        response = get('https://raw.githubusercontent.com/biheBlockChain/getBonusCode/master/version')
        remote_version = response.text
        if remote_version != local_version:
            response = get('https://raw.githubusercontent.com/biheBlockChain/getBonusCode/master/update_desc')
    except:
        print('')


if __name__ == '__main__':
    version = open('version', 'r')
    local_version = version.read()
    version.close()
    response = get('https://raw.githubusercontent.com/biheBlockChain/getBonusCode/master/version')
    remote_version = response.text
    if remote_version == local_version:
        exit(0)
    try:
        zipfile = open(remote_version + '.zip', 'r')
    except:
        download('https://github.com/biheBlockChain/getBonusCode/archive/master.zip', file_name=remote_version + '.zip')
