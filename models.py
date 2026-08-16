# Imports
from pydantic import BaseModel, Field

# Pydantic model for Profile parser -> Query builder
class ParsedProfile(BaseModel):
    name: str | None = Field(description="Name of the patient.", default=None)
    age: int | None = Field(description="Age of the patient", default=None)
    sex: str | None = Field(description="Sex of the patient", default=None)
    condition: str = Field(description="The disease, disorder, syndrome, illness, or injury that is being studied. /"
                                       "On ClinicalTrials.gov, conditions may also include other health-related issues, /"
                                       "such as lifespan, quality of life, and health risks.")
    cancer_stage: str | None=None
    diagnosis_status: str | None=None
    current_treatments: list[str] | None=None
    prior_treatments: list[str] | None=None
    prior_surgery: bool | None=None
    prior_radiation: bool | None=None
    prior_immunotherapy: bool | None=None
    prior_stem_cell_transplant: bool | None=None
    performance_status: str | None=None
    organ_function: str | None=None
    allergies: list[str] | None=None
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
    nct_id: str

# Pydantic model for Eligibility checker -> Ranker and explainer (R & E's input will be a list of this object)
class EligibilityResult(BaseModel):
    nct_id: str
    study_overview: str
    contacts_and_locations: str
    study_plan: str = Field(description="details of the study plan, including how the study is designed and what /"
                                        "the study is measuring.")
    reasoning: str = Field(description="Reasoning for why a patient is eligible or not")
    eligibility_status: str = Field(description="Eligibility status of the patient, ELIGIBLE or NOT ELIGIBLE or UNCERTAIN.")
    status: str = Field(description="Whether study is actively recruiting or not")

# Pydantic model for individual EligibilityResult result summarized
class RankedTrial(BaseModel):
    rank: int
    eligibility_result: EligibilityResult
    ranking_reasoning: str = Field("Why this trial is ranked where it is relative to others.")


# Pydantic model for Ranker and explainer -> FastAPI render
class RankedOutput(BaseModel):
    results: list[RankedTrial]








