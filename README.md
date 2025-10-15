Backyard bird classification 
**Next goal -> use pretrained model to make sure there is a bird in the images. Figure out how to get a coordinate of the bird and resize the image so the bird is +50% of the total image.

**Once model is complete, evaluate results against https://huggingface.co/datasets/sasha/birdsnap and https://cocodataset.org/#download

**Setup flask server for raspberry pi

TODO: 
1. Compile list of all backyard Chicago bird species
2. Source images from Cornell Lab’s Macaulay Library
3. Split into train / val / test folders
4. Use pretrained model with custom classification
5. Build raspberry pi webcam server
6. Deploy model live to webcam server * 