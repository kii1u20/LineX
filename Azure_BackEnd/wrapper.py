

#Note this requirement, in case you run this from outside the venv you are working on
import requests
# Set the 'function' authorization level on your deployment
# Put the relevant App key here (Refer to Lecture Thursday Week 4)

APP_KEY="ahk2J8Rcw4j6b1v5oNTw05CeoBAI8ZuUP6DxTTHWKP3fAzFuGg_Clg=="

LOCAL_SERVER="http://localhost:7071/api"
#Replace below as appropriate
# CLOUD_SERVER="https://coursework1-kii1u20.azurewebsites.net/api"

def PersonalCalendarAddEntry(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
         
    response = requests.post(prefix+'/personalCalendar/addEvent', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def Register(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/user/register', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def Login(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/user/login', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def player_leaderboard(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/player/leaderboard', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def prompt_create(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/prompt/create', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def prompt_edit(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/prompt/edit', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def prompt_delete(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/prompt/delete', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def prompts_get(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix+'/prompts/get', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def prompts_getText(the_input,local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification. 
    """
    if local:
        prefix = LOCAL_SERVER 
    else:
        prefix = CLOUD_SERVER
    print(prefix)
    response = requests.post(prefix+'/prompts/getText', json=the_input, 
            headers={'x-functions-key' : APP_KEY })
    output = response.json()
    return output

def tests():
    # you may use this function for your own testing
    # You should remove your testing before submitting your CW
    
    # PersonalCalendarAddEntry()
    # print(Register({'name' : 'Test', 'email' : 'kii1u20@soton.ac.uk', 'password': '12345678'}, True))
    print(Login({'email': 'kii1u20@soton.ac.uk', 'password' : '12345678'}, True))

if __name__ == '__main__':
    #If the script is called from the console or inside an IDE
    # it will execute the tests function
    tests()
      
