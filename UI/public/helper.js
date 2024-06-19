var socket = null;
let error = document.getElementById('error').innerHTML
if(error) alert(error);

//Prepare scheduler
var helper = new Vue({
    el: '#friends_list_vue',
    data: {
        connected: false,
        friends: document.getElementById('friends_list') ? JSON.parse(document.getElementById('friends_list').innerHTML) : [],
        events: document.getElementById('events_list') ? JSON.parse(document.getElementById('events_list').innerHTML) : [],
        requests: document.getElementById('requests') ? JSON.parse(document.getElementById('requests').innerHTML) : []
    },
    mounted: function(){
        connect();
    },
    methods: {
        set_friends(){
            this.friends = document.getElementById('friends_list') ? JSON.parse(document.getElementById('friends_list').innerHTML) : []
        }
    }
});


function connect() {
    //Prepare web socket
    socket = io();

    //Connect
    socket.on('connect', function() {
        helper.connected = true;
    });

    socket.on('update_friends', () =>{
        socket.emit('get_friends')
    })

    socket.on('update_events', () => {
        socket.emit('get_events')
    })

    socket.on('events_list', (events, requests) =>{
        helper.events = JSON.parse(events)
        helper.requests = JSON.parse(requests)
    })

    socket.on('friends_list', (friends) =>{
        helper.friends = friends
    })

    socket.on('error', (message) => {
        console.log('received error')
        helper.set_friends()
        alert(message)
    })
}