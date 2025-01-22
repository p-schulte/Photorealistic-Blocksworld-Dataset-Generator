# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import print_function
import sys, argparse, json, os

INSIDE_BLENDER = True
try:
  import bpy, bpy_extras
  from mathutils import Vector
except ImportError as e:
  INSIDE_BLENDER = False
if INSIDE_BLENDER:
  try:
    import utils
    import blocks
    from blocks import State, Unstackable, load_colors
    from render_utils import render_scene
  except ImportError as e:
    print("\nERROR")
    print("Running render_images.py from Blender and cannot import utils.py.")
    print("You may need to add a .pth file to the site-packages of Blender's")
    print("bundled python with a command like this:\n")
    print("echo $PWD >> $BLENDER/$VERSION/python/lib/python3.5/site-packages/clevr.pth")
    print("\nWhere $BLENDER is the directory where Blender is installed, and")
    print("$VERSION is your Blender version (such as 2.78).")
    sys.exit(1)

def initialize_parser():
  parser = argparse.ArgumentParser()

  # Input options
  blocks.initialize_parser_input_options(parser)

  # Environment options
  blocks.initialize_parser_environment_options(parser)

  # Output settings
  blocks.initialize_parser_output_options(parser,prefix='CLEVR')

  parser.add_argument('--start-idx', default=0, type=int,
                      help="The index at which to start for numbering rendered images. Setting " +
                      "this to non-zero values allows you to distribute rendering across " +
                      "multiple machines and recombine the results later.")

  parser.add_argument('--num-transitions', default=100, type=int,
                      help="The number of transitions to render")

  parser.add_argument('--num-samples-per-state', default=3, type=int,
                      help="The number of images to render per logical states")

  parser.add_argument('--num-steps', default=1, type=int,
                      help="The number of steps to perform from the source state")

  # Rendering options
  blocks.initialize_parser_rendering_options(parser)

  return parser

""" ORIGINAL VERSION
def path(dir,i,presuc,j,ext):
  if isinstance(i, int):
    i = "{:06d}".format(i)
  if isinstance(j, int):
    j = "{:03d}".format(j)
  return os.path.join(args.output_dir,dir,"_".join(["CLEVR",i,presuc,j])+"."+ext)
"""

def path(dir,i,name,j,ext):
  if isinstance(i, int):
    i = "{:06d}".format(i)
  if isinstance(j, int):
    j = "{:03d}".format(j)
  os.makedirs(os.path.join(args.output_dir,"image_tr",i), exist_ok=True)
  os.makedirs(os.path.join(args.output_dir,"scene_tr",i), exist_ok=True)
  return os.path.join(args.output_dir,dir,i,"_".join(["CLEVR",name,j])+"."+ext)


