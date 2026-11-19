from fastapi import APIRouter
from fastapi.responses import HTMLResponse



router = APIRouter(prefix="/api/subpages", tags=["subpages"])



# 搜索接口
@router.get("/search")
async def get_search(kw):
    with open("/home/public/Web/Project1/static/subpages/search.html", "r", encoding="utf-8")as f:
        data = f.read()
    return HTMLResponse(data)



# 设置接口
@router.get("/setting")
async def get_setting():
    with open("/home/public/Web/Project1/static/subpages/setting.html", "r", encoding="utf-8")as f:
        return HTMLResponse(f.read())