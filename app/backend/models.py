from pydantic import BaseModel


class AnswerData(BaseModel):
    id: str
    answer: str


class QuestionData(BaseModel):
    id: str
    question: str
    answers: list[AnswerData]


class StoryData(BaseModel):
    story: str | None
    vote: int | None


class SiteInfoData(BaseModel):
    stories: list[StoryData]
    answered: list[str]
    questions: list[QuestionData]
    story: StoryData


class ItemData(BaseModel):
    id: int
    name: str
    address: str
    latlng: tuple[float, float]
    description: dict[str, str]
    significance: dict[str, str]
    suburb: str


class RouteData(BaseModel):
    stops: list[ItemData]
