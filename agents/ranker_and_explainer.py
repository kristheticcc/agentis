# Imports
from clients import groq_model, groq
from models import EligibilityResult, RankedTrial, RankedOutput

# System prompt to guide LLM's behavior
system_prompt = """You are a helpful assistant. You will be given a list of clinical trials with trial information.
                Extract information and rank them. If a eligibility status is ELIGIBLE, it should have a higher rank.
                If two trials have the same eligibility status, rank them based on eligibility confidence.
               """

def ranker_and_explainer(selected_trials: list[EligibilityResult]):

    eligible_trials = [trial for trial in selected_trials if not trial.eligibility_status=="NOT ELIGIBLE"]

    # To reduce the context size for LLM
    summaries = []

    for t in eligible_trials:
        summaries.append(f"NCT: {t.nct_id} | status: {t.eligibility_status} "
                         f"| title: {t.study_overview} | reason: {t.reasoning} "
                         f"| location: {t.contacts_and_locations}")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "\n".join(summaries)},
    ]

    response = groq.responses.parse(
        input=messages,
        model = groq_model,
        text_format=RankedOutput
    )

    ranked = response.output_parsed

    trials_by_id = {trial.nct_id: trial for trial in eligible_trials}

    for ranked_trial in ranked.results:
        original = trials_by_id.get(ranked_trial.nct_id)
        if original:
            ranked_trial.contacts_and_locations = original.contacts_and_locations

    return ranked



