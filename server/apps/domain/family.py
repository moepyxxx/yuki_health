from pydantic import BaseModel, Field

from enum import Enum
from datetime import date


class Gender(int, Enum):
    MALE = 0  # 男の子
    FEMALE = 1  # 女の子
    UNKNOWN = 2  # 不明


class Family(BaseModel):
    name: str = Field(description="名前")
    nickname: str = Field(description="ニックネーム")
    gender: Gender = Field(description="性別")
    birthday: date = Field(description="誕生日")
