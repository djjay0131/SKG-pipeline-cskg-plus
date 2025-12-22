source ~/anaconda3/etc/profile.d/conda.sh

git clone https://github.com/dwadden/dygiepp.git
cd dygiepp


conda create --name dygiepp python=3.8
conda activate dygiepp

pip install torch==1.6.0 -f https://download.pytorch.org/whl/torch_stable.html
pip install transformers 
pip install -r requirements.txt

pip install -e .   # Adds DyGIE to your PYTHONPATH

chmod 755 ./scripts/pretrained/get_dygiepp_pretrained.sh
./scripts/pretrained/get_dygiepp_pretrained.sh

SCIBERT_PATH=$(pwd)/scibert_model
echo "SciBERT absolute path: $SCIBERT_PATH"
  
input_directory=../../../data/processed/dygiepp_input/
output_directory=../../../data/processed/dygiepp_output/

export TRANSFORMERS_OFFLINE=1
export HF_HOME=$(pwd)/hf_cache
mkdir -p $HF_HOME

cat > dygie/models/bert_patch.py << 'EOF'
from transformers import AutoModel, AutoConfig, AutoTokenizer
import os

_original_model_from_pretrained = AutoModel.from_pretrained
_original_config_from_pretrained = AutoConfig.from_pretrained
_original_tokenizer_from_pretrained = AutoTokenizer.from_pretrained

def patched_model_from_pretrained(pretrained_model_name_or_path, *args, **kwargs):
    if 'allenai/scibert_scivocab_cased' in str(pretrained_model_name_or_path):
        local_path = os.path.abspath('./scibert_model')
        print(f'[PATCH] Redirecting model {pretrained_model_name_or_path} to {local_path}')
        return _original_model_from_pretrained(local_path, *args, **kwargs)
    return _original_model_from_pretrained(pretrained_model_name_or_path, *args, **kwargs)

def patched_config_from_pretrained(pretrained_model_name_or_path, *args, **kwargs):
    if 'allenai/scibert_scivocab_cased' in str(pretrained_model_name_or_path):
        local_path = os.path.abspath('./scibert_model')
        print(f'[PATCH] Redirecting config {pretrained_model_name_or_path} to {local_path}')
        return _original_config_from_pretrained(local_path, *args, **kwargs)
    return _original_config_from_pretrained(pretrained_model_name_or_path, *args, **kwargs)

def patched_tokenizer_from_pretrained(pretrained_model_name_or_path, *args, **kwargs):
    if 'allenai/scibert_scivocab_cased' in str(pretrained_model_name_or_path):
        local_path = os.path.abspath('./scibert_model')
        print(f'[PATCH] Redirecting tokenizer {pretrained_model_name_or_path} to {local_path}')
        return _original_tokenizer_from_pretrained(local_path, *args, **kwargs)
    return _original_tokenizer_from_pretrained(pretrained_model_name_or_path, *args, **kwargs)

AutoModel.from_pretrained = patched_model_from_pretrained
AutoConfig.from_pretrained = patched_config_from_pretrained
AutoTokenizer.from_pretrained = patched_tokenizer_from_pretrained
EOF

# Add the patch to dygie's __init__.py
echo "from dygie.models import bert_patch" >> dygie/__init__.py

mkdir -p ${output_directory}

for file in ${input_directory}*
do
        
        filename=$(basename ${file})
        echo '> dygiepp processing: '$filename
        if  [ ! -e ${output_directory}/${filename} ]; then
                allennlp predict pretrained/scierc_local.tar.gz $input_directory$filename --predictor dygie --include-package dygie --use-dataset-reader --output-file $output_directory${filename}  --cuda-device -1
        fi
done


