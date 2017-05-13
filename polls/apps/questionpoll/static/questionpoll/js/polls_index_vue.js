"use strict";

window.onload=function(){
  window.__app__ = new Vue({
    el: '#pollsApp',

    data: {
      greeting: 'Welcome to polls app!',
      polls: [],

    },

    created: function () {
      document.getElementById('pollsApp').classList.remove('hide');
      this.fetchPolls();
    },

    methods: {
      'fetchPolls': function () {
        console.log("Fetching polls");
        var app = this;
        fetch('/api/polls_index', {credentials: 'include'}).then(function (response) {
          return response.json()
        }).then(function (polls) {
          console.log(polls);
          app.polls = polls;
        })
      },
      greet: function() {
        var vm = this;
        vm.greeting = "Test";
      }
    },
  });
}