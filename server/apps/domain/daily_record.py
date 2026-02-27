from pydantic import BaseModel


class DailyFamilyFacesImage(BaseModel):
    image_src: str
