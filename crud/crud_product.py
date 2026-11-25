from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.model_product import Category, Products







# ===================================== 查询产品分类表 ============================================
async def product_get_categories(db: AsyncSession):
    query = select(Category)
    result = await db.execute(query)
    return result.mappings().all()







# ==================================== 按分类查询产品列表 =====================================
async def product_get_products(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 查询的是指定分类下的所有产品
    query = select(Products).where(Products.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.mappings().all()

# 查询指定分类下的产品总数量
async def product_get_count(db: AsyncSession, category_id: int):
    query = select(func.count(Products.id)).where(Products.category_id == category_id)
    result = await db.execute(query)
    return result.scalar_one()





# ======================================= 查询产品详情 ===============================================
async def product_get_detail(db: AsyncSession, product_id: int = 1):
    query = select(Products).where(Products.id == product_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 浏览量+1
async def increase_products_views(db: AsyncSession, product_id: int = 1):
    stmt = update(Products).where(Products.id == product_id).values(views = Products.views+1)
    await db.execute(stmt)





# =================================== 产品推荐 =======================================
async def get_related_products(db: AsyncSession, product_id: int, category_id: int, limit: int = 5):
    # order_by 排序 ==> 按浏览量和发布时间
    stmt = select(Products).where(
        Products.category_id == category_id,
        Products.id != product_id
    ).order_by(
        Products.views.desc(),  # desc降序, 浏览量最高的排第一
        Products.publish_time.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    return result.scalars().all()