from datetime import datetime
from sqlalchemy import DateTime, String, Text, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Index




class Base(DeclarativeBase):
    pass



# 产品类型分类表
class Category(Base):
    __tablename__ = "product_category"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"



# 产品总表
class Products(Base):
    __tablename__ = "products"

    # 创建索引, 提升查询速度
    __table_args__ = (
        Index("fk_news_category_index", "category_id"),
        Index("index_publish_time", "publish_time")
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="产品id")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="产品名")
    description: Mapped[str] = mapped_column(String(500), comment="产品简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="产品内容")
    image: Mapped[str] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[str] = mapped_column(String(50), comment="作者")
    category_id: Mapped[str] = mapped_column(Integer, ForeignKey('product_category.id'), nullable=False, comment="产品类型id")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"Products(id: {self.id}, title: {self.title}, views: {self.views})"