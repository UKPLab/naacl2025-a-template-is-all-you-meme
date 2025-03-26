# KYMKB Encoder

The KYMKB Encoder extracts and encodes image features from meme templates and example images stored in the KYMKB. The extracted features can be used for various downstream tasks, such as meme classification or retrieval.

## Features
- Loads and processes meme templates and example images from the KYMKB.
- Uses CLIP to generate embeddings for both templates and examples.
- Handles missing images.
- Supports efficient batch processing on GPU.

## Usage
### Initializing the Encoder
The `KYMKBEncoder` class requires three main components:
1. **`args`**: Contains the path to the KYMKB JSON file and which CLIP model yout want to use.
2. **`preprocess`**: A preprocessing function for CLIP.
3. **`model`**: A clip model to compute image embeddings.

Example:
```
import argparse
import clip

parser = argparse.ArgumentParser(description='encoding_kymkb')
parser.add_argument('--feature_extraction', action="store", type=str, dest='feature', default='ViT-L/14@336px')
parser.add_argument('--data_path', type=str, default='data/updated_chonky_meme_data.json', help="Path to the JSON file containing KYMKB data.")
args = parser.parse_args()

model, preprocess = clip.load(args.feature)
encoder = KYMKBEncoder(args, preprocess, model)
encoder.get_template_embeddings()
encoder.get_template_example_embeddings()
```

### Data Structure
The following code assumes your KYMKB follows this structure:
```json
{
    "endfathersday": {
        "title": "#EndFathersDay",
        "url": "https://knowyourmeme.com/memes/endfathersday",
        "base_template": "https://i.kym-cdn.com/entries/icons/original/000/015/825/766736550778035887.png",
        "example_images": [
            "https://i.kym-cdn.com/photos/images/newsfeed/000/776/270/48f.png",
            "https://i.kym-cdn.com/photos/images/newsfeed/000/776/274/7f8.png"
        ]
    }
}
```

## Methods
### `get_template_embeddings()`
Extracts and encodes **only** the base meme templates.

### `get_template_example_embeddings()`
Extracts and encodes **both** meme templates and their example images.

### `clip_features(image_lst)`
Encodes images into feature vectors using CLIP.


## Output
The model produces:
- **`self.just_template_embeddings`**: Feature vectors for meme templates.
- **`self.template_embeddings`**: Feature vectors for both templates and examples.

## Notes
- Ensure images are stored in the `data/` directory before running encoding.
- Missing images will be skipped with a warning.
- Processing speed depends on GPU availability and batch size.

