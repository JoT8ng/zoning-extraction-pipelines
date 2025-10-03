import csv
import pathlib
import os
from llmapi import LLMAPI
from datetime import datetime
from parsing import Parsing
import geopandas as gpd
import pandas as pd
from thefuzz import process
import sys
import json

# Global variables for user configuration
city_name = "Burnaby" # Change accordingly
geoJsonIn = "Burnaby_Zoning.geojson" # Change the filename accordingly. Existing zoning geoJSON geospatial dataset required.
zoningpdf_path = "Example_Burnaby_R1Small-Scale-Multi-Unit-Housing-District.pdf" # Change the filename accordingly. Existing Zoning by-law PDF required.
zoneField = "ZONECODE" # Change the fieldname from your geoJSON accordingly. This field name contains all the zoning category titles
csvOut = "Zoning_Regulations_Out.csv" # Output CSV name
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
SPLIT = False # Change this accordingly. False if zoning by-law PDF is not already split into zoning category sections

# PART 0 - INITIALIZATION
# Initialize LLM
LLM = LLMAPI()
PARSING = Parsing()

# PART 1
# Extract bylaw document text as markdown
text = PARSING.extract_markdown(zoningpdf_path)
pathlib.Path("output.md").write_bytes(text.encode())

# Global variables
zoning_categories = {}

# Check if geojson zoning category field exists. Prepare geojson for Part 5
if geoJsonIn:
    # Uploading the datasets: geojson
    gdf = gpd.read_file(geoJsonIn)
    if zoneField in gdf.columns:
        # Ensuring columns are strings
        gdf[zoneField] = gdf[zoneField].astype(str)
    else:
        print("No matching fieldname found for variable zoneField. Ending Script.")
        sys.exit()
else:
    print("Unable to find geoJSON file. Ending script.")
    sys.exit()

if SPLIT:
    # PART 2
    # Extract zoning categories
    extracted_categories = PARSING.extract_zoning_titles(text)

    # Compare the list of extracted titles with the list of zoning information from the geojson. Fuzzy matching required
    for zoning_title in extracted_categories:
        match, score = process.extractOne(zoning_title, gdf[zoneField].unique())
        if score > 88:
            # If there is a match- save the key value pair into a dictionary
            zoning_categories[zoning_title] = {
            "zoneField": gdf[gdf[zoneField] == match][zoneField].values[0],
            "status": "match",
            "section": ""
            }
        else:
            # If there is no match- save the geojson zoning information into the dictionary and flag as a comment "no match in by-law titles"
            zoning_categories[zoning_title] = {
            "zoneField": gdf[gdf[zoneField] == match][zoneField].values[0],
            "status": "no match in by-law titles",
            "section": ""
            }

    print("Zoning Categories Extracted:", zoning_categories)

    # Save zoning categories into a json file for logging
    zoning_categories_path = os.path.join("zoning-out", "zoning_categories.txt")
    with open(zoning_categories_path, "w", encoding="utf-8") as f:
        json.dump(zoning_categories, f, ensure_ascii=False, indent=4)

    #PART 3
    # Split bylaw markdown text into zoning category sections
    # Split by zoning categories using exact matches

    # Update list of zoning category titles to include only titles that have a "match" status in zoning_categories dictionary
    matched_categories = []
    for title in extracted_categories:
        # Check if title has "match" status in zoning_categories
        if title in zoning_categories and zoning_categories[title]["status"] == "match":
            matched_categories.append(title)

    # Call function to split zoning text by zoning categories
    zoning_categories = PARSING.split_zoning_sections(text, matched_categories, zoning_categories)

else:
    print(f"PDF is already split into zoning category sections. Sending directly to LLM")

    zoning_categories = PARSING.onezoningsection_extractext(text, zoning_categories)

# PART 4
# Extract data from each zoning category section by querying LLM & write results to CSV
LLM_responses = {}

