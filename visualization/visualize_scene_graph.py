import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis import network as pvnet

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

import sys
import pprint

import os
from pathlib import Path

JSONFILE="test.json"
IMAGEFILE="test.png"


def rgba_to_hex(color):
    r, g, b, _ = color  # Ignore the alpha channel
    return '#{:02x}{:02x}{:02x}'.format(
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )

def create_scene_graph(data):
    scene_graph = {"nodes": {}, "edges": []}

    # Add objects as nodes
    for obj in data["objects"]:
        scene_graph["nodes"][obj["id"]] = {
            "shape": obj["shape"],
            "color": obj["color"],
            "size": obj["size"],
            "material": obj["material"],
            "stackable": obj["stackable"],
            "location": obj["location"],
        }

    # Add relationships as edges
    for relationship, objects in data["relationships"].items():
        for obj_id, related_ids in enumerate(objects):
            for related_id in related_ids:
                scene_graph["edges"].append((obj_id, related_id, relationship))

    return scene_graph

def visualize_scene_graph_pygraphviz(scene_graph, output_file="sg_output.png"):
    # Create a directed graph
    A = nx.MultiDiGraph()

    # Add nodes with attributes
    for node_id, attributes in scene_graph["nodes"].items():
        A.add_node(
            node_id,
            label=f"{node_id}",
            color=rgba_to_hex(attributes['color']),
            style="filled",
            fillcolor=rgba_to_hex(attributes['color']),
        )

    # Add edges with labels for relationships
    for source, target, relationship in scene_graph["edges"]:
        A.add_edge(source, target, label=relationship)

    graph = nx.nx_agraph.to_agraph(A)
    graph.layout(prog="dot")
    graph.draw(output_file)

def create_annotations_png(json_data, png_file, output_file="bbox_output.png"):
    try:
        img = Image.open(png_file)
    except FileNotFoundError:
        print(f"Error: File '{png_file}' not found.")
        return

    fig, ax = plt.subplots(1)
    ax.imshow(img)

    objects = json_data["objects"]
    for obj_id, obj in enumerate(objects):
        color = obj["color"][:3]    # Use RGB values for the bounding box color

        xmin = obj["bbox"][0]
        ymin = obj["bbox"][1]
        xmax = obj["bbox"][2]
        ymax = obj["bbox"][3]

        rect = patches.Rectangle(
            (xmin, ymin),  # Bottom-left corner
            xmax - xmin,   # Width
            ymax - ymin,   # Height
            linewidth=2,
            edgecolor=color,
            facecolor='none'
        )
        ax.add_patch(rect)
        ax.text(
            xmin,
            ymin - 0,  # Position label slightly above the bounding box
            f"{obj_id}",
            color='white',
            fontsize=10,
            ha='left',
            bbox=dict(facecolor='black', edgecolor='none', alpha=0.4)
        )
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    #plt.show()



def visualize_scene_graph_pyviz(scene_graph):
    G = nx.MultiDiGraph()

    for node_id, attributes in scene_graph["nodes"].items():
        label = f"{attributes['shape']}\n{attributes['color']}\n{attributes['material']}"
        G.add_node(node_id, label=str(node_id), color=rgba_to_hex(attributes['color']))

    for source, target, relationship in scene_graph["edges"]:
        G.add_edge(source, target, label=relationship)

    name = 'output/visualize_scene_graph_pyviz_output.html'
    g = G.copy()
    net = pvnet.Network(notebook=True, directed=True)

    opts = """
    {
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -100,
                "centralGravity": 0.11,
                "springLength": 100,
                "springConstant": 0.09,
                "avoidOverlap": 1
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based",
            "timestep": 0.22
        },
        "manipulation": {
            "enabled": true,
            "dragNode": true,
            "zoomSpeed": 0.1,
            "zoomView": true
        }
    }
    """

    net.set_options(opts)
    net.from_nx(g)
    return net.show(name)


def process_images_and_jsons(image_dir, json_dir, output_dir="visualization_output"):
    """
    Process all PNG and JSON file pairs from the given directories, generating annotated images and scene graphs.

    Parameters:
    image_dir (str): Directory containing PNG files.
    json_dir (str): Directory containing JSON files.
    output_dir (str): Directory to save the annotated images and scene graphs.
    """
    os.makedirs(output_dir, exist_ok=True)
    image_files = sorted(Path(image_dir).glob("*.png"))
    json_files = sorted(Path(json_dir).glob("*.json"))

    if not image_files or not json_files:
        print("No PNG or JSON files found in the specified directories.")
        return

    for img_file, json_file in zip(image_files, json_files):

        try:
            with open(json_file, "r") as file:
                data = json.load(file)

            annotated_image_path = os.path.join(output_dir, f"annotated_{img_file.stem[-3:]}.png")
            scene_graph_path = os.path.join(output_dir, f"scene_graph_{img_file.stem[-3:]}.png")
            create_annotations_png(data, img_file, output_file=annotated_image_path)
            scene_graph = create_scene_graph(data)
            visualize_scene_graph_pygraphviz(scene_graph, output_file=scene_graph_path)
            print(f"Processed {img_file.name} and {json_file.name} -> Saved to {output_dir}")
        except Exception as e:
            print(f"Error processing {img_file.name} and {json_file.name}: {e}")


def process_folder():
    image_directory = "cylinders-6/image_tr/000000/"
    json_directory = "cylinders-6/scene_tr/000000/"
    output_directory = "visualization_output"
    process_images_and_jsons(image_directory, json_directory, output_directory)

def visualize_test():
    if len(sys.argv) > 1:
        JSONFILE = sys.argv[1]

    if len(sys.argv) > 2:
        IMAGEFILE = sys.argv[2]

    try:
        with open(JSONFILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{JSONFILE}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{JSONFILE}'.")
        sys.exit(1)

    scene_graph = create_scene_graph(data)

    pprint.pprint(scene_graph['edges'])
    pprint.pprint(scene_graph['nodes'])

    visualize_scene_graph_pyviz(scene_graph)
    visualize_scene_graph_pygraphviz(scene_graph)
    create_annotations_png(data, IMAGEFILE)

if __name__ == "__main___":
    if len(sys.argv) > 1:
        visualize_test()
    else:
        process_folder