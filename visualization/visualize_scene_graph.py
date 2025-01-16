import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis import network as pvnet

# CONSTS:
FILENAME = "test.json"

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
        G.add_node(node_id, label=str(node_id), color=attributes['color'])

    # Add edges with multiple relationships
    for source, target, relationship in scene_graph["edges"]:
        G.add_edge(source, target, label=relationship)

    name='out.html'
    g = G.copy() # some attributes added to nodes
    net = pvnet.Network(notebook=True, directed=True)
    opts = '''
        var options = {
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
          }
        }
    '''

    net.set_options(opts)
    # uncomment this to play with layout
    # net.show_buttons(filter_=['physics'])
    net.from_nx(g)
    return net.show(name)

def visualize_2(scene_graph):
    """
    Visualize the scene graph using NetworkX and Matplotlib as a multigraph.

    Args:
        scene_graph (dict): Scene graph represented as a dictionary.
    """
    G = nx.MultiDiGraph()

    # Add nodes with attributes
    for node_id, attributes in scene_graph["nodes"].items():
        label = f"{attributes['shape']}\n{attributes['color']}\n{attributes['material']}"
        G.add_node(node_id, label=str(node_id), color=attributes['color'])

    # Add edges with multiple relationships
    for source, target, relationship in scene_graph["edges"]:
        G.add_edge(source, target, label=relationship)

    name = 'out2.html'
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



# Example usage
if __name__ == "__main__":
    # Read JSON data from file
    with open(FILENAME, "r") as file:
        data = json.load(file)

    # Create the scene graph
    scene_graph = create_scene_graph(data)
    
    # Prints the nicely formatted dictionary
    import pprint
    pprint.pprint(scene_graph)

    # Visualize the scene graph
    visualize_scene_graph(scene_graph)
    visualize_2(scene_graph)
