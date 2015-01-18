/**
 * Created by canerten on 14/06/2014.
 */
var robot	= function(options) {
    this.websocket = false;

    this.joystick = null;
    this.options = options;
    this.feedback = options.feedback;
    this.isStopped = true;


    this.init = function() {

        var self = this;

        if ("WebSocket" in window) {
            var socketAddress = "ws://"+  window.location.host +"/websocket";
            console.log(socketAddress);

            this.websocket = new WebSocket(socketAddress);
            this.websocket.onopen = function() {

                //self.websocket.send('{"command":"move","x":5.3,"y":-2.2}'); //+ value + "}");
            };

            this.websocket.onmessage = function (msg) {
                var message = JSON.parse(msg.data);
                document.getElementById('serverFeedback').innerHTML = message.response;
            };



            // Cleanly close websocket when unload window
            window.onbeforeunload = function () {
                self.websocket.onclose = function () {
                }; // disable onclose handler first
                self.websocket.close()
            };
        } else {
            this.log("WebSocket are not supported by your browsers but required to communicate with the rover..");
        }

        this.joystick = new VirtualJoystick({
            container: document.getElementById("joystick"),
            mouseSupport: true,
            limitStickTravel: true,
            stickRadius: 20,
            baseX:50,
            baseY:10,
            useCssTransform : true,
            strokeStyle:'blue'
        });


        setInterval(function() { self.handle(); }, 500);
        //setInterval(function() { self.checkIfIsStopped(false); }, 150);
    }

    this.handle = function () {

        var dx = this.joystick.deltaX();
        var dy = this.joystick.deltaY();
        this.feedback.innerHTML	=
             ' dx:'+ dx + "<br/>"
            + ' dy:'+dy + "<br/>"
            + (this.joystick.right()	? ' right'	: '')
            + (this.joystick.up()	? ' up'	: '')
            + (this.joystick.left()	? ' left'	: '')
            + (this.joystick.down()	? ' down' : '')
       +  (!this.joystick.right() && !this.joystick.up()  && !this.joystick.left()   &&  !this.joystick.down()
        ? ' no direction' : '');

        if (!this.joystick.right() && !this.joystick.up()  && !this.joystick.left()   &&  !this.joystick.down())
        {
            if (!this.isStopped) {
                var message = JSON.stringify({"command": "stop"});
                this.websocket.send(message);
                this.isStopped = true;
            }
        }
        else {
            var message = JSON.stringify({"command": "move", "x": dx, "y": dy});
            this.websocket.send(message);
            this.isStopped = false;
        }

    }
}
