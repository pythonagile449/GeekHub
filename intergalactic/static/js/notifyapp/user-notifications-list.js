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
        if (this.selectAllCheckbox) {
            this.selectAllCheckbox.onchange = () => {
                this.deleteNotificationButton.disabled = !this.selectAllCheckbox.checked;
                this.notificationsCheckboxes.forEach(checkbox => {
                    checkbox.checked = this.selectAllCheckbox.checked;
                });
            }
        }

        if (this.notificationsCheckboxes) {
            this.notificationsCheckboxes.forEach(checkbox => {
                checkbox.onchange = () => {
                    this.deleteNotificationButton.disabled = !checkbox.checked;
                }
            })
        }

        if (this.deleteNotificationButton) {
            this.deleteNotificationButton.addEventListener('click', evt => {
                this.checkedNotifications = [];
                this.notificationsCheckboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        this.checkedNotifications.push(checkbox.dataset.notificationId);
                    }
                });
                let formData = this.getFormData();
                this.pushCheckedIds(formData);
                this.sendDeleteRequest(formData);
            })
        }
    }

    getFormData() {
        let form = document.querySelector('.notifications-content');
        let formData = new FormData(form);
        return formData;
    }

    pushCheckedIds(formData) {
        formData.append('ids', JSON.stringify(this.checkedNotifications));
    }

    sendDeleteRequest(formData) {
        $.ajax({
            url: '/notifications/delete-notifications/',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: data => {
                location.reload();
            },
            error: d => {
                console.log(d);
            }
        })
    }
}

const userNotifications = new UserNotifications();