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


if(messageBlock != null){
    move_messages();

    messageBlock.onclick = function(event){
        let target = event.target;

        if(target.classList.contains('close-message')){
            messageBlock.style.display = 'none';
        }
    }

}
