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
            <div class="wrapper-absolute">
                <div class="comment-complaint-title">
                    <h5-1>Оставить жалобу на комментарий:</h5-1>
                </div>
                <div class="field-comment-complaint" style="background-color: rgba(255, 122, 0, 0.2)">
                    <textarea class="complaint-against-comment-text"
                        name="complaint-against-comment" cols="30" rows="10" maxlength="500"></textarea>
                </div>
                <button type="button" class="button23-c submit-complaint-comment-button" data-comment-id="${commentId}">
                    Отправить жалобу
                </button>
                <span class="close-block" title="Закрыть">
                    <svg class="icon-X">
                        <use xlink:href="#check-box2"></use>
                    </svg>
                </span>
            </div>
            </div>
        `
    }

    removeComplaintBlocks() {
        document.querySelectorAll('.complaint-input-comment-block')?.forEach(el => el.remove());
    }

    drawComplaintInputBlock(node, commentId) {
        this.removeComplaintBlocks();
        node.insertAdjacentHTML('afterbegin', this.getHTML(commentId));
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
                commentForm.hideActionButtons();
                $('.modal-content').html(data.success);
                $("#modal-articles").modal("show");
            },
            error: d => {
                console.log(d);
                commentForm.hideActionButtons();

            }
        });
    }
}

export {CommentUserComplaint}