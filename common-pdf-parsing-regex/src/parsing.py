import pymupdf4llm
import re
import pathlib
import os
import geopandas as gpd
import pandas as pd
import sys
import json

class Parsing:
    # Global variables
    zoning_categories = {}

    # Regex pattern to extract zoning categories
    zoning_regex_b = r"\*\*([^*]+)\*\*" # Use this pattern for titles in "**bold**"
    zoning_regex_h = r"(#+)\s*(.*)" # Use this pattern for titles in "### header title format". Captures any number of "#"

    if SPLIT:
        # PART 2
        # Identify zoning categories in document via document section titles
        zoning_categories_b = []
        zoning_categories_h = []
        extracted_categories = []

        # Split text into lines for processing
        lines = text.splitlines()

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

        for line in lines:
            match_b = re.search(zoning_regex_b, line)
            match_h = re.search(zoning_regex_h, line)
            # Change keyword depending on by-law
            if match_b and any(keyword in line.lower() for keyword in ["zone", "district", "division"]):
                cleaned_line = line.strip()
                if len(cleaned_line) <= 150:
                    zoning_categories_b.append(cleaned_line)
            if match_h and any(keyword in line.lower() for keyword in ["zone", "district", "division"]):
                cleaned_line = line.strip()
                if len(cleaned_line) <= 150:
                    zoning_categories_h.append(cleaned_line)

        # Combine extracted zoning categories
        extracted_categories = zoning_categories_b + zoning_categories_h

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

        # Loop through zoning categories and extract sections between them
        for i, title in enumerate(matched_categories):
            if title in text:
                # Find the start index of the current title
                start_index = text.index(title) + len(title)
                
                # Determine the end index by finding the next title
                if i + 1 < len(matched_categories) and matched_categories[i + 1] in text:
                    end_index = text.index(matched_categories[i + 1])
                else:
                    end_index = len(text)  # If it's the last title, capture everything to the end
                
                # Extract the section content
                section_content = text[start_index:end_index].strip()
                
                # Save the content if it's non-empty
                if section_content:
                    zoning_categories[title]["section"] = section_content

        # Print zoning sections with their titles and content for debugging
        for title, content in zoning_categories.items():
            print(f"Title: {title}")
            print(f"Zone Field: {content["zoneField"]}")
            print(f"Status: {content["status"]}")
            print(f"Content: {content["section"][:300]}...")  # Print the first 300 characters of the content
            print("\n---\n")

        # Save zoning sections into separate text files for logging
        for title, content in zoning_categories.items():
            if content["status"] == "match":
                # Create a sanitized filename from the title
                filename = re.sub(r'[<>:"/\\|?*\n]', '_', title)
                filename = filename[:150] # If title is long truncate title
                filepath = os.path.join("sections-out", filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Title: {title}\n\n")
                    f.write(content["section"])
    else:
        print(f"PDF is already split into zoning category sections. Sending directly to LLM")

        # Extract zoning category title
        # Split text into lines for processing
        lines = text.splitlines()

        extracted_title = None

        for line in lines:
            match_b = re.search(zoning_regex_b, line)
            match_h = re.search(zoning_regex_h, line)
            # Change keyword depending on by-law
            if match_b and any(keyword in line.lower() for keyword in ["zone", "district", "division"]):
                cleaned_line = line.strip()
                if len(cleaned_line) <= 150:
                    # Save the first title with keyword as the title in zoning_categories
                    if extracted_title is None:
                        extracted_title = cleaned_line
                        zoning_categories[extracted_title] = {
                            "status": "match",
                            "section": ""
                        }
                    break
            if match_h and any(keyword in line.lower() for keyword in ["zone", "district", "division"]):
                cleaned_line = line.strip()
                if len(cleaned_line) <= 150:
                    # Save the first title with keyword as the title in zoning_categories
                    if extracted_title is None:
                        extracted_title = cleaned_line
                        zoning_categories[extracted_title] = {
                            "status": "match",
                            "section": ""
                        }
                    break

        # Save markdown text as section in zoning_categories
        zoning_categories[extracted_title]["section"] = text

        # Print for debugging
        print(f"Title: {extracted_title}")
        print(f"Content: {zoning_categories[extracted_title]["section"][:300]}")