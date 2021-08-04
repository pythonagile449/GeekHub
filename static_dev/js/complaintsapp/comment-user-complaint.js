"use strict"
import {commentForm} from "../mainapp/comment-form.js";


class CommentUserComplaint {

    getElements() {
        this.complaintForm = document.querySelector('.complaint-input-comment-block');
        this.complaintTextArea = document.querySelector('.complaint-against-comment-text');
        this.submitButton = document.querySelector('.submit-complaint-comment-button');
        this.closeBlockButton = document.querySelector('.close-block');
    }

    getHTML(commentId) {
        return `
            <div class="complaint-input-comment-block">
            <p>Оставить жалобу на комментарий:</p>
                <textarea class="complaint-against-comment-text" 
                    name="complaint-against-comment" cols="30" rows="10"></textarea>
                <button type="button" class="button23 submit-complaint-comment-button" data-comment-id="${commentId}">
                    Отправить жалобу
                </button>
                <span class="close-block">X</span>
            </div>
        `
    }

    removeComplaintBlocks() {
        document.querySelectorAll('.complaint-input-comment-block')?.forEach(el => el.remove());
    }

    drawComplaintInputBlock(node, commentId) {
        this.removeComplaintBlocks();
        node.insertAdjacentHTML('beforeend', this.getHTML(commentId));
        this.getElements();
        this.setHandlers();
    }

    setHandlers() {
        this.submitButton?.addEventListener('click', evt => {
            this.sendComplaint(evt);
            this.removeComplaintBlocks();
        });

        this.closeBlockButton?.addEventListener('click', () => {
            this.removeComplaintBlocks();
            commentForm.hideActionButtons();
        });
    }

    sendComplaint(evt) {
        let commentId = evt.currentTarget.dataset.commentId,
            message = this.complaintTextArea?.value;

        $.ajax({
            url: `/complaint/create/?obj_id=${commentId}&message=${message}&instance=comment`,
            success: data => {
                console.log(data.success);
            },
            error: d => {
                console.log(d);
            }
        });
    }
}

export {CommentUserComplaint}