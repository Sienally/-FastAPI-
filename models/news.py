from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



# Base基类的老写法
# Base = declarative_base()

# Base基类的新写法
class Base(DeclarativeBase):
    # 新写法, 能够在基类里写上期望在建表时添加的公共字段
    # Mapped里面映射的对象基本都是Python标准数据类型
    
    # 创建日期 - 字段:
    create_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        comment="创建时间"      
    )
    # 更新日期 - 字段: 
    update_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )
    


# 分类表
class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort: Mapped[int] = mapped_column(default=0, nullable=False, comment="排名")
    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, sort: {self.sort}"
