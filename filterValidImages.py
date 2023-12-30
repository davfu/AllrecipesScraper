import json

input_file_path = 'FINAL.jsonlines'
output_file_path = 'filtered.jsonlines'

with open(input_file_path, 'r', encoding='utf-8') as input_file, \
        open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        data = json.loads(line)
        if data.get('image') is not None:
            output_file.write(json.dumps(data) + '\n')

print(f"Filtered data written to {output_file_path}")