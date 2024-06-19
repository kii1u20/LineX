var socket = null;
let counter = 0;
let eventsList = JSON.parse(document.getElementById('eventsList').innerHTML);

//Prepare scheduler
var app = new Vue({
    el: '#calendar',
    data: {
        connected: false,
        error: 'a',
        weekdays: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        eventsList_Vue: JSON.parse(document.getElementById('eventsList').innerHTML)
    },
    mounted: function(){
        connect();
    },
    methods: {
        //For testing to see that your website is working
        test_app_runs(){
            socket.emit('Hello world!');
        },
        get_eventsList(){
            return this.eventsList_Vue;
        }
    }
});

function connect() {
    //Prepare web socket
    socket = io();

    //Connect
    socket.on('connect', function() {
        //Set connected state to true
        app.connected = true; 

        app.test_app_runs();

        handleButtons();
        loadCalendar();
    });

    socket.on('error', function(message){ 
        alert(message);
    });
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function loadCalendar() {
    const calendarDoc = document.getElementById('calendarContent');

    const date = new Date();

    if(counter!==0) {
        date.setMonth(new Date().getMonth() + counter);
    }

    const day = date.getDate();
    const month = date.getMonth();
    const year = date.getFullYear();

    const daysInMonth = new Date(year, month+1, 0).getDate();
    const firstDayInMonth = new Date(year, month, 1);

    const dateString = firstDayInMonth.toLocaleDateString('en-uk', {
        weekday: 'long',
        year: 'numeric',
        month: 'numeric',
        day: 'numeric'
    });
    const paddingDays = app.weekdays.indexOf(dateString.split(', ')[0]);

    document.getElementById('currentMonth').innerText = date.toLocaleDateString('en-uk', {month: 'long'}) + ' ' + year;

    calendarDoc.innerHTML = '';

    for (let i = 1; i<=paddingDays+daysInMonth; i++) {
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('day');

        if(i>paddingDays) {
            dayDiv.innerText = i - paddingDays;

            if (i - paddingDays === day && counter === 0) {
                dayDiv.classList.add('currentDay');
            }

            const dayEvent = eventsList.filter(r => inTimeframe(r, i, paddingDays, month, year));
            //Here u call app.get_eventsList()

            if(dayEvent) {
                dayEvent.forEach(element => {
                    const eventDisplayDiv = document.createElement('div');
                    eventDisplayDiv.classList.add('eventC');
                    eventDisplayDiv.innerText = element.description;
                    dayDiv.appendChild(eventDisplayDiv);
                });
            }
        } else {
            dayDiv.classList.add('paddingC');
        }
        calendarDoc.appendChild(dayDiv);
    }
}

function inTimeframe(r, i, paddingDays, month, year) {
    if(r.startDate.day <= i - paddingDays && i - paddingDays <= r.endDate.day && r.startDate.month == month + 1 && month + 1 == r.endDate.month && r.startDate.year == year && year == r.endDate.year) {
        return true;
    } else if (r.startDate.day <= i - paddingDays && r.startDate.month == month + 1 && month + 1 < r.endDate.month && r.startDate.year == year && year == r.endDate.year) {
        return true;
    } else if (i - paddingDays <= r.endDate.day && r.startDate.month < month + 1 && month + 1 == r.endDate.month && r.startDate.year == year && year == r.endDate.year) {
        return true;
    } else if (r.startDate.day <= i - paddingDays && r.startDate.month <= month + 1 && r.startDate.year == year && year < r.endDate.year) {
        return true;
    } else if (i - paddingDays <= r.endDate.day && month + 1 <= r.endDate.month && r.startDate.year < year && year == r.endDate.year) {
        return true;
    } else {
        return false;
    }
}

function handleButtons() {
    document.getElementById('previousButton').addEventListener('click', () => {
        counter--;
        loadCalendar();
    });

    document.getElementById('nextButton').addEventListener('click', () => {
        counter++;
        loadCalendar();
    });
}