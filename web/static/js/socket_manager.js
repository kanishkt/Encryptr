// @author : Sudarshan Govindaprasad

// MOTIVATION FROM FLASK-SOCKETIO DOCUMENTATION
var socket;
$(document).ready(function(){

    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat'); // Connect to socket.io server
    socket.on('connect', function() {
        socket.emit('join', {}); // On connect of a new user, emit join signal to socket.io server
    });

    /**
     * @author : Sudarshan Govindaprasad
     * On status being emitted by socket.io server, this function catches the join information and
     * adds it to the chat message box
     */
    socket.on('status', function(data) {
        $('#chat').val($('#chat').val() + '<!' + data.msg + '!>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    /**
     * @author : Sudarshan Govindaprasad
     * On a new message being emitted by socket.io server, this function
     * catches it and appends it to the chat box
     */
    socket.on('message', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
    });

    /**
     * @author : Sudarshan Govindaprasad
     * On Key Press of enter, message is retrieved from textbox (text) and emit signal with message is sent to
     * socket.io server
     */
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
        }
    });
});

/**
 * When a user leaves the room, socket is disconnected and user is redirected to a common page
 */
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        var redirect ='http://' + document.domain + ':' + location.port + '/';
        window.location.href = redirect;
    });
}