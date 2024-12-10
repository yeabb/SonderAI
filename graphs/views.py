from django.shortcuts import render
from django.http import HttpResponse
from sonderPyvis.network import Network

    
def constructGraph(request):
    net = Network(neighborhood_highlight=True)
    net.add_node(0, "a")
    net.add_node(1, "b")
    net.add_node(2, "c")
    net.add_node(3, "d")
    net.add_node(4, "e")
    net.add_node(5, "f")
    net.add_node(6, "g")
    net.add_node(7, "h")
    net.add_node(8, "i")
    net.add_node(9, "j")
    net.add_node(10, "k")
    net.add_node(11, "l")
    net.add_node(12, "m")
    net.add_node(13, "n")
    net.add_node(14, "o")
    net.add_node(15, "p")
    net.add_node(16, "q")
    net.add_node(17, "r")
    net.add_node(18, "s")
    net.add_node(19, "t")
    net.add_node(20, "u")
    net.add_node(21, "v")
    net.add_node(22, "w")
    net.add_node(23, "x")
    net.add_node(24, "y")
    net.add_node(25, "z")
    net.add_edge(0, 1)
    net.add_edge(0, 2)
    net.add_edge(0, 3)
    net.add_edge(4, 5)
    net.add_edge(5, 6)
    net.add_edge(4, 6)
    net.add_edge(6, 7)
    net.add_edge(8, 9)
    net.add_edge(8, 10)
    net.add_edge(10, 11)
    net.add_edge(11, 12)
    net.add_edge(13, 14)
    net.add_edge(14, 15)
    net.add_edge(15, 16)
    net.add_edge(14, 17)
    
    
    nodes, edges, heading, height, width, options = net.get_network_data()
    
    # print(net.cdn_resources)
    # return render(request, "basic_template.html", {"cdn_resources": "local"})
    # return HttpResponse("HI")
    
    return render(request, "template.jinja", {
        "height": height,
        "width": width,
        "nodes": nodes,
        "edges": edges,
        "heading": heading,
        "options": options,
        "physics_enabled": True,
        "use_DOT": net.use_DOT,
        "dot_lang": net.dot_lang,
        "widget": net.widget,
        "bgcolor": net.bgcolor,
        "conf": net.conf,
        "tooltip_link": False,
        "neighborhood_highlight": net.neighborhood_highlight,
        "select_menu": net.select_menu,
        "filter_menu": net.filter_menu,
        "notebook": False,
        "cdn_resources": net.cdn_resources
        }
    )

    