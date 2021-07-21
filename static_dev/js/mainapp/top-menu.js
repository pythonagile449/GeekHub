"use strict";

const getTopData = (hub) => {
    $.ajax({
        url: '/get-top-menu/' + hub,
        type: "GET",
        success: data => {
            $(`.section-right`).html(data);
        },
        error: d => {
            console.log(d);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const topMenu = document.querySelector('.section-right-block');
    let hubName = document.querySelector('.section-title h2').innerText;
    // let chosenMenu;

    getTopData(hubName);

    // document.querySelector('#top-menu-dropdown').addEventListener('click', e => {
    //     e.preventDefault();
    //     if (e.target.tagName === 'A'){
    //         chosenMenu = e.target.value;
    //         console.log(chosenMenu);
    //     }
    // });

    topMenu.querySelector('.content-top-info').addEventListener('load', () => {
        setInterval(() => {
            getTopData(hubName);
        }, 300000);
    })
});


