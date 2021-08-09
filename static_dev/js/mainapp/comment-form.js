import {CommentsRating} from './rating.js';
import {CommentUserComplaint} from "../complaintsapp/comment-user-complaint.js";

class Comment {
    constructor() {
        this.settings = {
            truncateCharsLength: 100,
        }
        this.commentForm = document.querySelector('.comment-form');
        this.commentSubmitButton = document.querySelector('.send-comment-button');
        this.showCommentsButton = document.querySelector('.show-all-comments-button');
        this.commentsTreeBlock = document.querySelector('.comments-tree-block');
        this.parentCommentSmall = document.querySelector('.parent-comment-small');
        this.parentCommentText = document.querySelector('.parent-comment-text');
        this.closeAnswerButton = document.querySelector(".close-answer-button");
        this.complaintButtons = document.querySelectorAll('.complaint-comment-button');
        this.complaint = new CommentUserComplaint();
        this.requestParams = new URLSearchParams(location.search);
        this.setHandlers();
        this.setAfterRenderHandlers();
        this.tryScrollTo();
    }

    tryScrollTo() {
        let scrollToComment = this.requestParams.get('scroll_to_comment');
        this.complaintAgainstComment = this.requestParams.get('complaint_against_comment');

        if (scrollToComment) {
            this.renderCommentsList().then(() => {
                location.href = `#comment-anchor-${scrollToComment}`;
                if (this.complaintAgainstComment) {
                    let commentNode = document.querySelector(`#comment-card-id-${scrollToComment}`)
                    this.highlightCommentBlock(commentNode);
                }
            })
        }
    }

    highlightCommentBlock(commentNode) {
        commentNode.classList.add('highlight');
    }

    renderCommentsList() {
        let articleId = this.commentsTreeBlock.dataset.articleId,
            url = `/comments/get-comments-tree/${articleId}/?complaint_against_comment=${this.complaintAgainstComment}`;

        return $.ajax({
            url: url,
            type: "GET",
            success: data => {
                $(`.comments-tree-root`).html(data)
                this.setAfterRenderHandlers();
                const commentsRating = new CommentsRating();
            },
            error: d => {
                console.log(d);
            }
        });
    }

    postComment(evt) {
        let formData = new FormData(this.commentForm);

        let articleId = evt.currentTarget.dataset.articleId,
            url = '/comments/create-comment/';
        formData.append('article_id', articleId);

        if (this.parentCommentText.innerHTML) {
            formData.append('parent_comment_id', this.currentParentId);
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: data => {
                this.renderCommentsList();
                $('.comments-counter').html(data.comments_count);
                this.resetAndCloseAnswerBlock();
                document.querySelector('#comments-start-point').scrollIntoView()
            },
            error: d => {
                console.log(d);
            }
        });
    }

    resetAndCloseAnswerBlock() {
        this.parentCommentText.innerHTML = '';
        this.parentCommentSmall.classList.add('hidden');
    }

    setHandlers() {
        const commentsRating = new CommentsRating();

        this.showCommentsButton?.addEventListener('click', evt => {
            this.renderCommentsList();
        })

        this.commentSubmitButton?.addEventListener('click', evt => {
            this.postComment(evt);
            this.commentForm.reset();
        })

        this.closeAnswerButton?.addEventListener('click', evt => {
            this.resetAndCloseAnswerBlock();
        })
    }

    setAfterRenderHandlers() {
        this.commentBlocks = document.querySelectorAll('.author-comment');
        this.answerButtons = document.querySelectorAll('.answer-button');
        this.complaintButtons = document.querySelectorAll('.complaint-comment-button');

        this.commentBlocks?.forEach(block => {
            block?.addEventListener('mouseenter', evt => {
                this.answerButton = evt.target.querySelector('.answer-button');
                this.complaintButton = evt.target.querySelector('.complaint-comment-button');
                this.answerButton?.classList.toggle('hidden');
                this.complaintButton?.classList.toggle('hidden');
            })

            block?.addEventListener('mouseleave', evt => {
                this.answerButton?.classList.toggle('hidden');
                this.complaintButton?.classList.toggle('hidden');
            })
        })

        this.answerButtons?.forEach(button => {
            button?.addEventListener('click', evt => {
                this.complaint.removeComplaintBlocks();
                this.parentCommentSmall.classList.remove('hidden');
                let text = evt.target.parentNode.parentNode.querySelector('.author-text p').textContent;
                text = this.truncateChars(text);
                document.querySelector('.comment-area').focus();
                this.parentCommentText.innerHTML = text;
                this.currentParentId = evt.currentTarget.dataset.answerTo;
            })
        })

        this.complaintButtons?.forEach(button => {
            button?.addEventListener('click', evt => {
                let drawToNode = evt.target.parentNode.parentNode;
                let commentId = evt.target.dataset.complaintTo;
                this.complaint.drawComplaintInputBlock(drawToNode, commentId);
            })
        })
    }

    truncateChars(str) {
        if (str.length > this.settings.truncateCharsLength) {
            return str.slice(0, this.settings.truncateCharsLength) + '...';
        }
        return str
    }

    hideActionButtons() {
        this.answerButtons.forEach(button => button.classList.add('hidden'));
        this.complaintButtons.forEach(button => button.classList.add('hidden'));
    }
}

const commentForm = new Comment();
export {commentForm};