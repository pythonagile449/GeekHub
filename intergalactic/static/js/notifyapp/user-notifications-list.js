"use strict"

class UserNotifications {
    constructor() {
        this.selectAllCheckbox = document.querySelector('#select-all-checkbox');
        this.notificationsCheckboxes = document.querySelectorAll('.notification-checkbox');
        this.deleteNotificationButton = document.querySelector('#delete-notification-button');
        this.checkedNotifications = [];
        this.setHandlers();
    }

    setHandlers() {
        this.selectAllCheckbox.onchange = () => {
            this.notificationsCheckboxes.forEach(checkbox => {
                checkbox.checked = this.selectAllCheckbox.checked ? true : false;
            });
        };

        this.deleteNotificationButton.addEventListener('click', evt => {
            this.checkedNotifications = [];
            this.notificationsCheckboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    this.checkedNotifications.push(checkbox.dataset.notificationId);
                }
            });
        })
    }
}

const userNotifications = new UserNotifications();