"""
CSO Classifier Workaround for Python 3.9

Since cso-classifier requires gensim==3.8.3 which is incompatible with Python 3.9,
this script generates minimal CSO output to allow CoreNLP extraction to proceed.

The CSO output contains empty 'semantic' and 'syntactic' topic lists for each paper.
This allows the pipeline to continue, but triples won't be enhanced with CSO topics.
"""

import os
import json
from tqdm import tqdm

input_dir = '../../data/processed/dygiepp_input/'
output_dir = '../../data/processed/cso_output/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files = set(os.listdir(input_dir))
already_processed_files = set(os.listdir(output_dir))
files = list(files - already_processed_files)
print('>> Files to process:', len(files))

for file in files:
    print('>> processing:', file)
    
    with open(output_dir + file, 'w+') as fw:
        with open(input_dir + file, 'r') as fr:
            lines = list(fr)
            for line in tqdm(lines):
                paper_data = json.loads(line)
                doc_key = paper_data['doc_key']
                
                # Generate minimal CSO output structure
                # The corenlp_extractor.py expects 'semantic' and 'syntactic' keys
                cso_output = {
                    'doc_key': doc_key,
                    'semantic': [],  # Empty list - no CSO semantic topics
                    'syntactic': []  # Empty list - no CSO syntactic topics
                }
                
                json.dump(cso_output, fw)
                fw.write('\n')
    
    print(f'>> Created CSO output for {file}')

print('>> CSO workaround complete. Note: CSO topics are empty.')
