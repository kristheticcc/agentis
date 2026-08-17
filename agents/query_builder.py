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
        nct_id = trial["protocolSection"].get("identificationModule", {}).get("nctId", "")
        study_overview = (trial["protocolSection"].get("identificationModule", {}).get("briefTitle", "") + "," +
                          trial["protocolSection"].get("identificationModule", {}).get("officialTitle", ""))

        status = trial["protocolSection"].get("statusModule", {}).get("overallStatus", "")
        participation_criteria = (trial["protocolSection"].get("eligibilityModule", {}).get("eligibilityCriteria", "") +
                                         trial["protocolSection"].get("eligibilityModule", {}).get("sex", "") +
                                         trial["protocolSection"].get("eligibilityModule", {}).get("minimumAge", "")+
                                         ",".join(trial["protocolSection"].get("eligibilityModule", {}).get("stdAges", []))
                                         )
        contacts_and_locations = []
        locations_list_of_dicts = trial["protocolSection"].get("contactsLocationsModule", {}).get("locations", [])
        for location in locations_list_of_dicts:
            facility = location.get("facility", "")
            city = location.get("city", "")
            state = location.get("state", "")
            zip_code = location.get("zip", "")
            country = location.get("country", "")
            contact_and_location = f"{facility}, {city}, {state}, {zip_code}, {country}"
            contacts_and_locations.append(contact_and_location)

        contacts_and_locations = ";".join(contacts_and_locations)

        study_plan = (",".join(trial["protocolSection"].get("designModule", {}).get("phases", [])) +
                             trial["protocolSection"].get("descriptionModule", {}).get("detailedDescription", ""))

        # Trial Candidate object add to the list of trial candidates
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










