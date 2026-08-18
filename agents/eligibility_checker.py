# Imports
import asyncio
from clients import openai_async, gpt_model
from models import EligibilityResult, TrialCandidate, ParsedProfile

# System message to guide LLM's behavior
system_prompt = """you are Eligibility checker. You will be provided with a patient profile and a clinical trial.
                Compare patient profile to the clinical trial and determine whether the patient is eligible for trial
                or not. Do not include irrelevant details.
                """


# Eligibility checker for single trial
async def eligibility_checker_for_one_trial(message):

    response = await openai_async.responses.parse(
        model = gpt_model,
        input=message,
        text_format=EligibilityResult,
    )

    return response.output_parsed

# Input message for LLM
def get_message(profile, trial_candidate):
    return [{"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Patient profile: {profile} | Trial: {trial_candidate}"}
            ]

# Checks patient eligibility by comparing against each clinical trial
async def eligibility_checker(profile: ParsedProfile, trial_candidates: list[TrialCandidate]):

    results = await asyncio.gather(
        *[eligibility_checker_for_one_trial(get_message(profile, trial_candidate)) for trial_candidate in trial_candidates]
    )

    return results




