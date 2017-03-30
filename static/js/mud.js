function start_websocket() {
    $(document).ready(function() {
	if (!window.console) window.console = {};
	if (!window.console.log) window.console.log = function() {};

	$("#messageform").on("submit", function() {
            newMessage($(this));
            return false;
	});
	$("#messageform").on("keypress", function(e) {
            if (e.keyCode == 13) {
		newMessage($(this));
		return false;
            }
	});
	$("#command").select();
	updater.start();
    });
}

function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

function saveMessage() {
    var message = {"type":"save"};
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

function resetMessage() {
    var message = {"type":"reset"};
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

function scroll_to_bottom() {
    $("#inbox").animate({scrollTop:$("#inboxcontents").height()}, 1000);
}

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/websocket";
	updater.socket = new WebSocket(url);
	updater.socket.onmessage = function(event) {
	    updater.showMessage(JSON.parse(event.data));
	}
    },

    showMessage: function(message) {
	var html = "<div class=\"alert mud-"+message.type+"\">"+message.html+"</div>"
        $("#inboxcontents").append(html);
	scroll_to_bottom();
    }
};
