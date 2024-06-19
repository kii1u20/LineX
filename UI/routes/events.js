const express = require('express')
const router = express.Router()
const helper = require('./helper')

//get a certain user active events
async function getUserEvents(email_cookie, password_cookie, socket = null){
    if(email_cookie == '') return {'result': false, 'message': 'Invalid email'};
    if(password_cookie == '')  return {'result': false, 'message': 'Invalid password'};
  
    let data_update = {
      'email': email_cookie,
      'password': password_cookie
    };
  
    let res_update = await helper.postRequest(data_update, '/api/GetUserEvents');
    if(!res_update.result){
      console.log('A problem with getting the user events');
      //error(res_update.message, socket);
      return {'result': false, 'message': res_update.message};
    }
    else{
      console.log("The user events have been returned");
      let eventIdList = Object.keys(res_update.message);
      console.log('User active events are ' + eventIdList);
  

      let events = []
      //only get the details of user events with accepted status
      for (let i = 0; i < eventIdList.length; i++) {
        if (res_update.message[eventIdList[i]] == 'accepted') {
          let event = await getEvent(eventIdList[i], socket);
          if(event.result) events.push(event.message)
        }
      }

      return {'result': 'true', 'message': events};
    }
  }

async function saveFinalTime(eventId, finalStartTime, finalEndTime, users, description) {
  let save = await helper.postRequest({'id' : eventId, 'finalStartTime' : finalStartTime, 'finalEndTime' : finalEndTime}, '/api/SaveFinalEvent');

  let start_date = new Date(finalStartTime);
  let end_date = new Date(finalEndTime); 

  for (let user of users) {
    let personalCalendarData = {"email" : user, 'startDate' : {'day' : start_date.getDate(), 'month' : start_date.getMonth() + 1, 'year' : start_date.getFullYear(), 'hour' : start_date.getHours(), 'minutes' : start_date.getMinutes()}, 
                                'endDate' : {'day' : end_date.getDate(), 'month' : end_date.getMonth() + 1, 'year' : end_date.getFullYear(), 'hour' : end_date.getHours(), 'minutes' : end_date.getMinutes()}, 'description' : description}
    let updatePersonalCalendar = await helper.postRequest(personalCalendarData, '/api/personalCalendar/addEvent');
  }

  if (save.result) {
    return {'result' : 'true', 'message' : "Event final time saved successfuly"}
  }
}

  async function getUserEventRequests(email_cookie, password_cookie, socket = null){
    if(email_cookie == '') return {'result': false, 'message': 'Invalid email'};
    if(password_cookie == '')  return {'result': false, 'message': 'Invalid password'};
  
    let data_update = {
      'email': email_cookie,
      'password': password_cookie
    };
  
    let res_update = await helper.postRequest(data_update, '/api/GetUserEvents');
    if(!res_update.result){
      console.log('A problem with getting the user events');
      //error(res_update.message, socket);
      return {'result': false, 'message': res_update.message};
    }
    else{
      console.log("The user events have been returned");
      let eventIdList = Object.keys(res_update.message);  

      let events = []
      //only get the details of user events with accepted status
      for (let i = 0; i < eventIdList.length; i++) {
        if (res_update.message[eventIdList[i]] == 'pending') {
          let event = await getEvent(eventIdList[i], socket);
          if(event.result) events.push(event.message)
        }
      }

      return {'result': 'true', 'message': events};
    }
  }
  
  //get event data by id
  async function getEvent(event_id, socket = null) {
    if(event_id == '') {helper.error('Invalid event ID', socket); return;}
  
    let data_update = {
      'id': event_id
    };
  
    let res_update = await helper.postRequest(data_update, '/api/GetEvent');
    if(!res_update.result){
      console.log('A problem with getting the event');
      //error(res_update.message, socket);
      return {'result': false, 'message': res_update.message};
    }
    else{
      console.log("The event has been returned");
      if(socket != null){
        socket.emit('homeEvents', res_update.message);
      }else{
        return {'result': true, 'message': res_update.message};
      }
    }
  }

  //get event suggestions by id, start and end date
  async function updateEventSuggestions(event_info, socket = null) {
    if(event_info.startDate == '' || event_info.endDate == '') {helper.error('Invalid data', socket); return;}
  
    let data_update = {
      'id': event_info.id,
      'suggestion': [{'startDate': event_info.startDate, 'endDate': event_info.endDate,'votes': 0}]
    };
  
    let res_update = await helper.postRequest(data_update, '/api/UpdateEventSuggestions');
    if(!res_update.result){
      console.log('A problem with getting the event');
      //error(res_update.message, socket);
      return {'result': false, 'message': res_update.message};
    }
    else{
      console.log("The event has been returned");
      return {'result': true, 'message': res_update.message};
    }
  }  
  
  //increment event votes
  async function updateSuggestionVotes(ids, socket = null){
    if(ids.id == '' || ids.suggestion == '') {socket.emit('error', 'You must input both time frames'); return}
  
    let data_update = {
      'id': ids.id,
      'suggestion': ids.suggestion
    };
  
    let res_update = await helper.postRequest(data_update, '/api/UpdateSuggestionVotes');
    if(!res_update.result){
      console.log('A problem with getting the event');
      //error(res_update.message, socket);
      return {'result': false, 'message': res_update.message};
    }
    else{
      console.log("The event has been returned");
      return {'result': true, 'message': res_update.message};
    }
  }

  //updates users voted
  async function updateUsersVoted(id, email, socket = null){
    console.log("id: "+id);
    console.log("email: "+email);
    if(id == '' || email == '') {socket.emit('error', 'Make sure you have selected a suggestion and are logged in.'); return}
  
    let data_update = {
      'id': id,
      'email': email
    };
  
    let res_update = await helper.postRequest(data_update, '/api/UpdateEventsUsersVoted');
    if(!res_update.result){
      console.log('A problem with getting the event');
      //error(res_update.message, socket);
      return {'result': false, 'message': res_update.message};
    }
    else{
      console.log("The event has been returned");
      return {'result': true, 'message': res_update.message};
    }
  }

