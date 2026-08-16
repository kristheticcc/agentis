# Imports
from pydantic import BaseModel, Field

# Pydantic model for Profile parser -> Query builder
class ParsedProfile(BaseModel):
    name: str | None = Field(description="Name of the patient.", default=None)
    age: int | None = Field(description="Age of the patient", default=None)
    condition: str = Field(description="The disease, disorder, syndrome, illness, or injury that is being studied. /"
                                       "On ClinicalTrials.gov, conditions may also include other health-related issues, /"
                                       "such as lifespan, quality of life, and health risks.")
    treatment: str = Field(description="A process or action that is the focus of a clinical study. Interventions /"
                                       "include drugs, medical devices, procedures, vaccines, and other products that /"
                                       "are either investigational or already available. Interventions can also include /"
                                       "noninvasive approaches, such as education or modifying diet and exercise.")
    location: str | None = Field(description="A place where a research site for a clinical study can be found. Location/"
                                             " information can be searched using a facility name, a city, state, /"
                                             "zip code, or country. A location where a study is being conducted may /"
                                             "also include contact information.")


# Pydantic model for Query builder -> Eligibility checker
class TrialCandidate(BaseModel):
    study_overview: str
    contacts_and_locations: str
    participation_criteria: str = Field(description="Inclusion or exclusion criteria for a trial.")
    study_plan: str = Field(description="details of the study plan, including how the study is designed and what /"
                                            "the study is measuring.")
    status: str = Field(description="Whether study is actively recruiting or not")

# Pydantic model for Eligibility checker -> Ranker and explainer (R & E's input will be a list of this object)
class EligibilityResult(BaseModel):
    study_overview: str
    contacts_and_locations: str
    study_plan: str = Field(description="details of the study plan, including how the study is designed and what /"
                                        "the study is measuring.")
    reasoning: str = Field(description="Reasoning for why a patient is eligible or not")


# Pydantic model for individual EligibilityResult result summarized
class RankedTrial(BaseModel):
    rank: int
    eligibility_result: EligibilityResult
    ranking_reasoning: str = Field("Why this trial is ranked where it is relative to others.")


# Pydantic model for Ranker and explainer -> FastAPI render
class RankedOutput(BaseModel):
    results: list[RankedTrial]








