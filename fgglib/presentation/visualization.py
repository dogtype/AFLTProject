from fgglib.fgg.fgg import FGG

class Visualization:
              
    def draw(self, graph, name=None):         
        import pygraphviz as pgv         
        """ returns a png image of the graph """                 
        G, filename = self.visualize(graph,name)
        G.layout(prog="neato") # one of: neato|dot|twopi|circo|fdp|nop         
        filename="./fgglib/presentation/images/"+str(filename)+".png"   
        return G.draw(filename)
    
    def visualize(self,graph, name):
        import pygraphviz as pgv    
        G = pgv.AGraph(strict = False, directed = False)   
        name = str(name)
        if isinstance(graph,FGG):                       
            if str(name) == "None": name = "FGG"
            for p in  graph.P:      
                body = p.body        
                for e in body.E:       
                    G.add_node(e.label,shape="circle")       
                for v in body.V:                
                    G.add_node(v.label,shape="box")    
                for v in e.targets:    
                    G.add_edge(e.label, v.label, color = "black")        
        else:        
            if str(name) == "None": name = "Grammar"
            for v in graph.V:           
                G.add_node(v.label,shape="circle")     
            for e in graph.E:        
                G.add_node(e.label,shape="box", color ="red")    
                for tgt in e.targets:    
                    G.add_edge(e.label, tgt.label, color = "black")                                            
        G.graph_attr["label"] = name  
        G.node_attr["color"] = "black"     
        return G, name