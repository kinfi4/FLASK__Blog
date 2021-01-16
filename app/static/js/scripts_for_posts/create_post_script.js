let formBlock = document.getElementById('form-block');
let input_body = document.getElementsByClassName('input-post-body')[0];
let form_input = document.getElementById('input-text');

function hide_post_block(){
    document.getElementById('create_post').classList.remove('visible');
    document.getElementById('create_post').classList.add('hidden');
}

function show_confirm_window(){
    if(input_body.textContent != ''){
        document.getElementById('confirm_window').classList.remove('hidden');
    }
    else{
        hide_post_block();
    }
}


document.getElementsByClassName('show-form-btn')[0].onmousedown = function(event){
    let createPost = document.getElementById('create_post');
    createPost.classList.remove('hidden');
    createPost.classList.add('visible');
}

document.getElementById('create_post').onclick = function(event){
    let targer = event.target;
    if(targer == document.getElementById('create_post')){
        show_confirm_window();
    }
}

document.getElementById('close').onclick = function(){
    show_confirm_window();
}

document.getElementsByClassName('input-post-body')[0].oninput = function(){
    form_input.value = input_body.textContent;
}
