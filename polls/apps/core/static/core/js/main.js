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
    var data = $.parseJSON(e.data);
    var graph = $('div.graph.generate-graph').data('graph');

    console.log(data);

    graph.load({
      'columns': data.answer_graph_data,
    });

    for (var idx in data.answers) {
      var answer = data.answers[idx]
      $("p.votes#answer-id-" + answer.id).text(answer.votes);
    }

  }

  socket.onopen = function() {}
  // Call onopen directly if socket is already open
  if (socket.readyState == WebSocket.OPEN) socket.onopen();
}