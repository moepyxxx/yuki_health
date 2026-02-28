from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from apps.domain import FecesColor, Wateriness, Gender
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate

prompt_file_path = Path(__file__).parent / "family_feces_analyzer_prompt.md"


class FecesAnalyzeResult(BaseModel):
    color: FecesColor | None = Field(None, description="ふんの色味")
    has_urates: bool | None = Field(description="尿酸（白い部分）の有無。")
    wateriness: Wateriness | None = Field(description="水分量")
    has_undigested_seeds: bool | None = Field(description="未消化便か否か")
    confidence: float | None = Field(description="解析の信頼度")
    impressions: str | None = Field(
        description="異常ありかどうか。異常がある場合、どのような異常があるかや注意点等を記載。全体的に判定不可能な場合も記載"
    )


class FamilyFecesAnalyzer:
    def __init__(self, google_ai_model):
        self._model = ChatGoogleGenerativeAI(
            model=google_ai_model,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
            max_retries=3,
        )
        self._prompt = prompt_file_path.read_text(encoding="utf-8")

    def invoke(
        self, image_data: str, bird_type, age_year: int, age_month: int, gender: Gender
    ):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self._prompt),
                (
                    "user",
                    [
                        {"type": "text", "text": "解析をお願いします。"},
                        {"type": "image_url", "image_url": {"url": image_data}},
                    ],
                ),
            ]
        )

        structured_model = self._model.with_structured_output(FecesAnalyzeResult)
        chain = prompt_template | structured_model
        return chain.invoke(
            {
                "bird_type": bird_type,
                "age_year": age_year,
                "age_month": age_month,
                "gender": gender.label,
                "image_url": image_data,
            }
        )
