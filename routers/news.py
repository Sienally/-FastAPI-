from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio



# 导入模型, 会话
from crud.crud_news import get_categories
from config.db_config import get_db_session, init_db



# 创建 APIRouter 实例
# prefix是路由前缀, (API 接口规范文档)
# tags是所属组名, 在fastapi的测试链接用
router = APIRouter(prefix="/api/news", tags=["news"])  


# 该接口实现流程:
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表 (数据库设计文档)
# 3. 在 curd 文件夹里面创建文件, 封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法, 响应结果



@router.get("/catergories")
async def get_catergories(db: AsyncSession = Depends(get_db_session), skip: int = 0, limit: int = 100):
    
    # 初始化建表函数
    # await init_db()
    
    # 先填充数据库里面的新闻分类数据 ==> 先创建数据库引擎与会话 ==> 再定义模型类 ==> 封装查询数据的方法
    categories = await get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "ok",
        "data": categories
    }