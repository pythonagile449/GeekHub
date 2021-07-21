"use strict";

const getTopData = () => {
    $.ajax({
            url: '/get-top-menu/',
            type: "GET",
            success: data => {
                $(`.section-right`).html(data);
            },
            error: d => {
                console.log(d);
            }
        });
}

const TopMenuConsumer = new WebSocket(
    'ws//'
    + window.location.host
    + '{{ active_hub }}'
    + '/'
);

document.addEventListener('DOMContentLoaded', () => {
        getTopData();
});

document.querySelector('.content-top-info').addEventListener('load', ()=>{
    setInterval(()=>{
        getTopData();
    }, 300000)
})
