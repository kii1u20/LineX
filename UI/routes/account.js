const { raw } = require('express');
const express = require('express')
const router = express.Router()
const helper = require('./helper');

async function change_password(change_pwd, email_cookie, password_cookie){
    console.log('Handling changing password')
    if(change_pwd.old_pwd_fd == '') return {'result' : false, 'message': 'The old password field is empty'}
    if(change_pwd.new_pwd_fd == '') return {'result' : false, 'message': 'The new password field is empty'}
    if(change_pwd.confirm_pwd_fd == '') return {'result' : false, 'message': 'The confirm password field is empty'}
    if(change_pwd.new_pwd_fd != change_pwd.confirm_pwd_fd) return {'result' : false, 'message': 'The new password with confirm password do not match'}
    if(change_pwd.old_pwd_fd != password_cookie) return {'result' : false, 'message': 'That is not your old password'}

    let data_update = {'email': email_cookie, 'oldPassword': password_cookie, 'newPassword': change_pwd.new_pwd_fd}
    return await helper.postRequest(data_update, '/api/user/updatePassword');
}

async function friend_action(action, email_cookie, password_cookie, email_friend){
    if(email_friend == '')  return {'result': false, 'message': 'The email for the friend is empty'}

    let data = {'email1': email_cookie, 'password': password_cookie, 'email2': email_friend}
    if(action == 'add') return await helper.postRequest(data, '/api/user/addfriend')
    if(action == 'remove') return await helper.postRequest(data, '/api/user/deletefriend')
    if(action == 'accept') return await helper.postRequest(data, '/api/user/acceptfriend')
    if(action == 'reject') return await helper.postRequest(data, '/api/user/rejectfriend')
}

async function add_calendar_entry(email_cookie, start, end, description){
    //Add gurards
    
    let data_add = {"email": email_cookie, "description": description, 
              "startDate": {'day' : start.getDate(), 'month' : start.getMonth() + 1, 'year' : start.getFullYear(), 'hour' : start.getHours(), 'minutes' : start.getMinutes()},
              "endDate": {'day' : end.getDate(), 'month' : end.getMonth() + 1, 'year' : end.getFullYear(), 'hour' : end.getHours(), 'minutes' : end.getMinutes()}}
    return await helper.postRequest(data_add, '/api/personalCalendar/addEvent')
}

router.get('/change/password', (req, res) => {
    if(!req.cookies['email']) {
        res.cookie('error', 'You are not logged in', helper.cookie_settings)
        res.redirect('/');
        return
    } 
    if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./account/change-password', {'error': req.cookies['error']})
    }
    else res.render('./account/change-password')
})

router.post('/change/password', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let change_res = await change_password({'old_pwd_fd': req.body.old_password, 'new_pwd_fd': req.body.new_password, 'confirm_pwd_fd': req.body.confirm_password}, req.cookies['email'], req.cookies['password'])
    if(change_res.result){
        res.cookie("password", req.body.confirm_password, helper.cookie_settings)
        res.cookie("email", req.cookies['email'], helper.cookie_settings)
        res.cookie('error', 'The password has been changed successfuly', helper.cookie_settings)
        res.redirect('/home')
    }
    else res.render('./account/change-password', {'error': change_res.message})
})

router.post('/add/friend', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let add_res = await friend_action('add', req.cookies['email'],  req.cookies['password'], req.body.friend_email)
    if(add_res.result) {
        if(helper.email_socket.has(req.body.friend_email)) helper.email_socket.get(req.body.friend_email).emit('update_friends')
        res.cookie('error', 'The friend request has been sent successfuly', helper.cookie_settings)
        res.redirect('/home')
    }
    else {res.cookie('error', add_res.message, helper.cookie_settings); res.redirect('/home')}
})

router.post('/remove/friend', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let remove_res = await friend_action('remove', req.cookies['email'], req.cookies['password'], req.body.friend)
    if(remove_res.result){
        if(helper.email_socket.has(req.body.friend)) helper.email_socket.get(req.body.friend).emit('update_friends')
        res.cookie('error', 'The friend has been removed succesfully', helper.cookie_settings)
        res.redirect('/home')
    }
    else {res.cookie('error', remove_res.message, helper.cookie_settings); res.redirect('/home')}
})

router.post('/reject/friend', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let reject_res = await friend_action('reject', req.cookies['email'], req.cookies['password'], req.body.friend)
    if(reject_res.result){
        if(helper.email_socket.has(req.body.friend)) helper.email_socket.get(req.body.friend).emit('update_friends')
        res.cookie('error', 'The friend has been rejected succesfully', helper.cookie_settings)
        res.redirect('/home')
    }
    else {res.cookie('error', reject_res.message, helper.cookie_settings); res.redirect('/home')}
})

router.post('/accept/friend', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let accept_res = await friend_action('accept', req.cookies['email'], req.cookies['password'], req.body.friend)
    if(accept_res.result) {
        if(helper.email_socket.has(req.body.friend)) helper.email_socket.get(req.body.friend).emit('update_friends')
        res.cookie('error', 'The friend has been accepted succesfully', helper.cookie_settings)
        res.redirect('/home')
    }
    else {res.cookie('error', accept_res.message, helper.cookie_settings); res.redirect('/home')}
})
  
router.get('/', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    let friends = await helper.getFriendsList(req.cookies['email'], req.cookies['password'], null);
    let username = await helper.getUsername(req.cookies['email'], req.cookies['password'])
    if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./account/profile', {'friends_list': JSON.stringify(friends.message), 'username': username, 'email': req.cookies['email'], 'error': req.cookies['error']})
    }
    else res.render('./account/profile', {'friends_list': JSON.stringify(friends.message), 'username': username, 'email': req.cookies['email']})
})

router.get('/calendar', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}

    startDate = {"day": 24, "month": 12, "year": 2012, "hour": 13, "minutes": 30}
    endDate = {"day": 24, "month": 12, "year": 2032, "hour": 13, "minutes": 30}

    let personalCalendar = await require('./events')['getCalendars'](req.cookies['email'], startDate, endDate)

    console.log(JSON.stringify(personalCalendar))
    if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./account/calendar', {'eventsList': JSON.stringify(personalCalendar), 'error': req.cookies['error']})
    }
    else res.render('./account/calendar', {'eventsList': JSON.stringify(personalCalendar)})
})

router.get('/calendar/add/entry', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./account/add-calendar-entry', {'error': req.cookies['error']})
    }
    else res.render('./account/add-calendar-entry')
})

router.post('/calendar/add/entry', async (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}
    
    let res_add = await add_calendar_entry(req.cookies['email'], new Date(req.body.start_date), new Date(req.body.end_date), req.body.description)
    if(!res_add.result) res.render('./account/add-calendar-entry', {'description': req.body.description, 'start_date': req.body.start_date, 'end_date': req.body.end_date, 'error': res_add.message})
    else {
        let personalCalendar = await require('./events')['getCalendars'](req.cookies['email'], startDate, endDate)
        res.render('./account/calendar', {'error': 'The entry has been added successfuly', 'eventsList': JSON.stringify(personalCalendar)})
    }
})

module.exports = router