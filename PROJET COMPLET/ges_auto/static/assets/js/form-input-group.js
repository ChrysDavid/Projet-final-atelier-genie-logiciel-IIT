(()=>{var n,t,s,e=$(".speech-to-text");e.length&&null!=(n=n||webkitSpeechRecognition)&&(t=new n,s=!1,e.on("click",function(){let e=$(this);!(t.onspeechstart=function(){s=!0})===s&&t.start(),t.onerror=function(n){s=!1},t.onresult=function(n){e.closest(".form-send-message").find(".message-input").val(n.results[0][0].transcript)},t.onspeechend=function(n){s=!1,t.stop()}}))})();