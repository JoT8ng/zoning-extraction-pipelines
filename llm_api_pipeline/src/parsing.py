import pymupdf4llm
import re
import os

class Parsing:

    def __init__(self):
        pass

    def extract_markdown(self, pdf_path):
        # Function to extract bylaw document text as markdown
        text = pymupdf4llm.to_markdown(pdf_path)
        return text
    
    def extract_zoning_titles(self, text):
        # Function to extract zoning category titles using regex

        # Regex pattern to extract zoning categories
        zoning_regex_b = r"\*\*([^*]+)\*\*" # Use this pattern for titles in "**bold**"
        zoning_regex_h = r"(#+)\s*(.*)" # Use this pattern for titles in "### header title format". Captures any number of "#"

        # Identify zoning categories in document via document section titles
        zoning_categories_b = []
        zoning_categories_h = []
        extracted_categories = []

        # Split text into lines for processing
        lines = text.splitlines()

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

        return extracted_categories
    
    def split_zoning_sections(self, matched_categories, text, zoning_categories):
        # Function to split zoning text by zoning categories

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

        return zoning_categories
    
    def onezoningsection_extractext(self, text, zoning_categories):
        # Function to extract text and zoning category title if zoning bylaw pdf is already split into zoning category sections

        # Regex pattern to extract zoning categories
        zoning_regex_b = r"\*\*([^*]+)\*\*" # Use this pattern for titles in "**bold**"
        zoning_regex_h = r"(#+)\s*(.*)" # Use this pattern for titles in "### header title format". Captures any number of "#"

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

        return zoning_categories