from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str="success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    # 目标: 把任何的 FastAPI、Pydantic、ORM 对象 都要正常响应 ==> code、message、data
    # jsonable_encoder() 能把里面的字典内容中不可操作的对象 强制转换成可序列化的对象如dict、list、str
    # JSONResponse() 能把里面的内容包装成json格式的字符串, 通常情况下我们直接return, FastAPI会自动调用这个函数
    return JSONResponse(content=jsonable_encoder(content))