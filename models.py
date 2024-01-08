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

    cannabinoids: dict[str, Cannabinoid]
    effects: dict[str, Effect]
    terps: dict[str, Terp]

    def __hash__(self):
        return self.id


class Strainlist(BaseModel):
    strains: list[Strain]
