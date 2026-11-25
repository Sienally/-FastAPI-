from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio



# 导入模型, 会话
from crud import crud_product
from config.db_config import get_db_session, init_db





router = APIRouter(prefix="/api/products", tags=["products"])


# =============================== 查询产品分类 ====================================
@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db_session)):
    data = await crud_product.product_get_categories(db)

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }




# ================================ 查询产品列表 =====================================
@router.get("/list")
async def get_product_list(
    categoryId: int = 1,
    page: int = 1,
    pageSize: int = 9,
    db: AsyncSession = Depends(get_db_session)
):

    # 思路: 处理分页规则 => 查询产品列表 => 计算重量 => 计算是否还有更多
    offset = (page - 1) * pageSize
    data = await crud_product.product_get_products(db, categoryId, offset, pageSize)
    total = await crud_product.product_get_count(db, categoryId)
    # (跳过的 + 当前列表里面的数量) < 总量
    hasMore = (offset + len(data)) < total
    return {
        "code": 200,
        "message": "ok",
        "data": {
            "list": data,
            "total": total,
            "hasMore": hasMore
        }
    }




# ================================== 查询产品详情 ======================================
@router.get("/detail")
async def get_product_detail(
    productId: int = 1,
    db: AsyncSession = Depends(get_db_session)
):
    product_detail = await crud_product.product_get_detail(db, productId)
    # 如果该产品不存在
    if not product_detail:
        raise HTTPException(status_code=404, detail="产品不存在")

    # 如果存在, 则浏览量+1
    await crud_product.increase_products_views(db, productId)

    # 推荐其它产品
    related_products = await crud_product.get_related_products(db, product_detail.id, product_detail.category_id)

    return {
        "code": 200,
        "id": product_detail.id,
        "title": product_detail.title,
        "description": product_detail.description,
        "content": product_detail.content,
        "image": product_detail.image,
        "author": product_detail.author,
        "categoryId": product_detail.category_id,
        "views": product_detail.views,
        "publishTime": product_detail.publish_time,
        "relatedProducts": [{
            "id": product.id,
            "title": product.title,
            "content": product.content,
            "image": product.image,
            "author": product.author,
            "publishTime": product.publish_time,
            "categoryId": product.category_id,
            "views": product.views
        } for product in related_products]
    }

