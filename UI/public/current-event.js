var socket = null

//Prepare scheduler
var app = new Vue({
    el: '#current-event',
    data: {
        connected: false,
        error: 'a',
        calendarEvents: JSON.parse(document.getElementById('calendars').innerHTML),
        event_info : JSON.parse(document.getElementById('event').innerHTML),
        test_data: [],
        group_data: [],
        startDate: '',
        endDate: '',
        current_group: '',
        options: [],
        selectedOption: '',
        renderDiv: true,
        renderFinalDiv: false,
        finalSavedTime: ''
    },
    mounted: function(){
        connect();
    },
    methods: {
        //For testing to see that your website is working
        test_app_runs(){
            socket.emit('Hello world!');
        },
        get_test_data(){
          return this.test_data;
        },
        get_group_data(){
          return this.group_data;
        },
        test_button(){
          socket.emit('TEST');
        },
        update_group_data(){
          for(let i =0; i<this.event_info['users'].length;i++){
            this.group_data.push({'id': ''+i+'', 'content':this.event_info['users'][i]});
          }
          this.options = this.event_info['suggestions'];
        },
        update_test_data(){
          for(let i =0; i<this.calendarEvents.length;i++){
            var startDate = this.calendarEvents[i]['startDate']['year']+'-'+this.calendarEvents[i]['startDate']['month']+'-'+this.calendarEvents[i]['startDate']['day']  + ' ' + this.calendarEvents[i]['startDate']['hour'] + ':' + this.calendarEvents[i]['startDate']['minutes'] + ':00';
            var endDate=this.calendarEvents[i]['endDate']['year']+'-'+this.calendarEvents[i]['endDate']['month']+'-'+this.calendarEvents[i]['endDate']['day']  + ' ' + this.calendarEvents[i]['endDate']['hour'] + ':' + this.calendarEvents[i]['endDate']['minutes'] + ':00';
            this.getIdByEmail(this.calendarEvents[i]['email']);
            this.test_data.push({'id': ''+i+'', 'start': startDate, 'end':endDate, 'group': this.current_group});
          }
        },
        getIdByEmail(target){
          for(let i =0; i<this.group_data.length;i++){
            if(this.group_data[i]['content']==target){
              this.current_group = this.group_data[i]['id'];
            }
          }
        },
        add_option(){
          // handle error cases when input is empty
          socket.emit('addOption', {'id': this.event_info['id'] ,'startDate': this.startDate, 'endDate': this.endDate});
          this.startDate= '';
          this.endDate= '';
        },
        update_users_voted(){
          socket.emit('updateUsersVoted', this.event_info['id']);
        },
        increment_vote(){
          socket.emit('incrementVote', {'id': this.event_info['id'] , 'suggestion': this.selectedOption});
        },
        sortedItems() {
          this.options= this.options.sort((a,b) => (a.content.votes > b.content.votes) ? -1 : 1)
        },
        save_event(){
          if(this.event_info['usersVoted'].length<this.event_info['users'].length){
            alert("Not all users have voted yet.");
          }else{
            this.renderDiv = false;
            var result = this.options.sort((a,b) => (a.content.votes > b.content.votes) ? -1 : 1)[0];
            this.finalSavedTime = result['content']['startDate'] + ' to ' + result['content']['endDate'];
            this.renderFinalDiv = true;
            socket.emit('saveFinalTime', {'users' : this.event_info.users ,'id' : this.event_info['id'], 'finalStartTime' : result['content']['startDate'], 'finalEndTime' : result['content']['endDate'], 'description' : this.event_info.description})
          }
        },
        update_votes(){
          for(let i =0; i<this.options.length;i++){
            if(this.options[i]['id']==this.selectedOption){
              this.options[i]['content']['votes'] = this.options[i]['content']['votes'] + 1;
            }
          }
          this.selectedOption = '';
        }
    }
});

// DOM element where the Timeline will be attached
var container = document.getElementById('visualization');

// Create a DataSet (allows two way data-binding)
app.update_group_data();
var groups = new vis.DataSet(app.get_group_data());
app.update_test_data();
var items = new vis.DataSet(app.get_test_data());

app.sortedItems();

var start = app.event_info['startTimeFrame']['year']+'-'+app.event_info['startTimeFrame']['month']+'-'+app.event_info['startTimeFrame']['day'];
var end = app.event_info['endTimeFrame']['year']+'-'+app.event_info['endTimeFrame']['month']+'-'+(app.event_info['endTimeFrame']['day']);
end = incrementDate(end);

function incrementDate(dateString) {
  const date = new Date(dateString);
  date.setDate(date.getDate() + 1);
  const newDateString = date.toISOString().slice(0, 10);
  return newDateString;
}


// Configuration for the Timeline
var options = {
  min: new Date(start),                // lower limit of visible range
  max: new Date(end),                // upper limit of visible range
};

// Create a Timeline
var timeline = new vis.Timeline(container, null, options);
timeline.setGroups(groups);
timeline.setItems(items);


function connect() {
    //Prepare web socket
    socket = io();

    //Connect
    socket.on('connect', function() {
        //Set connected state to true
        app.connected = true; 
        if (app.event_info.finalStartTime.length != 0) {
          app.renderDiv = false;
          app.renderFinalDiv = true;
          app.finalSavedTime = app.event_info.finalStartTime + " to " + app.event_info.finalEndTime;
        }
    });

    socket.on('error', function(message){ 
        alert(message);
    });

    socket.on('event_suggestions', (event_suggestions) => {
      app.options = JSON.parse(event_suggestions);
    });

    socket.on('event_votes', ()=>{
      app.update_votes();
    });

    socket.on('usersVoted', ()=>{
      app.increment_vote();
    });
}