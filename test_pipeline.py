from input_handler import get_text_from_file 
from nlp_pipeline import preprocess_text, extract_entities, extract_relationships, process_text_in_chunks 
import os
import json

# Specify the folder containing your input files (PDFs and text files)
input_folder_path = '/Users/aravindsundaresan/AI_mapping'

# Get a list of all supported files in the folder (PDFs and .txt files for now)
supported_extensions = ['.pdf', '.txt'] 
input_files = [f for f in os.listdir(input_folder_path) if any(f.endswith(ext) for ext in supported_extensions)]

for input_file in input_files:
    input_file_path = os.path.join(input_folder_path, input_file)

    try:
        extracted_text = get_text_from_file(input_file_path)

        if extracted_text:
            # Process the extracted text in chunks (if it's large)
            if len(extracted_text) > 100000:  # Adjust the threshold as needed
                all_entities, all_relationships = process_text_in_chunks(extracted_text)
            else:
                all_entities = extract_entities(extracted_text)
                all_relationships = extract_relationships(extracted_text)

            # Create a dictionary to store the output
            output_data = {
                "extracted_text": extracted_text,
                "preprocessed_tokens": preprocess_text(extracted_text),  # Preprocess the entire text
                "entities": all_entities,
                "relationships": all_relationships
            }

            # Create output file name (JSON format)
            output_file_name = os.path.splitext(input_file)[0] + '_output.json'
            output_file_path = os.path.join(input_folder_path, output_file_name)

            # Save the output to a JSON file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(output_data, output_file, indent=4)

            print(f"Output for {input_file} saved to {output_file_path}")

        else:
            print(f"No text extracted from {input_file}")

    except Exception as e:
        print(f"Error processing {input_file}: {e}")
