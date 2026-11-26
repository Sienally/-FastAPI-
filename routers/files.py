from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from typing import List


router = APIRouter(prefix="/api/files", tags=["文件下载"])




# Kettle
@router.get("/download/Kettle")
async def get_file_Kettle():
    return FileResponse(
        path = "./database/Kettle/pdi-ce-9.3.0.0-428.zip",  # 文件存放的真实地址
        filename = "Kettle-for-Windows.zip",      # 浏览器弹出下载框时显示的文件名
        media_type = "application/pdf",    # 内容类型, 不写会自动猜测
        content_disposition_type = "attachment"
        # attachment=下载弹窗;  inline=浏览器直接打开(图片/pdf预览)
    )
    
      
      
      
# sqlite3
@router.get("/download/sqlite3")
async def get_file_sqlite3():
    return FileResponse(
            path = "./database/sqlite3/sqlite-tools-win-x64-3500400.zip",  
            filename = "sqlite3-tools-for-Windows.zip",      
            media_type = "application/pdf",    
            content_disposition_type = "attachment"
        )
    
    
    
    
    
    
    
    
    
    
    
    
# 上传任何东西
@router.post("/uploads")
async def upload_files(files: List[UploadFile]):
    for f in files:
        with open(f"./database/any/{f.filename}", "wb")as fp:
            fp.write(await f.read())
    return {
        "code": 200,
        "count": len(files)
    }