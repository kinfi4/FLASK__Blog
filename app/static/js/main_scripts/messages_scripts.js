let messageBlock = document.getElementById('messages-block');

function move_messages(){
    let pos = -100;

    let id = setInterval(frame, 1);
    function frame(){
        if(pos == 20){
            clearInterval(id);
        }else{
            pos++;
            messageBlock.style.right = pos + 'px';
        }
    }
}

function smooth_hidding(){
    let pos = 60;
    let opacity = 1;

    let id = setInterval(frame, 2);
    function frame(){
        if(pos == 10){
            clearInterval(id);
            messageBlock.style.display = 'none'
        }else{
            pos--;
            opacity -= 0.03;
            messageBlock.style.top = pos + 'px';
            messageBlock.style.opacity = opacity;            
        }
    }
}

if(messageBlock != null){
    move_messages();

    messageBlock.onclick = function(event){
        let target = event.target;

        if(target.classList.contains('close-message')){
            smooth_hidding();
        }
    }

}