//get personal events by email
async function getCalendars(email, startDate, endDate) {

  // if(startDate == {} || endDate == {}) {error('Empty start or end date', socket); return;}

  let data_update = {
    'email': email,
    'startDate': startDate,
    'endDate': endDate
  };

  let res_update = await helper.postRequest(data_update, '/api/GetCalendars');
  if(!res_update.result){
    console.log('A problem with getting the personal events');
    return [];
  }
  else{
    console.log("The personal events have been returned");
    return res_update.message;
  }
}

router.get('/', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let events = await getUserEvents(req.cookies['email'], req.cookies['password'], null)
    let pendingEvents = await getUserEventRequests(req.cookies['email'], req.cookies['password'], null)
    if(!events.result) {
      if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./events/events', {'error': req.cookies['error']})
      }
      else res.render('./events/events')
    }
    else{
      if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./events/events', {'events_list': JSON.stringify(events.message), 'error': req.cookies['error'], 'requests': JSON.stringify(pendingEvents.message)})
      }
      else res.render('./events/events', {'events_list': JSON.stringify(events.message), 'requests': JSON.stringify(pendingEvents.message)})
    } 
})



router.post('/modify', async (req, res) => {
  if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}

  if ('acceptButton' in req.body) { //Add event to personal calendar
    let accept = await helper.postRequest({'email' : req.cookies['email'], 'eventID' : req.body.eventId, 'status' : "accept"}, "/api/user/modifyActiveEvent");
    
    console.log(req.body)

    // let personalCalendarData = {"email" : req.cookies['email'], 'startDate' : {'day' : parseInt(req.body.startDay), 'month' : parseInt(req.body.startMonth), 'year' : parseInt(req.body.startYear), 'hour' : parseInt(req.body.startHour), 'minutes' : parseInt(req.body.startMinutes)}, 
    //                             'endDate' : {'day' : parseInt(req.body.endDay), 'month' : parseInt(req.body.endMonth), 'year' : parseInt(req.body.endYear), 'hour' : parseInt(req.body.endHour), 'minutes' : parseInt(req.body.endMinutes)}, 'description' : req.body.description}
    //let updatePersonalCalendar = await helper.postRequest(personalCalendarData, '/api/personalCalendar/addEvent');
    //console.log("AHAHAHAHAHAHAHAHAHAHAAHHAHAHA")
    //console.log(updatePersonalCalendar.message)
    if (accept.result) {
      res.cookie('error', 'Event has been successfuly accepted', helper.cookie_settings)
      res.redirect('/events')
    } else {
      res.cookie('error', 'There has been an error accepting the event. Please try again later.', helper.cookie_settings)
      res.redirect('/events')
    }
  } else if ('rejectButton' in req.body) { //Find a way to remove the event from personal calendar too
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let accept = await helper.postRequest({'email' : req.cookies['email'], 'eventID' : req.body.eventId, 'status' : "reject"}, "/api/user/modifyActiveEvent");
    
    let updateParticipants = await helper.postRequest({"id" : req.body.eventId, "user" : req.cookies['email'], "task" : "remove"}, "/api/events/updateParticipants")
    if (updateParticipants.result) {
      res.cookie('error', 'Event has been successfuly rejected', helper.cookie_settings)
      res.redirect('/events')
    } else {
      res.cookie('error', 'There has been an error rejecting the event. Please try again later.', helper.cookie_settings)
      res.redirect('/events')
    }
  } else {
    res.cookie('error', 'Should not have been able to reach this point.', helper.cookie_settings)
    res.redirect('/')
  }
})

