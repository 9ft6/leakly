import json

from pydantic import BaseModel


class Cannabinoid(BaseModel):
    displayName: str
    order: int
    percentile25: float | None
    percentile50: float | None
    percentile75: float | None


class Effect(BaseModel):
    name: str
    icon: str | None
    score: float
    type: str | None
    votes: int | None


class Terp(BaseModel):
    name: str
    description: str | None
    score: float


class User(BaseModel):
    id: int
    avatar: str | None
    profileImageUrl: str | None
    publicId: str
    userSince: str
    username: str


class Comment(BaseModel):
    id: int
    avatar: str | None
    consumptionMethod: str | None
    created: str | None
    form: str | None
    isPrivate: bool
    language: str
    moderationStatus: str
    potency: dict | None
    rating: int
    reportedBenefits: list[str]
    reportedFeelings: list[str]
    reportedFlavors: list[str]
    reportedNegatives: list[str]
    strainSlug: str
    text: str
    upvotesCount: int
    user: User


class Strain(BaseModel):
    id: int
    averageRating: float
    category: str
    flowerImageSvg: str
    name: str
    nugImage: str
    phenotype: str | None
    reviewCount: int
    shortDescriptionPlain: str | None
    slug: str
    strainTopTerp: str | None
    subtitle: str | None
    thc: float | None
    topEffect: str | None

    comments: list[Comment] = []

    cannabinoids: dict[str, Cannabinoid]
    effects: dict[str, Effect]
    terps: dict[str, Terp]

    def __str__(self):
        #return json.dumps(self.dict(), indent=4)
        return f"{len(self.comments):<5} - {self.slug}"

    def __hash__(self):
        return self.id


class Strainlist(BaseModel):
    strains: list[Strain]
