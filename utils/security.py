# 做密码加密逻辑
from hashlib import md5



# ======================================= 密码加密 ========================================
def get_hash_passwd(passwd):
    # 设置sault盐
    sault = b"password"

    # 创建md5对象
    obj = md5(sault)
    
    obj.update(passwd.encode("utf-8"))
    return obj.hexdigest()




# ======================================== 密码校验 ==========================================
def auth_passwd(input_passwd, passwd):
    input_passwd = get_hash_passwd(input_passwd)
    if input_passwd == passwd:
        return True
    else:
        return False