def main(args):
  import copy
  load_colors(args)

  os.makedirs(os.path.join(args.output_dir,"image_tr"), exist_ok=True)
  os.makedirs(os.path.join(args.output_dir,"scene_tr"), exist_ok=True)

  print("rendering images")
  for i in range(args.start_idx,
                 args.start_idx+args.num_transitions):

    while True:
      try:
        # by default, save the noiseless states into json.
        # if we want to extend the number of samples, load these fils and performs a wiggle.
        if os.path.exists(path("scene_tr",i,"pre","---","json")):
          assert os.path.exists(path("scene_tr",i,"suc","---","json"))
          print("base scene available; loading scene")
          with open(path("scene_tr",i,"pre","---","json"),"r") as f:
            pre = State.undump(json.load(f))
          with open(path("scene_tr",i,"suc","---","json"),"r") as f:
            suc = State.undump(json.load(f))
        else:
          assert not os.path.exists(path("scene_tr",i,"suc","---","json"))
          print("base scene not found; creating a new scene")
          pre = State(args)
          suc = copy.deepcopy(pre)
          for j in range(args.num_steps):
            suc.random_action()

          with open(path("scene_tr",i,"pre","---","json"),"w") as f:
            json.dump(pre.dump(),f,indent=2)
            f.truncate()
          with open(path("scene_tr",i,"suc","---","json"),"w") as f:
            json.dump(suc.dump(),f,indent=2)
            f.truncate()
          # print("dump success: ", json.dumps(pre.dump(),indent=2))
          # print("loading")
          # with open(path("scene_tr",i,"pre","---","json"),"r") as f:
          #   pre2 = State.undump(json.load(f))
          # with open(path("scene_tr",i,"suc","---","json"),"r") as f:
          #   suc2 = State.undump(json.load(f))
          # print("loaded data: ", json.dumps(pre.dump(),indent=2))
          #
          # 1/0


        # --------------   OLD VERSION -----------------
        '''
        for j in range(args.num_samples_per_state):
          if os.path.exists(path("image_tr",i,"pre",j,"png")):
            continue
          state = copy.deepcopy(pre)
          state.wiggle()
          render_scene(args,
                       output_image = path("image_tr",i,"pre",j,"png"),
                       output_scene = path("scene_tr",i,"pre",j,"json"),
                       objects      = state.for_rendering())

        for j in range(args.num_samples_per_state):
          if os.path.exists(path("image_tr",i,"suc",j,"png")):
            continue
          state = copy.deepcopy(suc)
          state.wiggle()
          render_scene(args,
                       output_image = path("image_tr",i,"suc",j,"png"),
                       output_scene = path("scene_tr",i,"suc",j,"json"),
                       objects      = state.for_rendering(),
                       action       = state.last_action)
        '''
        # --------------   OLD VERSION -----------------
        WIGGLE_BETWEEN_IMAGES = True

        for j in range(args.num_samples_per_state):
          if os.path.exists(path("image_tr",i,"pre",j,"png")):
            continue
          state = compute_intermediate_state(pre, suc, j, args.num_samples_per_state-1)
          if WIGGLE_BETWEEN_IMAGES:
            state.wiggle()
          render_scene(args,
                       output_image = path("image_tr",i,"image",j,"png"),
                       output_scene = path("scene_tr",i,"annotation",j,"json"),
                       objects      = state.for_rendering())

        """
        for j in range(args.num_samples_per_state):
          if os.path.exists(path("image_tr",i,"suc",j,"png")):
            continue
          state = copy.deepcopy(suc)
          state.wiggle()
          render_scene(args,
                       output_image = path("image_tr",i,"suc",j,"png"),
                       output_scene = path("scene_tr",i,"suc",j,"json"),
                       objects      = state.for_rendering(),
                       action       = state.last_action)
        """
          
          



        break
      except Unstackable as e:
        print(e)
        pass

def compute_midpoint(initial, goal, fraction):
    if not (0 <= fraction <= 1):
        raise ValueError("Percentage must be between 0 and 1.")

    # Interpolate between start and end positions
    current_position = list(initial[i] + fraction * (goal[i] - initial[i]) for i in range(3))
    return current_position

def compute_intermediate_state(initial, goal, step, num_steps):
  import copy
  res = copy.deepcopy(initial)

  # calc fraction of movement
  frac = step/float(num_steps)
  for o_id, object in enumerate(res.objects):
    # get current position
    initial_pos = object.location

    # get final position
    final_pos = goal.objects[o_id].location

    # calculate intermediate position
    new_pos = compute_midpoint(initial_pos, final_pos, frac)
    object.location = new_pos

  return res


if __name__ == '__main__':
  parser = initialize_parser()
  if INSIDE_BLENDER:
    # Run normally
    argv = utils.extract_args()
    args = parser.parse_args(argv)
    main(args)
  elif '--help' in sys.argv or '-h' in sys.argv:
    parser.print_help()
  else:
    print('This script is intended to be called from blender like this:')
    print()
    print('blender --background --python render_images.py -- [args]')
    print()
    print('You can also run as a standalone python script to view all')
    print('arguments like this:')
    print()
    print('python render_images.py --help')

