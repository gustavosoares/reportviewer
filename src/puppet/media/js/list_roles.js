function init() {
    
	var json = {{json|safe}};

     //Create a new canvas instance.
      var canvas = new Canvas('mycanvas', {
         //Where to inject canvas. Any HTML container will do.
         'injectInto':'infovis',
         //Set width and height, default's to 200.
         'width': 900,
         'height': 600,
         //Set a background color in case the browser
         //does not support clearing a specific area.
        'backgroundColor': '#1a1a1a'
      });
    //Create a new ST instance
    var st= new ST(canvas, {
	
	  duration: 800,
	  transition: Trans.QuarteaseInOut,
	  levelDistance: 50,
      //Set node and edge colors
      //Set overridable=true to be able
      //to override these properties
      //individually
       Node: {
           height: 20,
           width: 200,
           type: 'rectangle',
           color: '#aaa',
           overridable: true
       },

       Edge: {
           type: 'bezier',
           overridable: true
       },
    //Add an event handler to the node when creating it.
    onCreateLabel: function(label, node){
        label.id = node.id;            
        label.innerHTML = node.name;
        label.onclick = function(){
            st.onClick(node.id);
        };
        //set label styles
        var style = label.style;
        style.width = 60 + 'px';
        style.height = 17 + 'px';            
        style.cursor = 'pointer';
        style.color = '#333';
        style.fontSize = '0.8em';
        style.textAlign= 'center';
        style.paddingTop = '3px';
    },
        //This method is called right before plotting
        //a node. It's useful for changing an individual node
        //style properties before plotting it.
        //The data properties prefixed with a dollar
        //sign will override the global node style properties.
        onBeforePlotNode: function(node) {
            //add some color to the nodes in the path between the
            //root node and the selected node.
            if (node.selected) {
                node.data.$color = "#ff7";
            } else {
                delete node.data.$color;
            }
        },

        //This method is called right before plotting
        //an edge. It's useful for changing an individual edge
        //style properties before plotting it.
        //Edge data properties prefixed with a dollar sign will
        //override the Edge global style properties.
        onBeforePlotLine: function(adj){
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
                adj.data.$color = "#eed";
                adj.data.$lineWidth = 3;
            }
            else {
                delete adj.data.$color;
                delete adj.data.$lineWidth;
            }
        }
    });
    //load json data
    st.loadJSON(json);
    //compute node positions and layout
    st.geom.translate(new Complex(-200, 0), "startPos");
    //emulate a click on the root node.
    st.onClick(st.root);
}
