"""先准备好两个依赖包: pip install sqlalchemy[asyncio] aiomysql"""

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from models import news, users, product



# 创建异步引擎
async_engine = create_async_engine(
    "mysql+aiomysql://root:123456@localhost/project1",
    pool_size = 50,  # 设置连接池中保持的持久连接数
    max_overflow = 20  # 设置连接池允许创建的额外链接数
)


"""------------------建表逻辑------------------"""
async def init_db():
    async with async_engine.begin()as conn:
        await conn.run_sync(news.Base.metadata.create_all)      # news表创建
        await conn.run_sync(users.Base.metadata.create_all)     # account表创建
        await conn.run_sync(product.Base.metadata.create_all)   # product表创建



"""-----------------创建会话逻辑--------------------"""
# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,  # 告诉它你现在是异步类型的session
    expire_on_commit=False
)


# 依赖项, 用于获取数据库会话
async def get_db_session():
    async with AsyncSessionLocal()as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        