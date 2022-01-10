//Author Rodions Barannikovs

var aliveSecond = 0;
var heartbeatRate = 5000;

var myChannel = "tadas-pi-channel"

var request = new XMLHttpRequest();
function keepAlive()
{
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){
				if(this.responseText !== null){
					var date = new Date();
					aliveSecond = date.getTime();
					var keepAliveData = this.responseText;
				}
			}
		}
	};
	request.open("GET", "keep_alive", true);
	request.send(null);
	setTimeout('keepAlive()', heartbeatRate);
}

function time()
{
	var d = new Date();
	var currentSec = d.getTime();
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{
		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}

pubnub = new PubNub({
            publishKey : "pub-c-23f0b7bb-05d1-4e28-ac32-f35c4b8a805c",
            subscribeKey : "sub-c-5180f24a-546d-11ec-931a-1addb9510060",
            uuid: "8ffc7d7d-2363-4ec8-bb6e-51ec369cd573"
        })
//Does the UUID has to be the same ???

let receivedMsg = {
            temperature: "101",
            humidity: "212",
            brightness: "light",
            soil: "wet",
            time: "time"}


pubnub.subscribe({channels: [myChannel]});

function sendStats(receivedMsg)
{
    request.open("POST", "updateStats", true);
     myJSON = JSON.stringify(receivedMsg);
	request.send(myJSON);
	console.log(myJSON);

}
pubnub.addListener({
       message: function(msg) {
            receivedMsg.temperature = msg.message.temperature
            receivedMsg.humidity = msg.message.humidity
            receivedMsg.soil = msg.message.soil
            receivedMsg.brightness = msg.message.brightness
            receivedMsg.time = msg.message.time
            console.log(receivedMsg.brightness)
            updateStats(msg.message)
//            sendStats(msg.message)
            }
         }
      )

function updateStats(receivedMsg)
{
document.getElementById('temperature').innerHTML  = receivedMsg.temperature
document.getElementById('humidity').innerHTML = receivedMsg.humidity
document.getElementById('brightness').innerHTML = receivedMsg.brightness
document.getElementById('soil').innerHTML = receivedMsg.soil
document.getElementById('time').innerHTML = receivedMsg.time

}
function publishUpdate(data, channel)
{
    pubnub.publish({
        channel: channel,
        message: data
        },
        function(status, response){
            if(status.error){
                console.log(status);
            }
            else
            {
                console.log("Message published with timetoken", response.timetoken)
            }
           }
        );
}


function handleClick()
{
	var ckbStatus = new Object();
	ckbStatus = "refresh";
	var event = new Object();
	event.event = ckbStatus;
	publishUpdate(event, myChannel);
	console.log(event);
	 console.log("sent status")
}

function handleDelete (plant_id)
{
const n = BigInt(plant_id).toString();
request.open("POST", "deletePlant", true);
	request.send(n);
}
