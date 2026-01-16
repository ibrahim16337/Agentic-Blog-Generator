from langgraph.graph import StateGraph, START, END
from src.llms.groq_llm import GroqLLM
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
        
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on the topic
        """
        ## Creating Blog Node
        self.blog_node_obj = BlogNode(self.llm)
        
        ## Add Nodes 
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        
        ## Add Edges
        self.graph.add_edge(START, "title_creation")  
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)
        
        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with topic and language inputs
        """
        ## Creating Blog Node
        self.blog_node_obj = BlogNode(self.llm)
        
        ## Add Nodes 
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        self.graph.add_node("urdu_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "urdu"}))        
        self.graph.add_node("french_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "french"}))
        self.graph.add_node("route", self.blog_node_obj.route)       
        
        ## Adding Edges
        self.graph.add_edge(START, "title_creation")  
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "urdu": "urdu_translation",
                "french": "french_translation"
            }
        )
        self.graph.add_edge("urdu_translation", END)
        self.graph.add_edge("french_translation", END)
        
        return self.graph
            
            
    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        if usecase == "language":
            self.build_language_graph()
            
        return self.graph.compile()
    
## Code for LangSmith LangGraph Studio
llm = GroqLLM().get_llm()

## Get Graph
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()