//Find a way to remove the event from personal calendar too
router.post('/quit', async (req, res) => {
  if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}

  await helper.postRequest({'email' : req.cookies['email'], 'eventID' : req.body.eventId, 'status' : "quit"}, "/api/user/modifyActiveEvent");
  let updateParticipants = await helper.postRequest({"id" : req.body.eventId, "user" : req.cookies['email'], "task" : "remove"}, "/api/events/updateParticipants")
  if (updateParticipants.result) {
    res.cookie('error', 'You quit the event successfuly', helper.cookie_settings)
    res.redirect('/events')
  } else {
    res.cookie('error', 'There has been an error. Please try again later.', helper.cookie_settings)
    res.redirect('/events')
  }
})

router.get('/add/event', async (req, res) => {
  if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
  let friends = await helper.getFriendsList_OnlyFriends(req.cookies['email'], req.cookies['password'], null);
  if(friends.message.length == 0) {res.cookie('error', 'You need some friends before creating an event.', helper.cookie_settings); res.redirect('/home');return}
  else res.render('./events/create-event', {'friends_list': JSON.stringify(friends.message)})
})

router.post('/add/event', async (req, res) => {
  if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
  let start_date = new Date(req.body.start_date);
  let end_date = new Date(req.body.end_date); 
  let invited = [req.cookies['email']];
  let duration = req.body['duration-value'];

  console.log(JSON.stringify(req.body))

  //Why is that? -> cause u need it for wrong input
  let friends = await helper.getFriendsList_OnlyFriends(req.cookies['email'], req.cookies['password'], null);
  
  if (!('friend' in req.body)) {
    res.render('./events/create-event', {'event_name': req.body.event_name, 'description': req.body.description, 'start_date': req.body.start_date, 'end_date': req.body.end_date, 'friends_list': JSON.stringify(friends.message), 'error': 'You have not invited anyone to this event!'})
    return;
  } else {
    invited = invited.concat(req.body.friend);
  }

  //Add guards
  if (start_date > end_date) {
    res.render('./events/create-event', {'friend': req.body.friend, 'event_name': req.body.event_name, 'description': req.body.description, 'start_date': req.body.start_date, 'end_date': req.body.end_date, 'friends_list': JSON.stringify(friends.message), 'error': 'The start timeframe cannot be after the end timeframe!'})
    return;
  }
  
    
  let data = {"users": invited, "title": req.body.event_name, "description": req.body.description, 
              "startTimeFrame": {'day' : start_date.getDate(), 'month' : start_date.getMonth() + 1, 'year' : start_date.getFullYear(), 'hour' : start_date.getHours(), 'minutes' : start_date.getMinutes()},
              "endTimeFrame": {'day' : end_date.getDate(), 'month' : end_date.getMonth() + 1, 'year' : end_date.getFullYear(), 'hour' : end_date.getHours(), 'minutes' : end_date.getMinutes()}}
  let res_update = await helper.postRequest(data, '/api/events/createEvent');
  if(res_update.result){
    for (let inv of invited) {
      if (inv == req.cookies['email']) {
        let updateData = {"email": inv, "eventID": res_update.message, "status" : "accepted"}
        await helper.postRequest(updateData, '/api/user/updateActiveEvents');
        //Why would u add it to the personal calendar if a time is not decided?
        //let personalCalendarData = {"email" : inv, 'startDate' : data.startTimeFrame, 'endDate' : data.endTimeFrame, 'description' : data.description}
        //let updatePersonalCalendar = await helper.postRequest(personalCalendarData, '/api/personalCalendar/addEvent');
      } else {
        let updateData = {"email": inv, "eventID": res_update.message, "status" : "pending"}
        await helper.postRequest(updateData, '/api/user/updateActiveEvents');
        if(helper.email_socket.has(inv)){helper.email_socket.get(inv).emit('update_events')}
      }
    }
    // if (updateActiveEvents.result) {
    //   console.log("Event saved!");
    // } else {
    //   //delete the event entry from azure!
    // }
    res.cookie('error', 'Event has been successfuly created', helper.cookie_settings)
    res.redirect('/events')
  }
  else{
    let friends = await helper.getFriendsList_OnlyFriends(req.cookies['email'], req.cookies['password'], null);
    res.render('./events/create-event', {'event_name': req.body.event_name, 'duration': req.body.duration, 'description': req.body.description, 'start_date': req.body.start_date, 'end_date': req.body.end_date, 'friends_list': JSON.stringify(friends.message), 'error': res_update.message})
  }
})

