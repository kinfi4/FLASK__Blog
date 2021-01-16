let confirm_window = document.getElementById('confirm_window');
let delete_btn = document.getElementById('confirm-window-delete-btn');
let cancel_btn = document.getElementById('confirm-window-cancel-btn');


function hide_post_block(){
    document.getElementById('create_post').classList.remove('visible');
    document.getElementById('create_post').classList.add('hidden');
}

function cancel_btn_activate(){
    confirm_window.classList.add('hidden');
}

delete_btn.onclick = function(){
    hide_post_block();
    confirm_window.classList.add('hidden');

    document.getElementsByClassName('input-post-body')[0].textContent = '';
    document.getElementById('input-text').value = '';
}

cancel_btn.onclick = cancel_btn_activate

document.getElementById('confirm_window').onclick = function(event){
    let targer = event.target;
    if(targer == document.getElementById('confirm_window')){
        cancel_btn_activate();
    }
}