# Modify prompts to extract the relevant information from the zoning text you want. In this example building height and maximum lot coverage is used.
promptHeight = ("Extract the maximum building height value from this excerpt of a Canadian zoning by-law. If no height can be found/extracted, respond with 'Invalid' followed by the reason why you could not find the value. Provide the height value as a number only. Do not include any other text. Do not include units. Be careful to not interpret the page number as the height value. Zoning by-law excerpt:")
promptCoverage = ("Extract the maximum lot coverage value from this excerpt of a Canadian zoning by-law. If no coverage can be found/extracted, respond with 'Invalid' followed by the reason why you could not find the value. Provide the coverage value as a number only. Do not include any other text. Do not include units. Be careful to not interpret the page number as the coverage value. Zoning by-law excerpt:")

regulationList= [["zone", "height", "coverage", "flagged response"]] # This list will store all the LLM responses for conversion to CSV. Modify names accordingly

for title, content in zoning_categories.items():
    if content["status"] == "match":
        # Each of the above prompts will be sent individually to the LLM. The model will be queried once per zoning regulation required for every zone.
        messageHeight = f"{promptHeight} {title}, {content["section"]}"
        messageCoverage = f"{promptCoverage} {title}, {content["section"]}"  
        try:
            # Set variables to be used to store returned values
            zoneTitle = title
            height = ""
            coverage = ""
            flag = ""

            print(f"Sending query to LLM for HEIGHT: {title}")
            # print(f"LLM Prompt: {message[:300]}") Use this for debugging
            response = LLM.query_llm(messageHeight)
            # Store valid LLM responses into memory
            if "Invalid" not in response and len(response) < 10: # Modifying this condition to capture instances where response is verbose.
                LLM_responses[title] = response
                print(f"Storing LLM response for {title} into memory")
                height = response
                print("\n---\n")
            else: # If invalid or long response, flag field as invalid and write raw response to "flag" column
                LLM_responses[title] = response
                print(f"Storing LLM response for {title} into memory - INVALID")
                height = "Invalid"
                flag += " HEIGHT: " + response
                print("\n---\n")
            
            print(f"Sending query to LLM for COVERAGE: {title}")
            # print(f"LLM Prompt: {message[:300]}") Use this for debugging
            response = LLM.query_llm(messageCoverage)
            # Store valid LLM responses into memory
            if "Invalid" not in response and len(response) < 10: # Modifying this condition to capture instances where response is verbose.
                LLM_responses[title] = response
                print(f"Storing LLM response for {title} into memory")
                coverage = response
                print("\n---\n")
            else: # If invalid or long response, flag field as invalid and write raw response to "flag" column
                LLM_responses[title] = response
                print(f"Storing LLM response for {title} into memory - INVALID")
                coverage = "Invalid"
                flag += " COVERAGE: " + response
                print("\n---\n")
            regulationList.append([zoneTitle, height, coverage, flag])
        except Exception as error:
            print(f"Error: {str(error)}")

# Write results for all zoning categories with titles with status "matched" into CSV       
csvOut = f"Zoning_Regulations_{timestamp}.csv"
with open(csvOut, mode='w', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in regulationList:
        writer.writerow(row)

# PART 5
# Output to geoJSON
# Uploading the datasets: csv
df = pd.read_csv(csvOut)

# Ensuring columns are strings
df["zone"] = df["zone"].astype(str)

# Function to find best match from csv
def get_best_match (zone_title, choices):
    match, score = process.extractOne(zone_title, choices)
    return match if score > 88 else None

# Applying fuzzy matching
df["clean_zone"] = df["zone"].apply(lambda x: get_best_match(x, gdf[zoneField].unique()))

# Merging matched data back to csv
df_matched = df.dropna(subset=["clean_zone"])
df_matched = df_matched.rename(columns={"clean_zone": zoneField})

# Adding a quality control field
df_matched["QC_Check"] = "matched" 

# Merging with geojson to bring in height, coverage, flagged response, and QC_Check
gdf = gdf.merge(df_matched[[zoneField, "height", "coverage", "flagged response", "QC_Check"]], on= zoneField, how="left")    

# Filling unmatched records with "not matching"
gdf["QC_Check"] = gdf["QC_Check"].fillna("not matching")

# Saving the output as a new geogson
output_filename = f"{city_name}_zoing_enriched_{timestamp}.geojson"
gdf.to_file(output_filename, driver="GeoJson")

print (f"GeoJSON file saved as {output_filename}")


print(f"\n****************Code run complete!****************")