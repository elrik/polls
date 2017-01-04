$(document).ready(function() {
  if ($("div.graph.generate-graph").length > 0) {
    generateGraph();
  }

  if ($("form.socket-form").length > 0) {
    bindSocketForm();
  }

  bindSocket();
});

function generateGraph() {
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

function bindSocket() {
  socket = new ReconnectingWebSocket("ws://" + window.location.host + window.location.pathname);
  socket.onmessage = function(e) {
    var data = $.parseJSON(e.data);

    xxx = data
    yyy = e

    if (data.action == "update-results") {
      updateResults(data);
    } else if (data.action == "vote") {
      voteEvent(data);
    } else if (data.action == "update-poll") {
      pollUpdateEvent(data);
    }
  }

  socket.onopen = function(e) {
    socket.send("update");
  }
  // Call onopen directly if socket is already open
  if (socket.readyState == WebSocket.OPEN) socket.onopen();
}

function updateResults(data) {
  console.log(data);
  var graph = $('div.graph.generate-graph').data('graph');

  graph.load({
    'columns': data.answer_graph_data,
  });

  for (var idx in data.answers) {
    var answer = data.answers[idx]
    $("p.votes#answer-id-" + answer.id).text(answer.votes);
  }
}

function voteEvent(data) {
  if (data.status == "ok") {
    window.location.href = data.redirect_url;
  } else {
    alert("Error submiting vote form");
  }
}

function bindSocketForm() {
  $("form.socket-form").submit(function(event) {
    event.preventDefault();

    var $this = $(this);
    var formData = $this.serializeArray();
    var action = $this.data('action');

    action = action ? action : "vote";


    data = {}
    formData.map(function(x){data[x.name] = x.value;})

    socket.send(JSON.stringify(
      {
        action: action,
        data: data,
      }
    ));

    return false;
  });
}


function pollUpdateEvent(data) {
  if (data.status == "success") {
    $("#poll-question").text(data.poll.question);
  }
}
