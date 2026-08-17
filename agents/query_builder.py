# Imports
import requests
from models import TrialCandidate, ParsedProfile

# Base url for clinicaltrials.gov
base_url = "https://clinicaltrials.gov/api/v2/studies"

# System prompt to guide LLM's behavior
system_prompt = "Extract the information from the text completely and accurately."


def query_builder(parser_profile: ParsedProfile):
    # Query parameters
    params = {
        "query.cond" : parser_profile.condition,
        "query.locn" : parser_profile.location,
        "pageSize" : 20,
    }

    # Getting the content from API
    response = requests.get(base_url, params=params)

    # Error checks
    if response.status_code != 200:
        return f"something went wrong: {response.status_code}"

    # Loading as json
    response_json = response.json()

    # List of trials
    trial_candidates = []

    # Checking each trial in retrieved content and adding required and important trial content into the list
    for trial in response_json["studies"]:
        nct_id = trial["protocolSection"]["identificationModule"].get("nctId")
        study_overview = (trial["protocolSection"]["identificationModule"].get("briefTitle") +
                          trial["protocolSection"]["identificationModule"].get("officialTitle"))

        status = trial["protocolSection"]["statusModule"].get("overallStatus")
        participation_criteria = (trial["protocolSection"]["eligibilityModule"].get("eligibilityCriteria") +
                                         trial["protocolSection"]["eligibilityModule"].get("sex") +
                                         trial["protocolSection"]["eligibilityModule"].get("minimumAge")+
                                         ",".join(trial["protocolSection"]["eligibilityModule"].get("stdAges", []))
                                         )
        contacts_and_locations = "".join(trial["protocolSection"]["contactsLocationsModule"])
        study_plan = (",".join(trial["protocolSection"]["designModule"].get("phases", [])) +
                             trial["protocolSection"]["descriptionModule"].get("detailedDescription"))

        trial_candidate = TrialCandidate(
            nct_id = nct_id,
            study_overview=study_overview,
            contacts_and_locations=contacts_and_locations,
            participation_criteria=participation_criteria,
            study_plan=study_plan,
            status=status,
        )

        trial_candidates.append(trial_candidate)


    return trial_candidates










