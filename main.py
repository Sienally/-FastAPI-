# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 导入路由
from routers import news, subpages, users, products

# 导入数据库配置初始化
from config.db_config import init_db

# 导入全局异常处理
from utils import exception



# 创建FastAP实例
app = FastAPI()



# 全局注册异常处理
exception.register_exception_handlers(app)



@app.get("/")  # 如果用户访问的是当前路IP下的根路径, 则执行函数root(), 返回值类型为HTML
async def root():

    await init_db()
    # 返回网页数据给用户
    with open("/home/public/Web/Project1/static/home.html", "r", encoding="utf-8")as f:
        text = f.read()
    return HTMLResponse(text)




# # dcos接口
# @app.get("/docs")
# async def warrning():
#     raise HTTPException(status_code=404, detail="什么也没找到")





# 静态资源挂载
app.mount("/static", StaticFiles(directory="/home/public/Web/Project1/static"), name="static")

# 挂载其他页面路由
app.include_router(subpages.router)

# 挂载用户路由
app.include_router(users.router)

# 挂载新闻路由
app.include_router(news.router)

# 挂载产品路由
app.include_router(products.router)






if __name__ == "__main__":
    import uvicorn
    
    # uvicorn是FastAPI的高效启动服务器, 它能托举FastAPI的运行
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)  # reload会监测代码变动, 如果变了就重启
