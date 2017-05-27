"use strict";

window.onload=function(){
  window.__app__ = new Vue({
    delimiters: ["[[", "]]"],
    el: '#appResult',

    data: {
      object: {},
      answers: [],
    },

    beforeCreate: function () {
      var objectId = document.getElementById('appResult').dataset.objectId;
      var app = this;
      app.objectId = objectId;
    },
    created: function () {
      this.fetchObject();
      this.csrfToken = this.getCookie('csrftoken');
    },

    methods: {
      getCookie: function(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
      },
      'fetchObject': function () {
        var app = this;
        if (app.objectId) {
          var url = "/api/questions/" + app.objectId + "/";
          fetch(url, {credentials: 'include'}).then(function (response) {
            return response.json()
          }).then(function (object) {
            console.log(object);
            app.object = object;
            app.answers = object.answers;
            document.getElementById('appResult').classList.remove('hide');
          });
        } else {
          document.getElementById('appResult').classList.remove('hide');
        }
      },
      handleSocketMessage: function(message) {
        console.log(message, message.question, message.answers);
        var app = this;
        app.object = message.question;
        app.answers = message.question.answers;
        var graph = $('div.graph.generate-graph').data('graph');
        var graphData = message.question.answers.map(function(i) {return [i.answer_text, i.votes] });
        graph.unload();
        graph.load({
          'columns': graphData,
        });
      }
    },
  });
}