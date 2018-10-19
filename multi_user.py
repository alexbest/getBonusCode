from pip._vendor.distlib.compat import raw_input

from bcode import Bcode
from update import check_update

if __name__ == '__main__':
    check_update()
    user = raw_input("博纳云账号: ")
    password = raw_input("博纳云密码: ")
    bcode = Bcode(user, password)
    bcode.start()
