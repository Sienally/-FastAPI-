from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category


# 因为要对具体的数据库操作, 那就需要传入该数据库的会话session, 第一个形参就是, 规范类型是AsyncSession
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # offset: 从第一条数据开始数, 跳过第skip个数据后才开始统计
    # limit: 限制数据查询数量
    # 等价SQL语句: select * from category offset `skip` limit `limit`;
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    
    # scalars()是对结果去壳, 反正以后用execute()的时候最好用它, 直接得到列表
    return result.scalars().all()
    