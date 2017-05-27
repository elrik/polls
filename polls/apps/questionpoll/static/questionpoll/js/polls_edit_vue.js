"use strict";

window.onload=function(){
  window.__app__ = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',

    data: {
      object: {
      },
      answers: [],
      newText: "",
      editedAnswer: null,
      editedObject: null,

    },

    beforeCreate: function () {
      var objectId = document.getElementById('app').dataset.objectId;
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
            document.getElementById('app').classList.remove('hide');
          });
        } else {
          document.getElementById('app').classList.remove('hide');
        }
      },
      editAnswer: function(answer) {
        var app = this;
        console.log("Editing answer");
        app.editedAnswer = answer;
      },
      saveAnswer: function() {
        var vm = this;
        alert("Saving answer");
      },
      saveQuestion: function() {
        var vm = this;
        alert("Saving question");
      },
      addAnswer: function(text) {
        var app = this;
        if (text) {
          var url = "http://localhost:8001/api/answers/";
          fetch(url, {
            credentials: 'include',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CsrfToken': app.csrfToken,
            },
            method: "POST",
            body: JSON.stringify({
              "question": app.objectId,
              "answer_text": text,
            }),
          }).then(function (response) {
            return response.json()
          }).then(function (object) {
            console.log(object);
            app.answers.push(object);
            app.newText = "";
          });
        }
      },
      updateAnswer: function(answer) {
        var app = this;
        console.log("Saving", answer, app.editedAnswer)
        if (answer == app.editedAnswer) {
          var url = "http://localhost:8001/api/answers/" + answer.id + "/";
          fetch(url, {
            credentials: 'include',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CsrfToken': app.csrfToken,
            },
            method: "PATCH",
            body: JSON.stringify(answer),
          }).then(function (response) {
            return response.json()
          }).then(function (object) {
            console.log(object);
            answer = object;
            app.editedAnswer = null;
          });
        }
      },
      deleteAnswer: function(answer) {
        var app = this;
        console.log("Removing answer", answer)
        if (answer) {
          var url = "http://localhost:8001/api/answers/" + answer.id + "/";
          fetch(url, {
            credentials: 'include',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CsrfToken': app.csrfToken,
            },
            method: "DELETE",
          }).then(function (response) {
            app.answers = app.answers.filter(function(item) {
              return item.id != answer.id;
            });
            console.log(response);
          });
        }
      },
    },
  });
}