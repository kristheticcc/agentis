# Imports
import asyncio
from models import PatientRequest
from pipeline import run_pipeline

# For local testing
if __name__ == "__main__":
    # Example patient inputs
    patient_1 = """
        41 year old female with stage 2 cervical cancer, no prior chemotherapy, no prior radiation, 
        no current medications, otherwise healthy, ECOG performance status 0.
        """
    patient_2 = """
    61 year old male with stage 2 pancreatic cancer, currently taking gemcitabine, no prior radiation, 
    no prior immunotherapy, otherwise healthy with good organ function.
    """

    patient_request = PatientRequest(message=patient_2)

    # Outside FastAPI
    example_results = asyncio.run(run_pipeline(patient_request))
    print(example_results)
