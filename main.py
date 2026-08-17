from agents.profile_parser import profile_parser
from agents.query_builder import query_builder
def main():
    print("Hello from agentis!")
    example = profile_parser("61 year old male with stage 2 pancreatic cancer, currently taking gemcitabine, no prior radiation, no prior immunotherapy, otherwise healthy with good organ function.")
    print("-----------------------------------------------------------------")
    #print(profile_parser("48 year old female with stage 3 ovarian cancer, currently taking carboplatin and paclitaxel, no prior surgeries, no prior radiation, no known allergies, ECOG performance status 1."))
    #print("-----------------------------------------------------------------")
    #print(profile_parser("58 year old male with newly diagnosed multiple myeloma, currently taking bortezomib and dexamethasone, no prior stem cell transplant, no prior radiation, good kidney function."))

    print(query_builder(example))



if __name__ == "__main__":
    main()
