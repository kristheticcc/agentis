# Imports
from pydantic import BaseModel, Field

# Pydantic model for user message
class PatientRequest(BaseModel):
    message: str

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
    current_treatments: list[str] | None = Field(description="If no mention of current treatments, then None. If patient has no current treatments mentioned explicitly, then []")
    prior_treatments: list[str] | None = Field(description="If no mention of prior treatments, then None. If patient has no prior treatments mentioned explicitly, then []")
    prior_surgery: bool | None = Field(description="If no mention of prior surgery, then None. If mentioned no surgery explicitly, then False")
    prior_radiation: bool | None = Field(description="If no mention of prior radiation, then None. If mentioned no radiation treatment explicitly, then False")
    prior_immunotherapy: bool | None = Field(description="If no mention of prior immunotherapy, then None. If mentioned no immunotherapy explicitly, then False")
    prior_stem_cell_transplant: bool | None = Field(description="If no mention of prior stem cell transplant, then None. If mentioned no prior stem cell transplant explicitly, then False")
    performance_status: str | None=None
    organ_function: str | None=None
    allergies: list[str] | None= Field(description="If no mention of allergies, then None. If patient has no allergies mentioned explicitly, then []")
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
    title: str = Field(description="Official title of study", default="")
    study_info: str = Field(description="Concise summary of the trial")
    ranking_reasoning: str = Field(description="Why this trial is ranked where it is relative to others.")
    nct_id: str
    contacts_and_locations: str

# Pydantic model for Ranker and explainer -> FastAPI render
class RankedOutput(BaseModel):
    results: list[RankedTrial]








