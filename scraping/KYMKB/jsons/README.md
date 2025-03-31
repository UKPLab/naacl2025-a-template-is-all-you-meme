# KYMKB Data Structure  

The KYMKB (Know Your Meme Knowledge Base) dataset is structured as a JSON object where each key represents a meme template. The value associated with each key contains metadata and image URLs for that meme.  

## Structure  
The overall structure is as follows:  

```
{
    "template_name": {
        "title": "Template Title",
        "url": "Link to Know Your Meme page",
        "base_template": "Link to the base template image",
        "example_images": [
            "Link to example image 1",
            "Link to example image 2",
            ...
        ]
    },
    ...
}
```
### Key Elements  
- **template_name**: A unique identifier for the meme template.  
- **title**: The human-readable title of the meme.  
- **url**: Wayback Machine page where more information about the meme can be found.  
- **base_template**: A link to the base image (template) commonly used in the meme.  
- **example_images**: A list of links to example images that demonstrate how the meme is used.

#### Example
```
{
    "eye-rolling-robert-downey-jr": {
        "title": "Eye Rolling Robert Downey Jr.",
        "url": "http://web.archive.org/web/20230322144534/https://knowyourmeme.com/memes/eye-rolling-robert-downey-jr",
        "base_template": "http://web.archive.org/web/20230409100200/https://i.kym-cdn.com/entries/icons/original/000/020/549/1081.gif",
        "example_images": [
            "http://web.archive.org/web/20221110173432/https://i.kym-cdn.com/photos/images/newsfeed/001/124/042/dfa.jpg",
            "http://web.archive.org/web/20221115142121/https://i.kym-cdn.com/photos/images/newsfeed/001/124/039/430.jpg"
        ]
    }
}
```
