# A Template Is All You Meme
#### Disclaimer: Our work should only ever be used for academic purposes.
Source code and data for [A Template Is All You Meme](https://arxiv.org/abs/2311.06649).

Contact person: [Luke Bates](luke.bates@tu-darmstadt.de)

https://www.ukp.tu-darmstadt.de/

https://www.tu-darmstadt.de/


Don't hesitate to send us an e-mail or report an issue, if something is broken (and it shouldn't be) or if you have further questions.

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.

## Project structure
* `finetune_clip.py` -- fine-tuning CLIP with TSplit / Original splits / baseline (downsampling)
* `clip_model.py` -- CLIP model for fine-tuning
* `tsplit.py` -- Template-Aware Splitter
* `tlc.py` -- Template-Label Counter
* `main.py` -- for running TLC
* `memetils.py` -- util code
* `scraping/` -- scraping scripts

## Requirements
Install [clip first](https://github.com/openai/CLIP).

Then, please use the `requirements.txt` file. 

## KYMKB / Data / Embeddings
[Our data files](https://knowyourmeme.com/memes/chonk-oh-lawd-he-comin) are some [chonky bois](https://knowyourmeme.com/memes/big-chungus)

Please see our scraping code for creating your own KYMKB!

Remember, sometimes memes are mean. We take no responsiblility if they are offensive nor do they reflect our views in any way.

## Installation
To setup, please follow the instructions below.
```
git clone https://github.com/UKPLab/naacl2025-a-template-is-all-you-meme.git
cd a-template-is-all-you-meme
python -m venv mvenv
source mvenv/bin/activate
pip install --upgrade pip
#install clip here please
pip install -r requirements.txt
```
### Reproduce our results: TSplit
## Overview  
The `finetune_clip.py` script fine-tunes OpenAI’s CLIP model on various datasets from the paper. You can specify multiple configurations using command-line arguments.  

## Usage  
Run the script with:  

```
python finetune_clip.py --dataset <dataset> --feature_extraction <encoder> --epochs <num_epochs> ...
```
## Arguments  
You can customize the fine-tuning process with the following arguments:  

### **Required Arguments:**  
- `--dataset`  
  - The dataset to use from the paper.
  -  - **Options**: `multioff`, `memotion3`, `figmemes`, `mami`.  
- `--feature_extraction`  
  - Which encoder to use?  
  - **Options**: `ViT-L/14@336px`, `ViT-B/32`, `ViT-B/16`.  

### **Optional Arguments:**  
- `--data_root`  
  - Location of dataset files.  
  - **Required for**: `figmemes`, `mami`, `multioff`.  
  - **Paths**:  
    - `data/annotations` (for `figmemes`)  
    - `data/MAMI_DATASET` (for `mami`)  
    - `data/MultiOFF_DATASET` (for `multioff`)  

- `--split`  
  - Dataset split strategy.  
  - **Required for**: `figmemes`, `mami`, `multioff`.  
  - **Options**:  
    - `standard`, `task5_style` (for `mami`), `standard` (for `multioff`).  

- `--task`  
  - Task specification (for `Memotion 3` and `MAMI`).  
  - **Options**: `1 = A`, `2 = B`.  

- `--reorganize`  
  - How to split and downsample the dataset.  
  - **Options**:  
    - `original` (original splits)  
    - `baseline` (random downsampling)  
    - `max`, `mean`, `median`, `quantile` (for TSplit variations).  

- `--batch_size` (default: `16`)  
  - Batch size for fine-tuning.  

- `--epochs` (default: `20`)  
  - Number of epochs for fine-tuning.  

- `--seed` (default: `0-4`)  
  - Random seed for modeling/sampling.  

- `--sample_train`, `--random_downsample_tsplit`, `--sample_tsplit`, `--overfit` (default: `False`)  
  - Various options for downsampling or skipping model selection.  
  - **Table References:**  
    - `sample_train` → Table 3 from page 7
    - `random_downsample_tsplit` → Table 9 on page 16 (the first grouping)
    - `sample_tsplit` → Table 9 on page 16 (the second grouping)  
    - `overfit` (Test eval on model trained for `epochs` without selection) → Table 6 on page 15 

If **all four** of these arguments are `False`, the script will TSplit the entire dataset (Table 4 on page 8).  

### TSplit expected results
Results will be written to disk in a json file following this structure:
```
clip_results/{args.overfit}/{args.sample_train}/{args.random_downsample_tsplit}/{args.sample_tsplit}/{args.dataset}/{args.reorganize}/{args.feature}/{args.task}/{args.seed}/
```
### Reproduce our results: TLC starting on page 16

You can run TLC by passing arguments to python with:  
```
python main.py
--template_path  # Directory where the KYMKB is located  
--dataset        # Which dataset from the paper you want to play with  
--data_root      # Where the datafiles are located.  
                 # Required for figmemes, mami, and multioff  
                 # Paths:  
                 # - data/annotations (for figmemes)  
                 # - data/MAMI_DATASET (for mami)  
                 # - data/MultiOFF_DATASET (for multioff)  
--num_neigh      # Number of neighbors to consider  
--vote_type      # Template vs label vote  
--split          # Only relevant for figmemes, mami, and multioff  
                 # Values: standard, task5_style (for mami), standard (for multioff)  
--include_examples  # Template or templates + examples?  
                    # True (template only) or False (template + examples)  
--feature_extraction  # Which encoder to use?  
                      # Options: ViT-L/14@336px, ViT-B/32, ViT-B/16  
--task           # Only relevant for Memotion 3 and MAMI  
                 # Options: 1 = A, 2 = B  
--combine        # How to model the modalities  
                 # Options: None (template vs memes), concatenate, fusion,  
                 # latefusion, fancy (normalize then average)  
--just_text      # Use just about vs OCR?  
                 # True or False  
--need_to_read   # Use pre-written embeddings or not?  
                 # True or False  
```
### TLC Expected results
Once finished, results will be printed out.

### Citation
If our work was helpful for your work, please be so kind as to cite us:
```
@article{atiaym_2023,
url = {https://arxiv.org/abs/2311.06649},
author = {Luke Bates and Peter Ebert Christensen and Preslav Nakov and Iryna Gurevych},
keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
journal={arXiv preprint arXiv:2311.06649},
title = {A Template Is All You Meme},
publisher = {arXiv},
year = {2023},
}
```
