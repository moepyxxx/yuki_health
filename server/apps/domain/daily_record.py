from pydantic import BaseModel
from enum import Enum


class FecesColor(int, Enum):
    DEEP_GREEN = 0  # 正常な緑
    FRESH_GREEN = 1  # 鮮やかな緑（野菜摂取後、絶食等の可能性あり）
    BROWN = 2  # ペレット食の子に多い

    YELLOW = 3  # 黄色（肝機能低下の疑い）
    BRIGHT_YELLOW = 4  # 鮮やかな黄色（重度の肝疾患や感染症）
    LIME_GREEN = 5  # 蛍光緑（クラミジア感染症などの疑い）

    RED = 6  # 赤（下部消化管の出血、誤飲）
    BLACK = 7  # 黒（上部消化管の出血 / タール便）
    WHITE_ONLY = 8  # 白のみ（絶食状態、重度の消化不良）

    OTHER = 9  # その他


class Wateriness(int, Enum):
    FIRM = 1  # 正常。形がしっかりしていて、周囲の尿も少ない
    SLIGHTLY_LOOSE = 2  # やや緩い。形はあるが、尿の水分が少し多い
    POLYURIA = 3  # 多尿（Polyuria）。糞は正常だが、周囲の尿の水分が非常に多い
    DIARRHEA = 4  # 下痢（Diarrhea）。糞の形が崩れていて、全体がドロドロしている
    WATERY = 5  # 水様下痢。固形物がほぼなく、水だけ、または粘液のみ


class DailyFamilyFecesImage(BaseModel):
    image_src: str
    image_data: str
    color: FecesColor | None = None
    has_urates: bool | None = None
    wateriness: Wateriness | None = None
    has_undigested_seeds: bool | None = None
    confidence: float | None = None
    impressions: str | None = None
