import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status


# 开发模式: 返回详细错误信息
# 生产模式: 返回简化错误信息
DEBUG_MODE = True  # 教学项目保持开启


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    处理 HTTPException 异常
    """
    # HTTPException 通常是业务逻辑主动抛出的, data 保持 None
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )


async def Integrity_error_handler(request: Request, exc: IntegrityError):
    """
    处理数据库完整性约束错误
    """
    error_msg = str(exc.orig)

    # 判断具体的余数错误类型
    if "user_name_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突, 请检查输入"


    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }


    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = {
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )




async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    处理 SQLAlchemy 数据库错误
    """
    # 开发者模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            # 格式化异常信息为字符串, 方便日志记录和调试
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "code": 500,
            "message": "数据库操作失败, 请稍后尝试",
            "data": error_data
        }
    )




async def general_exception_handler(request: Request, exc: Exception):
    """
    处理所有未捕获的异常
    """
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data
        }
    )




# 用一个函数封装所有异常处理
def register_exception_handlers(app):
    """
    注册全局异常处理
    """
    # 注册异常函数, 第一个参数是抛错类型, 第二个参数是具体要抛出的异常函数
    app.add_exception_handler(HTTPException, http_exception_handler)      # 业务
    app.add_exception_handler(IntegrityError, Integrity_error_handler)    # 数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # 数据库
    app.add_exception_handler(Exception, general_exception_handler)       # 兜底
