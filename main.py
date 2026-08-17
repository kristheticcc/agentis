from agents.profile_parser import profile_parser
from agents.query_builder import query_builder
def main():
    print("Hello from agentis!")
    patient_info = "58 year old male with newly diagnosed multiple myeloma, currently taking bortezomib and dexamethasone, no prior stem cell transplant, no prior radiation, good kidney function."
    print("------------------ PATIENT INFO ------------------------------")
    print(patient_info)

    profile_parser_output = profile_parser(patient_info)
    print("------------------- PARSED PROFILE -----------------------")
    print(profile_parser_output)

    print("--------------------- QUERY BUILDER OP/ TRIAL CANDIDATES-----------------------------")
    query_builder_output = query_builder(profile_parser_output)
    print(query_builder_output)



if __name__ == "__main__":
    main()
