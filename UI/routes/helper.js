const https = require('https')
const cookieParser = require('cookie-parser');
//The current expiry time is set to 2 h
// const cookie_settings = {'encode': String, 'expires': new Date(Date.now() + (2 * 60 * 60 * 1000))}
const cookie_settings = {'encode': String}

let email_socket = new Map()
let socket_email = new Map()

//Give it a non JSON.strigify format
function postRequest(requestData, path){
    const options = {hostname: 'comp3207groupcoursework-function.azurewebsites.net',
    path: path,
    method: 'POST',
    headers: {'x-functions-key' : 'ahk2J8Rcw4j6b1v5oNTw05CeoBAI8ZuUP6DxTTHWKP3fAzFuGg_Clg=='}}

    return new Promise((resolve) => {
        console.log('POSTING: ' + JSON.stringify(requestData))
        const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) =>{
            data += chunk
        })
        res.on('end', () => {
            console.log('Body: ', JSON.parse(data))
            resolve(JSON.parse(data))
        })
        })
        req.write(JSON.stringify(requestData))
        req.end()
    })
}

function error(message, socket) {
    socket.emit('error', message);
}

async function getFriendsList(email, password, socket = null) {
    let data = {'email': email, 'password': password};
    let res_update = await postRequest(data, '/api/user/getfriends');
    console.log("The user " + email +  " has requested a list of their friends");
    if(socket == null) return {'result': true, 'message' : res_update};
    else socket.emit('friends_list', res_update);
}

async function getFriendsList_OnlyFriends(email, password, socket = null){
    let friends = await getFriendsList(email, password, socket)
    let friends_out = [];
    for(let friend of friends.message){
        if(friend.status == 'friend')
            friends_out.push(friend);
    }
    
    return {'result': true, 'message': friends_out};
}

async function getUsername(email, password){
    let data_get = {'email': email, 'password': password}
    return await postRequest(data_get, '/api/user/getName')
}

module.exports = {postRequest, cookieParser, cookie_settings, error, getFriendsList, getFriendsList_OnlyFriends, getUsername, email_socket, socket_email}