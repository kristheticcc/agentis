# FastAPI backend for local use (NOT web version)
# Imports
from fastapi import FastAPI
from models import PatientRequest, RankedOutput
from pipeline import run_pipeline
from fastapi.responses import RedirectResponse

app = FastAPI(title="AGENTIS")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


# endpoint for using agentis
@app.post("/match-trials", response_model=RankedOutput)
async def match_trials(patient_info: PatientRequest):
    return await run_pipeline(patient_info)