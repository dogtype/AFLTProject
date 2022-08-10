from fgglib.fgg.fgg import FGG

class Visualization:
              
    def draw(self, graph):         
        import pygraphviz as pgv         
        """ returns a png image of the graph """         
        G, filename = self.visualize(graph)         
        G.layout(prog="neato") # one of: neato|dot|twopi|circo|fdp|nop         
        filename+=".png"         
        return G.draw(filename)      
    
    def visualize(self,graph):
        import pygraphviz as pgv    
        G = pgv.AGraph(strict = False, directed = False)   
        filename = ""           
        if isinstance(graph,FGG):           
            filename = "FGG"        
            for p in  graph.P:      
                body = p.body        
                for e in body.E:       
                    G.add_node(e.label,shape="circle")       
                    for v in body.V:                
                        G.add_node(v.label,shape="box")       
        else:        
            filename = "Graph"     
            for v in graph.V:           
                G.add_node(v.label,shape="circle")     
                for e in graph.E:        
                    G.add_node(e.label,shape="box", color ="red")    
                    for e in graph.E:         
                        for v in e.targets:    
                            G.add_edge(e.label, v.label, color = "black")
        
        G.graph_attr["label"] = filename  
        G.node_attr["color"] = "black"     
        return G, filename