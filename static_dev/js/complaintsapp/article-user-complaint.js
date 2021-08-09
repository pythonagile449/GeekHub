"use strict"

class Complaint {
    constructor() {
        this.complaintContainer = document.querySelector('.complaint-container');
        this.showComplaintBoxButton = document.querySelector('.show-complaint-button');
        this.complaintInput = document.querySelector('.article-complaint-input');
        this.submitComplaintButton = document.querySelector('.submit-complaint-button');
        this.setHandlers();
    }

    setHandlers() {
        this.showComplaintBoxButton?.addEventListener('click', evt => {
            this.complaintContainer?.classList?.toggle('hidden');
            if (this.complaintInput) {
                this.complaintInput.value = '';
                this.complaintInput.focus();
            }
        })

        this.submitComplaintButton?.addEventListener('click', evt => {
            this.complaintContainer?.classList?.add('hidden');
            let articleId = evt.target.dataset.articleId;
            let message = this.complaintInput.value;
            $.ajax({
                url: `/complaint/create/?obj_id=${articleId}&message=${message}&instance=article`,
                success: data => {
                    console.log(data)
                    this.complaintInput.value = '';
                },
                error: err => {
                    console.log(err.responseJSON)
                }
            })
        })
    }
}

const complaint = new Complaint();