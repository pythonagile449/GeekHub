"use strict"

var intervalId = window.setInterval(checkNotificationsCount, 5000);

function checkNotificationsCount() {
    let notificationsCountBox = document.querySelector('#menu-notifications-counter');

    $.ajax({
        url: '/notifications/check-user-notifications-count/',
        success: data => {
            console.log(data);
            if (data.notifications_count > 0) {
                notificationsCountBox.innerHTML = data.notifications_count;
            } else {
                notificationsCountBox.innerHTML = '';
            }
        },
        error: error => {
            console.log(error)
        }
    })
}