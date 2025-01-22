import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis import network as pvnet


def rgba_to_hex(color):
    """
    Convert an RGBA color with values in [0, 1] range to a HEX color string.

    Args:
        color (list): A list of four floats [R, G, B, A] where each value is in the range [0, 1].

    Returns:
        str: HEX color string in the format #RRGGBB.
    """
    r, g, b, _ = color  # Ignore the alpha channel
    return '#{:02x}{:02x}{:02x}'.format(
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )

def create_scene_graph(data):
    """
    Create a scene graph as a dictionary from the given data.

    Args:
        data (dict): Parsed JSON data containing object and relationship information.

    Returns:
        dict: Scene graph represented as a dictionary.
    """
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

def visualize_matplotlib(scene_graph):
    """
    Visualize the scene graph using NetworkX and Matplotlib as a multigraph.

    Args:
        scene_graph (dict): Scene graph represented as a dictionary.
    """
    G = nx.MultiDiGraph()

    # Add nodes with attributes
    for node_id, attributes in scene_graph["nodes"].items():
        label = f"{attributes['shape']}\n{attributes['color']}\n{attributes['material']}"
        G.add_node(node_id, label=label, color=attributes['color'])

    # Add edges with multiple relationships
    for source, target, relationship in scene_graph["edges"]:
        G.add_edge(source, target, label=relationship)

    # Generate positions with more spacing to reduce overlap
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Increase `k` for more spacing

    # Draw nodes with specific colors
    node_colors = [G.nodes[node]['color'] for node in G.nodes]
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=10,
        edgecolors='black',
    )

    # Draw edge labels (relationships between nodes)
    edge_labels = {}
    for source, target, key, data in G.edges(keys=True, data=True):
        edge_labels[(source, target, key)] = data['label']

    # Place edge labels with less overlap
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.6
    )

    # Draw edges with arrows
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, arrowstyle='->', arrowsize=20)

    plt.title("Scene Graph (Multigraph)")
    plt.show()




import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


def create_annotations_and_display_image(json_data, png_file):
    """
    Creates bounding boxes for the objects and overlays them on a PNG file.

    Parameters:
    objects (dict): Object data containing 'location' and 'size' attributes.
    png_file (str): Path to the rendered image file (PNG format).
    image_width (int): Width of the rendered image.
    image_height (int): Height of the rendered image.
    """
    # Open the PNG file
    try:
        img = Image.open(png_file)
    except FileNotFoundError:
        print(f"Error: File '{png_file}' not found.")
        return

    # Define the figure and axis
    fig, ax = plt.subplots(1)
    ax.imshow(img)

    objects = json_data["objects"]
    for obj_id, obj in enumerate(objects):
        color = obj["color"][:3]    # Use RGB values for the bounding box color

        # Define bounding box coordinates
        xmin = obj["bbox"][0]
        ymin = obj["bbox"][1]
        xmax = obj["bbox"][2]
        ymax = obj["bbox"][3]

        # Create a rectangle for the bounding box
        rect = patches.Rectangle(
            (xmin, ymin),  # Bottom-left corner
            xmax - xmin,   # Width
            ymax - ymin,   # Height
            linewidth=2,
            edgecolor=color,
            facecolor='none'
        )
        ax.add_patch(rect)

        # Add object ID as a label
        ax.text(
            xmin,
            ymin - 0,  # Position label slightly above the bounding box
            f"{obj_id}",
            color='white',
            fontsize=10,
            ha='left',
            bbox=dict(facecolor='black', edgecolor='none', alpha=0.4)
        )

    # Display the image
    plt.axis('off')
    plt.show()







def visualize_scene_graph(scene_graph):
    """
    Visualize the scene graph using NetworkX and Matplotlib as a multigraph.

    Args:
        scene_graph (dict): Scene graph represented as a dictionary.
    """
    G = nx.MultiDiGraph()

    # Add nodes with attributes
    for node_id, attributes in scene_graph["nodes"].items():
        label = f"{attributes['shape']}\n{attributes['color']}\n{attributes['material']}"
        G.add_node(node_id, label=str(node_id), color=rgba_to_hex(attributes['color']))

    # Add edges with multiple relationships
    for source, target, relationship in scene_graph["edges"]:
        G.add_edge(source, target, label=relationship)

    name = 'output/visualize_scene_graph_output.html'
    g = G.copy()  # Some attributes added to nodes
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
    
    # Uncomment this to play with layout
    # net.show_buttons(filter_=['physics'])

    net.from_nx(g)

    return net.show(name)

import sys
import pprint

JSONFILE="test.json"
IMAGEFILE="test.png"

# Example usage
if __name__ == "__main__":
    # Check if a filename is provided as a command-line argument
    if len(sys.argv) > 1:
        JSONFILE = sys.argv[1]

    if len(sys.argv) > 2:
        IMAGEFILE = sys.argv[2]

    # Read JSON data from file
    try:
        with open(JSONFILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{JSONFILE}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{JSONFILE}'.")
        sys.exit(1)

    # Create the scene graph
    scene_graph = create_scene_graph(data)

    # Print the nicely formatted dictionary
    pprint.pprint(scene_graph['edges'])
    pprint.pprint(scene_graph['nodes'])

    # Visualize the scene graph
    visualize_scene_graph(scene_graph)

    # Visualize bounding boxes
    #visualize_bounding_boxes(scene_graph['nodes'], IMAGEFILE)
    create_annotations_and_display_image(data, IMAGEFILE)