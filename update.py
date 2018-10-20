from http_utils import *
import zipfile


def check_update():
    version = open('version', 'r')
    local_version = version.read()
    version.close()
    print('币合区块链博纳云抢码脚本,版本号：' + local_version)
    print('使用时请同步好本地时间')
    print('使用后面的邀请地址注册，更容易成功，博纳云注册：https://console.bonuscloud.io/signUp?refer=264a1ce0d14511e894a05731b778d621')
    print('软件使用问题请查看：https://bbs.bihe.one/thread-1445.htm')
    print('更多工具请关注：币合区块链')
    print('币合官方群：490389116')
    try:
        response = get('https://raw.githubusercontent.com/biheBlockChain/getBonusCode/master/version')
        remote_version = response.text
        if remote_version != local_version:
            print('检测到新版本，请前往：https://github.com/biheBlockChain/getBonusCode 更新')
            response = get('https://raw.githubusercontent.com/biheBlockChain/getBonusCode/master/update_desc')
            print("\n----------\n更新说明：\n" + response.text + "\n\n----------\n")
    except:
        print('检查新版本失败')


if __name__ == '__main__':
    print("正在检查更新")
    version = open('version', 'r')
    local_version = version.read()
    print('当前版本：' + local_version)
    version.close()
    response = get('https://raw.githubusercontent.com/biheBlockChain/getBonusCode/master/version')
    remote_version = response.text
    print('最新版：' + remote_version)
    if remote_version == local_version:
        print('无需更新')
        exit(0)
    print('正在更新')
    try:
        zipfile = open(remote_version + '.zip', 'r')
    except:
        download('https://github.com/biheBlockChain/getBonusCode/archive/master.zip', file_name=remote_version + '.zip')
