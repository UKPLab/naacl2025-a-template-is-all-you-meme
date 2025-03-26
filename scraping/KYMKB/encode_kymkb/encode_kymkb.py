import argparse
import json
import gc
import glob
from tqdm import tqdm
import PIL.Image
import torch
import numpy as np

parser = argparse.ArgumentParser(description='encoding_kymkb')
parser.add_argument('--feature_extraction', action="store", type=str, dest='feature', default='ViT-L/14@336px')
parser.add_argument('--data_path', type=str, default='data/kymkb.json', help="Path to the JSON file containing KYMKB data.")



class KYMKBEncoder:
    def __init__(self, args, preprocess, model):
        self.args = args
        self.preprocess = preprocess
        self.model = model
        self.info = []
        self.idx_lst = []

    def get_template_embeddings(self):
        template_images = []
        self.info = json.load(open(self.args.path, 'r'))  # Load full JSON structure
        
        for template_name, template_data in tqdm(self.info.items()):
            if "base_template" in template_data:
                try:
                    im = self.preprocess(PIL.Image.open(f'data/{template_data["base_template"].split("/")[-1]}'))
                    template_images.append(im)
                    self.idx_lst.append(template_name)
                except Exception as e:
                    print(f'Error loading template {template_name}: {e}')
        
        self.just_template_embeddings = self.clip_features(template_images)

    def get_template_example_embeddings(self):
        miss_count = 0
        temps_and_examples = []
        self.idx_lst = []
        
        for template_name, template_data in tqdm(self.info.items()):
            # Process base template
            if "base_template" in template_data:
                try:
                    template_im = self.preprocess(PIL.Image.open(f'data/{template_data["base_template"].split("/")[-1]}'))
                    temps_and_examples.append(template_im)
                    self.idx_lst.append(template_name)
                except Exception as e:
                    print(f'Error loading template {template_name}: {e}')
            
            # Process example images
            if "example_images" in template_data:
                for example_url in template_data["example_images"]:
                    try:
                        example_im = self.preprocess(PIL.Image.open(f'data/{example_url.split("/")[-1]}'))
                        temps_and_examples.append(example_im)
                        self.idx_lst.append(template_name)
                    except Exception as e:
                        print(f'Miss: {example_url} ({e})')
                        miss_count += 1
        
        print(f'Total misses: {miss_count}')
        self.template_embeddings = self.clip_features(temps_and_examples)
    
    def clip_features(self, image_lst):
        tensor = torch.tensor(np.stack(image_lst)).cuda()
        dataset = self.torch_dataset(tensor)
        if len(dataset) == 1:
            with torch.no_grad():
                for x in dataset:
                    embeddings = np.array(self.model.encode_image(x[0]).float().cpu())#.cpu()
            gc.collect()
            torch.cuda.empty_cache()
            return embeddings
        else:
            embeddings = np.zeros(shape=(len(image_lst), self.model.ln_final.normalized_shape[0]))
            stop = 0
            for idx, x in tqdm(enumerate(dataset)):
                with torch.no_grad():
                    image_features = np.array(self.model.encode_image(x[0]).float().cpu())#.cpu()
                
                rows = image_features.shape[0]
                if idx != len(dataset)-1:
                    start = (idx * rows)
                    stop = (idx+1) * rows    
            
                else:
                    start = stop
                    stop = stop + rows

                embeddings[start:stop, :] = image_features
            gc.collect()
            torch.cuda.empty_cache()
            
            return embeddings
