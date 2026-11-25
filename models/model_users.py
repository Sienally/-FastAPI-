from datetime import datetime
from sqlalchemy import DateTime, String, Enum, Index, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional




class Base(DeclarativeBase):
    # 新写法, 能够在基类里写上期望在建表时添加的公共字段
    # Mapped里面映射的对象基本都是系统级数据类型
    
    # 创建日期字段:
    create_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        comment="创建时间"      
    )
    # 更新日期字段: 
    update_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )


# 账号表
class Users(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("username_UNIQUE", "user_name"),
        Index("phone_UNIQUE", "phone")
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="用户ID")
    user_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(100), nullable=False, comment="密码(加密存储)")
    
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment="头像URL", default="http://118.31.1.63/static/img/ciallo.png")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'), comment="性别", default="unknown")
    bio: Mapped[Optional[str]] = mapped_column(String(255), comment="个人简介", default="这个人很懒，什么也没留下")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment="手机号")




class UserToken(Base):
    __tablename__ = "user_token"

    __table_args__ = (
        Index("token_UNIQUE", 'token'),
        Index("fk_user_token_user_idx", "user_id")
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(Users.id), nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="令牌值")
    expires_at: Mapped[str] = mapped_column(DateTime, nullable=False, comment="过期时间")
    create_at: Mapped[str] = mapped_column(DateTime, nullable=False, default=datetime.now(), comment="创建时间")