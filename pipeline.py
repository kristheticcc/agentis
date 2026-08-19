# Imports
from agents.profile_parser import profile_parser
from agents.query_builder import query_builder
from agents.eligibility_checker import eligibility_checker
from agents.ranker_and_explainer import ranker_and_explainer
from models import PatientRequest, RankedOutput
import asyncio

# Function for calling entire pipeline: profile parser -> query builder -> eligibility checker -> ranker and explainer
async def run_pipeline(patient_info: PatientRequest) -> RankedOutput:

    # Extracting structured patient info from patient information
    print("Parsing patient profile...")
    profile_parsed = await asyncio.to_thread(profile_parser, patient_info.message)

    # Querying clinical trials from clinical.trials.gov
    print("Extracting clinical trials...")
    trials_received = await asyncio.to_thread(query_builder, profile_parsed)

    # If query builder returns error string
    if isinstance(trials_received, str):
        print(f"Query failed: {trials_received}")
        return RankedOutput(results=[])

    # Eligibility list containing eligibility results for each trial
    print("Checking for eligibility...")
    eligibility_list = await eligibility_checker(profile_parsed, trials_received)

    # Ranking and filtering trials for which patient is eligible
    print("Ranking and explaining trials...")
    ranked_and_explained = await asyncio.to_thread(ranker_and_explainer, eligibility_list)

    # Returning ranked and trials (summarized)
    return ranked_and_explained