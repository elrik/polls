$(document).ready(function() {
  generateGraph();

  bindSocket();
});

function generateGraph() {
  if ($("div.graph.generate-graph").length > 0) {
    var graph = c3.generate({
      bindto: 'div.graph.generate-graph',
      data: {
        columns: window.__initialGraphData__.data,
        type: 'donut',
      },
      donut: {
        'title': window.__initialGraphData__.title,
        'label': {
          'show': true,
          format: function (value, ratio, id) {
            return d3.format('')(value);
          }
        },
      },
    });

    $('div.graph.generate-graph').data('graph', graph);
  }
}

function bindSocket() {
  socket = new WebSocket("ws://" + window.location.host + window.location.pathname);
  socket.onmessage = function(e) {
      alert(e.data);
    console.log(e)
    xxx = e
  }
  socket.onopen = function() {
    console.log("fooo")
    //socket.send("hello world");
  }
  // Call onopen directly if socket is already open
  if (socket.readyState == WebSocket.OPEN) socket.onopen();
}