#!/bin/bash

echo "this test will just render the first 5 images of 2 objs, 2 stacks blocksworld."
read -n 1 -s -r -p "Press any key to continue"

blenderdir=$(echo blender-2.*/)
$blenderdir/blender -noaudio --background --python render_images.py -- \
      --output-dir      output                          \
      --use-gpu 1                                       \
      --render-num-samples 50                           \
      --start-idx          0                            \
      --width 300                                       \
      --height 200                                      \
      --num-objects 4                                   
#      --num-images         5                           \
#      --num-transitions         5                           \


# ./extract_region.py output/scenes/CLEVR_new_000000_pre.json
# ./extract_region.py output/scenes/CLEVR_new_000000_suc.json
