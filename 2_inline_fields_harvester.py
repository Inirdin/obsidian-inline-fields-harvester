import re
import os

### Define the input and output directories
vault_location = r"D:\\_Vault"  # Change this
output_location = r".\\processed_files"

### Function to process inline fields and convert them to YAML or YAML list items
def format_field(line):
    # Split the line into field and value using "::"
    field, item = line.split("::")

    # remove trailing whitespace
    field = field.strip()
    item = item.strip()

    # rename field if it is "tag/s" to "types"
    field = re.sub(r'\btag(?:s)?\b', "types", field, flags=re.IGNORECASE)

    # create list if there are links side by side even without ","
    item = re.sub(r"\]\]\s+\[\[", "]], [[", item)

    # if there are multiple items move them to new lines
    if "," in item:
        item = "\n" + re.sub(r",\s*","\n",item)

    # if there is single " escape it
    if "\"" in item:
        item = re.sub(r"\"", "\\\"", item)

    # remove ! at the start of any value
    item = re.sub(r'^!\s*', "", item)

    # format the items
    if item.count('\n') > 1: # if item constains list of values
        lines = item.split("\n")
        new_lines = [lines[0].strip() + '"' if lines[0].strip() else '']
        for line in lines[1:]:
            # enclose anything but numbers
            if not line.strip().isdigit():
                new_lines.append("- \"" + line.strip() + "\"")
            else:
                new_lines.append("- " + line.strip())
        item = "\n".join(new_lines) # combine all new lines into one string
    else: # when item isn't list of values
        if item != '':
            if not item.strip().isdigit(): # enclose anything but numbers
                item = '"' + item.strip() + '"'

    return field + ": " + item + "\n"

### Function to process single file
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.readlines()

    inline_fields = []
    content_no_fields = []
    codeblock = False

    # Remove original inline fields outside of the frontmatter
    for line in content:
        # Ignore "::" in code block
        if '```' in line:
            codeblock = not codeblock

        # Ignore "::" in inline code block
        pattern = r'`.*::.*`' 
        inline_code = re.search(pattern, line) is not None

        # Put inline fields to new list and remove them from rest of the file contents
        if '::' in line and not codeblock and not inline_code:
            inline_fields.append(format_field(line))
        else:
            content_no_fields.append(line)

    # Check if there are any inline fields
    if inline_fields != []:  
        # Find frontmatter
        frontmatter_index = 0
        frontmatter_started = False

        for line in content_no_fields:
            # Skip empty lines
            if not line.strip(): 
                continue
            # find end of the existing frontmatter
            if line.strip() == '---' or frontmatter_started: 
                if line.strip() == '---' and frontmatter_started:
                    #print(frontmatter_index)
                    break
                frontmatter_started = True
                frontmatter_index += 1
            # create frontmatter
            else:
                #print("no frontmatter")
                content_no_fields = ['---\n', '---\n'] + content_no_fields
                frontmatter_index = 1
                break

        # Move inline fields to frontmatter
        content_no_fields[frontmatter_index:frontmatter_index] = inline_fields
    
    # remove multiple empty lines in whole file
    empty_line_count = 0
    content_no_empty_lines = []
    
    for line in content_no_fields:
        if line.strip() == '':
            empty_line_count += 1
            if empty_line_count <= 1:
                content_no_empty_lines.append(line)
        else:
            content_no_empty_lines.append(line)
            empty_line_count = 0

    # return formated contents of the file
    return content_no_empty_lines

### Function to write processed content to a new file
def write_processed_file(input_file_path, processed_content):
    output_file_path = re.sub(vault_location, output_location, input_file_path)
    output_folder = os.path.dirname(output_file_path)

    print ("Processed file: " + output_file_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(processed_content)

### Read file paths from list.txt and process each file
# File paths shouldn't have " at the start or the end
with open('list.txt', 'r', encoding='utf-8') as file_list:
    # Iterate over each file path in the list
    for file_path in file_list:
        input_file_path = file_path.strip()
        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                processed_content = process_file(input_file_path)
                # write processed content to new file
                write_processed_file(input_file_path, processed_content)
        except FileNotFoundError:
            # file from list.txt wasn't found
            print(f"File: '{input_file_path}' not found")

print("Finished")
