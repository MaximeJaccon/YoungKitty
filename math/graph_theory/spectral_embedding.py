from manim import *
import networkx as nx
import numpy as np
from scipy.spatial import Delaunay

class SpectralSpringEmbedding(Scene):
    def construct(self):
        num_points = 1000 
        points = np.random.rand(num_points, 2)
        
        try:
            tri = Delaunay(points)
        except Exception as e:
            print(f"Error in Delaunay triangulation: {e}")
            return
        
        G = nx.Graph()
        G.add_nodes_from(range(len(points)))
        for simplex in tri.simplices:
            G.add_edges_from([(simplex[i], simplex[j]) for i in range(3) for j in range(i+1, 3)])
        
        pos_initial = {i: points[i] for i in range(len(points))}
        
        L = nx.laplacian_matrix(G).astype(float)
        eigenvalues, eigenvectors = np.linalg.eigh(L.toarray())
        X_spectral = eigenvectors[:, 1:3]
        pos_spectral = {i: X_spectral[i] for i in range(len(G.nodes))}
        
        pos_final = nx.spring_layout(G, pos=pos_spectral, fixed=None, seed=42)

        pos_initial = self.center_and_spread(pos_initial)
        pos_spectral = self.center_and_spread2(pos_spectral)
        pos_final = self.center_and_spread(pos_final)

        graph_initial = self.create_graph(G, pos_initial)
        graph_spectral = self.create_graph(G, pos_spectral)
        graph_final = self.create_graph(G, pos_final)

        self.play(Create(graph_initial))
        self.wait(1)

        self.play(
            ReplacementTransform(
                graph_initial, 
                graph_spectral,
                path_func=utils.paths.path_along_arc(PI/2),
                run_time=2
            )
        )
        self.wait(2)
      
    def center_and_spread(self, pos):
        positions = np.array(list(pos.values()))
        center = np.mean(positions, axis=0)
        positions_centered = positions - center
        
        scale_factor = 5.0 
        positions_spread = positions_centered * scale_factor
        
        return {i: positions_spread[i] for i in range(len(pos))}
    
    def center_and_spread2(self, pos):
        positions = np.array(list(pos.values()))
        
        center = np.mean(positions, axis=0)
        positions_centered = positions - center

        scale_factor = 50.0 
        positions_spread = positions_centered * scale_factor
        
        # Convert back to a dictionary
        return {i: positions_spread[i] for i in range(len(pos))}

    def create_graph(self, G, pos):
        vertices = list(G.nodes)
        edges = list(G.edges)
        
        pos_3d = {k: np.array([v[0], v[1], 0.0]) for k, v in pos.items()}
        
        return Graph(
            vertices,
            edges,
            layout=pos_3d,
            vertex_config={
                "radius": 0.01,          
                "fill_color": WHITE, 
                "stroke_color": WHITE, 
                "stroke_width": 0.5       
            },
            edge_config={
                "stroke_color": WHITE,
                "stroke_width": 0.5,      
                "stroke_opacity": 1.0
            }
        )
