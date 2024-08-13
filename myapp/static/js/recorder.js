const mic_btn = document.querySelector('#mic');
const playback = document.querySelector('.playback');
const loading = document.querySelector('#loading');
mic_btn.addEventListener('click', ToggleMic);

let can_record = false;
let is_recording = false;
let recorder = null;
let chunks = [];

function SetupAudio(){
  console.log("Setup==============");
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({
      audio: true
    }).then(SetupStream)
    .catch(err => {
      console.log('eerroro', err);
    });
  }
}
SetupAudio();

function SetupStream(stream){
  recorder = new MediaRecorder(stream);

  recorder.ondataavailable = e => {
    playback.src= '';
    chunks.push(e.data);
  }
  recorder.onstop = e => {  
    loading.style.display = 'inline';
    const blob = new Blob(chunks, {type: 'audio/mp3'})
    chunks = [];

    console.log("start sending binary data...");
    var form = new FormData();
    form.append('file', blob);

    $.ajax({
        url: 'http://localhost:8000/upload',
        type: 'POST',
        data: form,
        processData: false,
        contentType: false,
        success: function (response, status, xhr) {
          loading.style.display = 'none';
          window.alert("success");
          playback.src= 'static/test.mp3';
        },
        error: function (err) {
          loading.style.display = 'none';
          window.alert("error"+ err);
          console.log("error", err);
          // handle error case here
        }
    });
    

    
  }
  can_record = true;
}

function ToggleMic(){
  if(!can_record) return;

  is_recording = !is_recording;

  if(is_recording){
    recorder.start();
    mic_btn.classList.add("is_recording");
  }else {
    recorder.stop();
    mic_btn.classList.add("stop_recording");
  }

}