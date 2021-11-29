var aliveSecond = 0;
var heartbeatRate = 5000;

var myChannel = "greenhouse"

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
            publishKey : "pub-c-011316ff-7704-4b4d-95c1-5596132eea7c",
            subscribeKey : "sub-c-be0150e4-3bc8-11ec-b886-526a8555c638",
            uuid: "Client-y2y86"
        })
//Does the UUID has to be the same ???

let receivedMsg = {
            id:1,
            time: 121020211140,
            temperature: 10,
            humidity: 21,
            brightness: "light",
            soil: "wet"}


pubnub.subscribe({channels: [myChannel]});

function sendStats(receivedMsg)
{
    request.open("POST", "updateStats", true);
     myJSON = JSON.stringify(receivedMsg);
	request.send(myJSON);

}
pubnub.addListener({

       message: function(msg) {
       console.log(msg.message.id)
            receivedMsg.id = msg.message.id
            receivedMsg.temperature = msg.message.temperature
            receivedMsg.humidity = msg.message.humidity
            receivedMsg.brightness = msg.message.brightness
            receivedMsg.soil = msg.message.soil
             updateStats(msg.message)
             sendStats(msg.message)
            }
         }
      )

function updateStats(receivedMsg)
{
console.log(receivedMsg.temperature)
document.getElementById('temperature').innerHTML  = receivedMsg.temperature
document.getElementById('humidity').innerHTML = receivedMsg.humidity
document.getElementById('brightness').innerHTML = receivedMsg.brightness
document.getElementById('soilMoist').innerHTML = receivedMsg.soil

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

function deletePlant(plant)
{
    console.log(plant.value)
    request.open("POST", "deletePlant", true);

}
function handleClick()
{
	var ckbStatus = new Object();
	ckbStatus[0] = "water";
	var event = new Object();
	event.event = ckbStatus;
	publishUpdate(event, myChannel);
	 console.log("sent status")
}
