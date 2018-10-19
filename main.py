import json

from bcode import Bcode
from config import *
from date_utils import *
from http_utils import *
from rk import RClient
from update import check_update

if __name__ == '__main__':
    check_update()
    bcode = Bcode(BONUS_CLOUD_USER, BONUS_CLOUD_PASSWORD)
    bcode.start()
