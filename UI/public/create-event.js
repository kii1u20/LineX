//Prepare scheduler
var app = new Vue({
    el: '#create-event',
    data: {
        connected: false,
        friends: JSON.parse(document.getElementById('friends_list').innerHTML),
        selected: []
    },
    computed: {
        selectedFriends: function() {
          return this.friends.filter((friend, index) => this.selected[index]);
        }
    },
    mounted: function(){
        connect();
    },
    methods: {
        friends_list(list) {
            this.friends=list;
        }
    }
});