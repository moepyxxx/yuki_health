from pydantic import BaseModel, Field, computed_field

from enum import Enum
from datetime import date


class Gender(int, Enum):
    MALE = 0
    FEMALE = 1
    UNKNOWN = 2

    @property
    def label(self) -> str:
        mapping = {
            Gender.MALE: "男の子",
            Gender.FEMALE: "女の子",
            Gender.UNKNOWN: "不明",
        }
        return mapping.get(self, "不明")


class BirdType(int, Enum):
    OKAME_INKO = 0
    SEKISEI_INKO = 1

    @property
    def label(self) -> str:
        mapping = {
            BirdType.OKAME_INKO: "オカメインコ",
            BirdType.SEKISEI_INKO: "セキセイインコ",
        }
        return mapping.get(self, "不明")


class Family(BaseModel):
    name: str = Field(description="名前")
    nickname: str = Field(description="ニックネーム")
    gender: Gender = Field(description="性別")
    birthday: date = Field(description="誕生日")
    bird_type: BirdType = Field(description="種類")

    @computed_field
    @property
    def age_year(self) -> int:
        today = date.today()
        return (
            today.year
            - self.birthday.year
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )

    @computed_field
    @property
    def age_month(self) -> int:
        today = date.today()
        return (today.month - self.birthday.month) % 12
