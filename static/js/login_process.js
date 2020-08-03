      //webkitURL is deprecated but nevertheless
      URL = window.URL || window.webkitURL;

      var gumStream; //stream from getUserMedia()
      var rec; //Recorder.js object
      var input; //MediaStreamAudioSourceNode we'll be recording

      // shim for AudioContext when it's not avb. 
      var AudioContext = window.AudioContext || window.webkitAudioContext;
      var audioContext; //audio context to help us record
      document.getElementById("geo").addEventListener("click", Geolocation);

      function Record_btn() {
        document.getElementById("loc-form").submit();
        /*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

        var constraints = {
          audio: true,
          video: false
        };


        /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

        navigator.mediaDevices.getUserMedia(constraints);
        var timeLeft = 3;
        var elem = document.getElementById('timer');
        var timerId = setInterval(countdown, 1000);

        function countdown() {
          if (timeLeft == -1) {
            clearTimeout(timerId);
            doSomething();
          } else {
            elem.innerHTML = timeLeft + ' sec';
            timeLeft--;
          }
        }

        function doSomething() {
          document.getElementById('text').style.display = "none";
          document.getElementById("rec-ani").style.display = "block";
          Record_function();

        }

        function Record_function() {
          // start recording here
          console.log("recordButton clicked");



          navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

            /*
            	create an audio context after getUserMedia is called
            	sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            	the sampleRate defaults to the one set in your OS for your playback device

            */
            audioContext = new AudioContext();

            /*  assign to gumStream for later use  */
            gumStream = stream;

            /* use the stream */
            input = audioContext.createMediaStreamSource(stream);

            /* 
            	Create the Recorder object and configure to record mono sound (1 channel)
            	Recording 2 channels  will double the file size
            */
            rec = new Recorder(input, {
              numChannels: 1
            });

            //start the recording process
            rec.record();

            console.log("Recording started");

          }).catch(function (err) {
            //enable the record button if getUserMedia() fails
            alert("something Failed");
          });


          var stopLeft = 3;
          var elem = document.getElementById('timer');
          var timerIdstop = setInterval(countstop, 1000);

          function countstop() {
            if (stopLeft == -1) {
              clearTimeout(timerIdstop);
              dostop();
            } else {
              elem.innerHTML = stopLeft + ' sec';
              stopLeft--;
            }
          }

          function dostop() {
            document.getElementById("rec-ani").style.display = "none";
            console.log("stopButton clicked");
            //tell the recorder to stop the recording
            rec.stop();

            //stop microphone access
            gumStream.getAudioTracks()[0].stop();

            //create the wav blob and pass it on to createDownloadLink
            rec.exportWAV(createDownloadLink);

          }
        }
      }

      function createDownloadLink(blob) {


        //name of .wav file to use during upload and download (without extendion)
        var filename = new Date().toISOString();



        //upload link



        if (confirm("Press ok to submit voice Or simply click cancel to re-record")) {
          var xhr = new XMLHttpRequest();
          xhr.onload = function (e) {
            if (this.readyState === 4) {
              console.log("Server returned: ", e.target.responseText);
            }
          };
          var fd = new FormData();
          fd.append("audio_data", blob, filename);
          xhr.open("POST", "/record", true);
          xhr.send(fd);
          document.getElementById("recog").style.display = "block";




          var loginLeft = 3;
          var elem = document.getElementById('timer');
          var timerIdlogin = setInterval(countlogin, 1000);

          function countlogin() {
            if (loginLeft == -1) {
              clearTimeout(timerIdlogin);
              dologin();
            } else {
              elem.innerHTML = loginLeft + ' sec';
              loginLeft--;
            }
          }

          function dologin() {

            document.getElementById("loganiimg").src = "/static/img/md.png";
            document.getElementById("bly").innerHTML = "Your Voice is recorded successfully";
            document.getElementById("bly").style.color = "#00FFEF"
            document.getElementById("loma").innerHTML = "Click Login button !";
            document.getElementById("wizard-sub").disabled = false;
            location.replace("http://localhost:5000/dashboard")
          }







        } else {

          document.getElementById("text").style.display = "block";
          var again = Record_btn();
        }


      }

      function Geolocation() {
        document.getElementById("adminlogin").style.display = "none";
        document.getElementById("locmethod").style.display = "none";
        document.getElementById("locani").style.display = "block";
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(showPosition);
        } else {

          alert("location is not supported by your browser");
        }

        function showPosition(position) {
          // x.innerHTML = "Latitude: " + position.coords.latitude + 
          // "<br>Longitude: " + position.coords.longitude;
          document.getElementById("long").value = position.coords.longitude;
          document.getElementById("lat").value = position.coords.latitude;


          document.getElementById("locaniimg").src = "/static/img/gpsdone.png";
          document.getElementById("loc-msg").innerHTML = "Location Recorded Successfully"
          document.getElementById("loc-per").innerHTML = "Click Next !";
          document.getElementById("wizard-nxt").disabled = false;
          document.getElementById("im-new").style.display = "none";

        }
      }