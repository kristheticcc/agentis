# Imports
from agents.profile_parser import profile_parser
from agents.query_builder import query_builder
from agents.eligibility_checker import eligibility_checker
from agents.ranker_and_explainer import ranker_and_explainer
from models import PatientRequest
import asyncio

# Function for calling entire pipeline: profile parser -> query builder -> eligibility checker -> ranker and explainer
async def run_pipeline(patient_info: PatientRequest):

    # Extracting structured patient info from patient information
    print("Parsing patient profile...")
    profile_parsed = profile_parser(patient_info.message)

    # Querying clinical trials from clinical.trials.gov
    print("Extracting clinical trials...")
    trials_received = query_builder(profile_parsed)

    # Eligibility list containing eligibility results for each trial
    print("Checking for eligibility...")
    eligibility_list = await eligibility_checker(profile_parsed, trials_received)

    # Ranking and filtering trials for which patient is eligible
    print("Ranking and explaining trials...")
    ranked_and_explained = ranker_and_explainer(eligibility_list)

    # Returning ranked and trials (summarized)
    return ranked_and_explained

def main():
    message = """
    48 year old female with stage 3 ovarian cancer, currently taking carboplatin and paclitaxel, 
    no prior surgeries, no prior radiation, no known allergies, ECOG performance status 1.
    """
    patient_request = PatientRequest(message=message)
    example_results = run_pipeline(patient_request)
    print(example_results)


if __name__ == "__main__":
    main()