router.post('/event', async (req, res) => {
  //check that the user is in that event

  if(!req.body.event_id) {res.cookie('error', 'There is no event with this id'); res.redirect('/events'); return;}

  let eventInfo = await getEvent(req.body.event_id, null)
  console.log('pqppe' + eventInfo.result)
  if(!eventInfo.result) {res.redirect('/events'); return}
  var startTimeFrame = eventInfo.message['startTimeFrame'];
  var endTimeFrame = eventInfo.message['endTimeFrame'];
  var personalEvents=[];
  for (let i = 0; i < eventInfo.message['users'].length; i++) {
    console.log('Test email: '+eventInfo.message['users'][i]);
    let personalCalendarEvent = await getCalendars(eventInfo.message['users'][i], startTimeFrame, endTimeFrame);
    personalEvents.push.apply(personalEvents, personalCalendarEvent)
  }
  res.render('./events/current-event', {'calendars': JSON.stringify(personalEvents), 'event' : JSON.stringify(eventInfo.message)})
})

module.exports = {'router':router, 'getUserEvents': getUserEvents, 'getCalendars': getCalendars, 'updateEventSuggestions': updateEventSuggestions, 'updateSuggestionVotes': updateSuggestionVotes, 'getEvent': getEvent, 'getUserEventRequests': getUserEventRequests, 'updateUsersVoted': updateUsersVoted, 'saveFinalTime' : saveFinalTime}