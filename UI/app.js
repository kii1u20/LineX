'use strict';

//Set up express
const express = require('express');
const https = require('https');
const app = express();
const cookieParser = require('cookie-parser');
const cookie = require('cookie')

//Helper function
const helper = require('./routes/helper')

//The events backend functions
const eventsHelper = require('./routes/events')

//Setup socket.io
const server = require('http').Server(app);
const io = require('socket.io')(server);

//Setup static page handling
app.set('view engine', 'ejs');
app.use('/static', express.static('public'));
app.use(express.urlencoded({ extended : true }));
app.use(cookieParser())

app.use('/', require('./routes/welcome'))
app.use('/account', require('./routes/account'))
app.use('/events', require('./routes/events')['router'])

//Handle client interface on /
app.get('/', (req, res) => {
  if(req.cookies['email']) {
    res.cookie('error', 'You are already logged in', helper.cookie_settings)
    res.redirect('/home')
    return;
  }
  if(req.cookies['error']){
    res.clearCookie('error')
    res.render('./welcome/start', {'error': req.cookies['error']})
  }
  else{
    res.render('./welcome/start');
  }
});

app.get('/home', async (req, res) => {
  if(!req.cookies['email']) {
    res.cookie('error', 'You are not logged in', helper.cookie_settings)
    res.redirect('/');
    return
  }

  let friends = await helper.getFriendsList(req.cookies['email'], req.cookies['password'], null);
  let username = await helper.getUsername(req.cookies['email'], req.cookies['password'])
  
  if(req.cookies['error']){
    res.clearCookie('error')
    res.render('./welcome/home', {'friends_list': JSON.stringify(friends.message), 'username': username, 'error': req.cookies['error']})
  }
  else{
    res.render('./welcome/home', {'friends_list': JSON.stringify(friends.message), 'username': username})
  }
});

let email_socket = helper.email_socket
let socket_email = helper.socket_email

//Start the server
function startServer() {
    const PORT = process.env.PORT || 8080;
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

function handleConnection(email_connection, socket){
  if(!email_connection) return
  if(email_socket.has(email_connection)) return

  email_socket.set(email_connection, socket)
  socket_email.set(socket, email_connection)
  console.log('Welcome ' + email_connection + ' ' + email_socket.size)
}

function handleQuit(email_connection, socket){
  if(!email_connection) return
  
  email_socket.delete(email_connection)
  socket_email.delete(socket)
  
  console.log('Bye Bye ' + email_connection + ' ' + socket_email.size)
}

//Handle new connection
io.on('connection', socket => {
    let email_connection = null
    let password_connection = null
    if(socket.handshake.headers.cookie){
      email_connection = cookie.parse(socket.handshake.headers.cookie)['email']; 
      password_connection = cookie.parse(socket.handshake.headers.cookie)['password']
    }
    
    handleConnection(email_connection, socket)

    socket.on('get_friends', async () => {
      console.log('Got a get_friends from ' + socket_email.get(socket))
      let friends = await helper.getFriendsList(email_connection, password_connection)
      socket.emit('friends_list', friends.message)
    })

    socket.on('get_events', async () => {
      console.log('Got a get_events from' + socket_email.get(socket))
      let events = await eventsHelper.getUserEvents(email_connection, password_connection, null)
      let pendingEvents = await eventsHelper.getUserEventRequests(email_connection, password_connection, null)
      console.log(events.message + '\n' + pendingEvents.message)
      socket.emit('events_list', JSON.stringify(events.message), JSON.stringify(pendingEvents.message))
    })

    //Handle disconnection
    socket.on('disconnect', () => {
      handleQuit(email_connection, socket)
    });

    //Requesting events info
    socket.on('addOption', async (info) =>{
      //Check if the user is logged in??
      await eventsHelper.updateEventSuggestions(info, socket);
      let event_sugesstions = await eventsHelper.getEvent(info.id, null)
      if(event_sugesstions.result) socket.emit('event_suggestions', JSON.stringify(event_sugesstions.message.suggestions))
    });

    //Incrementing an event vote
    socket.on('incrementVote', async (info) =>{
      //Check if the user is logged in??
      let votes = await eventsHelper.updateSuggestionVotes(info);
      if(votes.result){
        socket.emit('event_votes')
      }else{
        helper.error(votes.message, socket);
      }
    });

     //Update users voted
     socket.on('updateUsersVoted', async (id) =>{
      //Check if the user is logged in??
      let update = await eventsHelper.updateUsersVoted(id, email_connection);
      if(update.result){
        socket.emit('usersVoted')
      }else{
        helper.error(update.message, socket);
      }
    });

    socket.on('saveFinalTime', async (message) =>{
      //Check if the user is logged in??
      let update = await eventsHelper.saveFinalTime(message.id, message.finalStartTime, message.finalEndTime, message.users, message.description);
      if(update.result){
        //
      }else{
        helper.error(update.message, socket);
      }
    });
});  

//Start server
if (module === require.main) {
    startServer();
}
  
module.exports = server;