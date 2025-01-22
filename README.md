
# Photo-Realistic Blocksworld 

This is a repository modified from the [IBM-Repo](https://github.com/ibm/photorealistic-blocksworld) and the  [CLEVR dataset](https://github.com/facebookresearch/clevr-dataset-gen)
for generating realistic visualizations of [blocksworld](https://en.wikipedia.org/wiki/Blocks_world).


Setup:

With anaconda,

```
conda env create -f environment.yml
conda activate prb
```

Install blender:

```
wget https://download.blender.org/release/Blender2.83/blender-2.83.2-linux64.tar.xz
tar xf blender-2.83.2-linux64.tar.xz
echo $PWD > $(echo blender*/2.*/python/lib/python*/site-packages/)clevr.pth
rm blender-2.83.2-linux64.tar.xz
```

Example: Run `./test.sh`.

For the original readme, see [README-clevr.md](README-clevr.md) and [README-ibm.md](README-ibm.md).
=
<div align="center">
  <img src="example/image/CLEVR_new_010000.png" width="800px">
</div>

# Functionality

+ `render_images.py` : 
  
  Renders random scenes using Blender and stores them into a result directory.
  The directory contains images and metadata.
  This file must be run in the python environment shipped with Blender.

+ `generate-dataset.sh` :

  Render the dataset. Options are ```[number of objects] [number of transitions] [number of images per transition] [number of jobs] [use gpu?]```. Example run:
  ```./generate-dataset.sh 5 10 3 1 true``` 


+ `generate-and-visualize.sh` :

  Test out the dataset generator. Creates visualization for generated bounding boxes and scene graphs.

# Running

To generate 10 transitions with 5 objects each. For every state, there are 3 images and GPU is used:

    ./generate-dataset.sh 5 10 3 1 true

# Visualization

To visualize the generated ```.json``` file, the ```visualize_scene_graph.py``` file in the ```visualize``` folder can be used:

<div align="center">
  <img src="example/image/visualize_photo.png" width="500px">
</div>
<div align="center">
  <img src="example/image/Visualize.png" width="500px">
</div>


# Citation

``` bibtex
@article{asai2018blocksworld,
	author = {Asai, Masataro},
	journal = {arXiv preprint arXiv:1812.01818},
	title = {{Photo-Realistic Blocksworld Dataset}},
	year = {2018}
}
```

Relevant citations:

``` bibtex
@article{asai2018perminv,
	author = {Asai, Masataro},
	journal = {arXiv preprint arXiv:1812.01217},
	title = {{Set Cross Entropy: Likelihood-based Permutation Invariant Loss Function for Probability Distributions}},
	year = {2018}
}
```

``` bibtex
@inproceedings{asai2019unsupervised,
  title={Unsupervised grounding of plannable first-order logic representation from images},
  author={Asai, Masataro},
  booktitle={Proceedings of the International Conference on Automated Planning and Scheduling},
  volume={29},
  pages={583--591},
  year={2019}
}
```



This repository is based on the clevr-dataset-gen software created by Facebook, Inc.
Copyright (c) 2017-present, Facebook, Inc. All rights reserved.
Licensed under the BSD-3-Clause License. See the LICENSE file for details.

