let tabs;
let urlParams;

window.onload = function(){
    tabs = document.getElementsByClassName('filter-posts-title');
    urlParams = new URLSearchParams(window.location.search);

    deactivate_all_tabs()

    if(urlParams.get('sort_by') == 'world'){
        tabs[0].classList.add('active');
    }
    else if(urlParams.get('sort_by') == 'country'){
        tabs[1].classList.add('active');
    }
    else if(urlParams.get('sort_by') == 'following'){
        tabs[2].classList.add('active');
    }else{
        tabs[0].classList.add('active');
    }
}

function deactivate_all_tabs(){
    for(let i = 0; i < tabs.length; i++){
        tabs[i].classList.remove('active');
    }
}

document.getElementById('filter-block').onclick = function(event){
    let target = event.target;
    for(let i = 0; i < tabs.length; i++){
        if(tabs[i] == target){
            deactivate_all_tabs();
            target.classList.add('active');

            break;
        }
    }
}