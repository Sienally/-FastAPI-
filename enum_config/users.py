from enum import Enum


# 性别参数的枚举规范
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"