
import hashlib
def get_ww_idx(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    uuid = m2.hexdigest()
    return uuid


if __name__ == '__main__':
    print(get_ww_idx('WH0468'+'WL01A-01-01'+'1000-A00061'))
