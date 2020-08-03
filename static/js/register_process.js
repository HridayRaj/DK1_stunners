document.getElementById("rbb1").addEventListener("click", R1);
document.getElementById("rr1").addEventListener("click", Ret1);

document.getElementById("rbb2").addEventListener("click", R2);
document.getElementById("rr2").addEventListener("click", Ret2);


document.getElementById("rbb3").addEventListener("click", R3);
document.getElementById("rr3").addEventListener("click", Ret3);






  //webkitURL is deprecated but nevertheless
  URL = window.URL || window.webkitURL;

  var gumStream; //stream from getUserMedia()
  var rec; //Recorder.js object
  var input; //MediaStreamAudioSourceNode we'll be recording

  // shim for AudioContext when it's not avb. 
  var AudioContext = window.AudioContext || window.webkitAudioContext;
  var audioContext; //audio context to help us record

  /*
      Simple constraints object, for more advanced audio features see
      https://addpipe.com/blog/audio-constraints-getusermedia/
  */

 




function R1() {
    var constraints = {
        audio: true,
        video: false
    };
  


    /*
        We're using the standard promise based getUserMedia() 
        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

    navigator.mediaDevices.getUserMedia(constraints);

    document.getElementById('rb1').style.display = 'none';
    document.getElementById('rt1').style.display = 'block';


    var timeLeft = 3;
    var elem = document.getElementById('timer');
    var timerId = setInterval(countdown, 1000);

    function countdown() {
        if (timeLeft == -1) {
            clearTimeout(timerId);
            doSomething1();
        } else {
            elem.innerHTML = timeLeft + ' sec';
            timeLeft--;
        }
    }

    function doSomething1() {
        document.getElementById('rt1').style.display = 'none';
        document.getElementById('rn1').style.display = 'block';
        document.getElementById('rbl1').style.display = 'block';
        Record1();
    }



    function Record1() {
        // start recording here
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

            //tell the recorder to stop the recording
            rec.stop();
            document.getElementById('rn1').style.display = 'none';
            document.getElementById('rbl1').style.display = 'none';
            document.getElementById('rbb1').innerHTML = 'First Voice Sample';
            document.getElementById('rb1').style.display = 'block';
            document.getElementById('rbb1').disabled = true;
            document.getElementById('rr1').style.display = 'inline-block';
            document.getElementById('rti1').style.display = 'inline-block';
            if (document.getElementById('rti2').style.display == 'inline-block' && document.getElementById('rti3').style.display == 'inline-block'){
                document.getElementById('regBtn').style.display = 'block';
            }




            //stop microphone access
            gumStream.getAudioTracks()[0].stop();

            //create the wav blob and pass it on to createDownloadLink
            rec.exportWAV(createDownloadLink);
            document.getElementById('rbb2').disabled = false;

        }

        function createDownloadLink(blob) {


            //name of .wav file to use during upload and download (without extendion)
            var filename = new Date().toISOString();



            //upload link



            var xhr = new XMLHttpRequest();
            xhr.onload = function (e) {
                if (this.readyState === 4) {
                    console.log("Server returned: ", e.target.responseText);
                }
            };
            var fd = new FormData();
            fd.append("audio_data", blob, filename);
            xhr.open("POST", "/rec1", true);
            xhr.send(fd);
           




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
                



            }










        }
    }
    
}

function Ret1() {
    document.getElementById('rbb2').disabled = true;
    document.getElementById('rti1').style.display = 'none';
    document.getElementById('rr1').style.display = 'none';
    document.getElementById("regBtn").style.display = "none";
    R1();

}

























function R2() {

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

    document.getElementById('rb2').style.display = 'none';
    document.getElementById('rt2').style.display = 'block';


    var timeLeft = 3;
    var elem = document.getElementById('timer2');
    var timerId = setInterval(countdown2, 1000);

    function countdown2() {
        if (timeLeft == -1) {
            clearTimeout(timerId);
            doSomething2();
        } else {
            elem.innerHTML = timeLeft + ' sec';
            timeLeft--;
        }
    }

    function doSomething2() {
        document.getElementById('rt2').style.display = 'none';
        document.getElementById('rn2').style.display = 'block';
        document.getElementById('rbl2').style.display = 'block';
        Record2();
    }



    function Record2() {
        // start recording here
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
            alert("Unable to Record !!!");
        });


        var stopLeft = 3;
        var elem = document.getElementById('timer2');
        var timerIdstop = setInterval(countstop2, 1000);

        function countstop2() {
            if (stopLeft == -1) {
                clearTimeout(timerIdstop);
                dostop2();
            } else {
                elem.innerHTML = stopLeft + ' sec';
                stopLeft--;
            }
        }

        function dostop2() {

            //tell the recorder to stop the recording
            rec.stop();
            document.getElementById('rn2').style.display = 'none';
            document.getElementById('rbl2').style.display = 'none';
            document.getElementById('rbb2').innerHTML = 'Second Voice Sample';
            document.getElementById('rb2').style.display = 'block';
            document.getElementById('rbb2').disabled = true;
            document.getElementById('rr2').style.display = 'inline-block';
            document.getElementById('rti2').style.display = 'inline-block';
            if (document.getElementById('rti1').style.display == 'inline-block' && document.getElementById('rti3').style.display == 'inline-block'){
                document.getElementById('regBtn').style.display = 'block';
            }



            //stop microphone access
            gumStream.getAudioTracks()[0].stop();

            //create the wav blob and pass it on to createDownloadLink
            rec.exportWAV(createDownloadLink);
            document.getElementById('rbb3').disabled = false;

        }

        function createDownloadLink(blob) {


            //name of .wav file to use during upload and download (without extendion)
            var filename = new Date().toISOString();



            //upload link



            var xhr = new XMLHttpRequest();
            xhr.onload = function (e) {
                if (this.readyState === 4) {
                    console.log("Server returned: ", e.target.responseText);
                }
            };
            var fd = new FormData();
            fd.append("audio_data", blob, filename);
            xhr.open("POST", "/rec2", true);
            xhr.send(fd);





            var loginLeft = 3;
            var elem = document.getElementById('timer2');
            var timerIdlogin = setInterval(countlogin, 1000);

            function countlogin() {
                if (loginLeft == -1) {
                    clearTimeout(timerIdlogin);
                    dologin2();
                } else {
                    elem.innerHTML = loginLeft + ' sec';
                    loginLeft--;
                }
            }

            function dologin2() {



            }










        }
    }
}

function Ret2() {
    document.getElementById('rbb3').disabled = true;
    document.getElementById('rti2').style.display = 'none';
    document.getElementById('rr2').style.display = 'none';
    document.getElementById("regBtn").style.display = "none";
    R2();

}
























function R3() {

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

    document.getElementById('rb3').style.display = 'none';
    document.getElementById('rt3').style.display = 'block';


    var timeLeft = 3;
    var elem = document.getElementById('timer3');
    var timerId = setInterval(countdown3, 1000);

    function countdown3() {
        if (timeLeft == -1) {
            clearTimeout(timerId);
            doSomething3();
        } else {
            elem.innerHTML = timeLeft + ' sec';
            timeLeft--;
        }
    }

    function doSomething3() {
        document.getElementById('rt3').style.display = 'none';
        document.getElementById('rn3').style.display = 'block';
        document.getElementById('rbl3').style.display = 'block';
        Record3();
    }



    function Record3() {
        // start recording here
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
        var elem = document.getElementById('timer3');
        var timerIdstop = setInterval(countstop3, 1000);

        function countstop3() {
            if (stopLeft == -1) {
                clearTimeout(timerIdstop);
                dostop3();
            } else {
                elem.innerHTML = stopLeft + ' sec';
                stopLeft--;
            }
        }

        function dostop3() {

            //tell the recorder to stop the recording
            rec.stop();
            document.getElementById('rn3').style.display = 'none';
            document.getElementById('rbl3').style.display = 'none';
            document.getElementById('rbb3').innerHTML = 'Third Voice Sample';
            document.getElementById('rb3').style.display = 'block';
            document.getElementById('rbb3').disabled = true;
            document.getElementById('rr3').style.display = 'inline-block';
            document.getElementById('rti3').style.display = 'inline-block';
            // document.getElementById("regBtn").style.display = "block";
            if (document.getElementById('rti1').style.display == 'inline-block' && document.getElementById('rti2').style.display == 'inline-block'){
                document.getElementById('regBtn').style.display = 'block';
            }
            



            //stop microphone access
            gumStream.getAudioTracks()[0].stop();

            //create the wav blob and pass it on to createDownloadLink
            rec.exportWAV(createDownloadLink);

        }

        function createDownloadLink(blob) {


            //name of .wav file to use during upload and download (without extendion)
            var filename = new Date().toISOString();



            //upload link



            var xhr = new XMLHttpRequest();
            xhr.onload = function (e) {
                if (this.readyState === 4) {
                    console.log("Server returned: ", e.target.responseText);
                }
            };
            var fd = new FormData();
            fd.append("audio_data", blob, filename);
            xhr.open("POST", "/rec3", true);
            xhr.send(fd);





            var loginLeft = 3;
            var elem = document.getElementById('timer3');
            var timerIdlogin = setInterval(countlogin, 1000);

            function countlogin() {
                if (loginLeft == -1) {
                    clearTimeout(timerIdlogin);
                    dologin3();
                } else {
                    elem.innerHTML = loginLeft + ' sec';
                    loginLeft--;
                }
            }

            function dologin3() {



            }










        }
    }
}

function Ret3() {
    document.getElementById('rti3').style.display = 'none';
    document.getElementById('rr3').style.display = 'none';
    document.getElementById("regBtn").style.display = "none";
    R3();

}