import pandas as pd
import numpy as np
import sys

def estimate(result):
    if result == 0:
        return "Well"
    elif result > 0:
        return "Under"
    else:
        return "Over"


path = "./data/"
# raw_filename = "YMCA_Sprint57.csv"
raw_filename = sys.argv[1]
clean_filename = raw_filename[0:-4] + "_cleaned.csv"

data = pd.read_csv(path + raw_filename, sep=",", encoding="utf-8", header=0)
print("Reading file :: " + raw_filename + "")

data['Missile'] = np.where(
    data["Tags"].str.contains("Missile") == True, "Missile", "Plan"
)
print("Cleaning 'Tag' -> 'Missile' & 'Plan'")

data['State'] = np.where(
    data["State"].str.contains("Active") == True, "Closed", data["State"]
)
print("Cleaning State 'Active' -> 'Closed'")

data['Story Points'] = np.where(
    np.isnan(data['Story Points']) == True, data["Estimate Story Point"], data["Story Points"]
)
print("Cleaning Removed point")

data["Estimate"] = data["Story Points"]-data["Estimate Story Point"]
data["Estimate"] = data["Estimate"].apply(lambda row: estimate(row))
print("Cleaning Point Estimation")

data['Area Path'] = data["Area Path"].str.split('\\', n=1, expand=True)[1]
print("Cleaning 'Area Path Name' -> Remove Prefix")

data['AreaPathType'] = np.where(
    data["Area Path"] == "JIBSoft Project\Other", "Support", "Project"
)
print("Cleaning 'Area Path Type' -> 'Support' & 'Project'")

data.to_csv(path + clean_filename, encoding="utf-8", sep=",", index=False)
print("Writing new file :: " + clean_filename + "")

print("Complete...")
