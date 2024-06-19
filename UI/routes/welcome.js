const express = require('express')
const router = express.Router()
const helper = require('./helper')

async function register(name, email, password){
    console.log('Handling register');
    if(name == '') return {'result': false, 'message': 'The name field is empty'}
    if(email == '') return {'result': false, 'message': 'The email field is empty'}
    if(password == '') return {'result': false, 'message': 'The password field is empty'}

    return await helper.postRequest({name: name, email: email, password: password}, '/api/user/register')
}

async function login(email, password){
    console.log('Handling login')
    if(email == '') return {'result' : false, 'message': 'The email field is empty'}
    if(password == '') return {'result' : false, 'message': 'The password field is empty'}

    return await helper.postRequest({email: email, password: password}, '/api/user/login')
}

router.get('/register', (req, res) => {
    if(req.cookies['email']) {
        res.cookie('error', 'You are already logged in', helper.cookie_settings)
        res.redirect('/home'); 
        return
    }
    if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./welcome/register', {'error': req.cookies['error']})
    }
    else res.render('./welcome/register')
})   

router.post('/register', async (req, res) => {
    if(req.cookies['email']) {res.redirect('/home'); return} 
    let register_res = await register(req.body.name, req.body.email, req.body.password)

    if(register_res.result) {
        res.cookie("email", req.body.email, helper.cookie_settings)
        res.cookie("password", req.body.password, helper.cookie_settings)
        res.cookie('error', 'You succesfully registered', helper.cookie_settings)
        res.redirect('home')
    }
    else res.render('./welcome/register', {'name': req.body.name, 'email': req.body.email, 'error': register_res.message})
})

router.get('/login', (req, res) => {
    if(req.cookies['email']) {
        res.cookie('error', 'You are already logged in', helper.cookie_settings)
        res.redirect('/home');
        return
    }
    if(req.cookies['error']){
        res.clearCookie('error')
        res.render('./welcome/login', {'error': error})
    }
    else res.render('./welcome/login')
})

router.post('/login', async (req, res) => {
    if(req.cookies['email']) {res.redirect('/home'); return}
    let login_res = await login(req.body.email, req.body.password)

    if(login_res.result) {
        res.cookie("email", req.body.email, helper.cookie_settings)
        res.cookie("password", req.body.password, helper.cookie_settings)
        res.cookie('error', 'Login successful', helper.cookie_settings)
        res.redirect('home')
    }
    else res.render('./welcome/login', {'email': req.body.email, 'error': login_res.message})
})

router.get('/logout', (req, res) => {
    if(!req.cookies['email']) {res.cookie('error', 'You are not logged in', helper.cookie_settings); res.redirect('/'); return}

    res.clearCookie('email') 
    res.clearCookie('password')
    res.cookie('error', 'Logout successful', helper.cookie_settings)
    res.redirect('/')
})

module.exports = router