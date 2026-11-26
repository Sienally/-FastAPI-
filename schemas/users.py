from pydantic import BaseModel, Field, ConfigDict
from enum_config import users
from typing import Optional


# 定义参数结构类
class UserRequest(BaseModel):
    token: str | None = None
    user_name: str | None = Field(None, min_length=2, max_length=20, alias="userName")
    passwd: str | None = Field(None, min_length=6, max_length=20)
    avatar: str | None = "http://118.31.1.63/static/img/ciallo.png"
    gender: users.GenderEnum = users.GenderEnum.unknown
    bio: str | None = Field("这个人很懒, 什么也没留下", min_length=1, max_length=255)
    phone: str | None = None
    key: str | None = None





# user_info 对应的类: 基础类 + Info类(id、用户名)
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes = True    # 允许从 ORM 对象属性中取值
    )





# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name = True,  # alias | 字段名 兼容
        from_attributes = True    # 允许从 ORM 对象属性中取值
    )
    
    









# 查询所有token参数模型类
class selectTokensRequest(BaseModel):
    key: str





# 更改用户参数模型类
class UserUpdateInfoRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=20, alias="userName")
    avatar: str = None
    gender: users.GenderEnum = users.GenderEnum.unknown
    bio: str | None = Field("这个人很懒, 什么也没留下", min_length=1, max_length=255)
    phone: str | None = None
    
    
    
    
# 更改用户密码参数模型类
class UserUpdatePasswordRequest(BaseModel):
    password: str = Field(..., min_length=6, max_length=20, alias="passwd")
    new_passwd: str = Field(..., min_length=6, max_length=20, alias="newPasswd")