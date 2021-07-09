import {CommentsRating} from './rating.js';

class Comment {
    constructor() {
        this.settings = {
            truncateCharsLength: 100,
        }
        this.commentForm = document.querySelector('.comment-form');
        this.commentSubmitButton = document.querySelector('.send-comment-button');
        this.showCommentsButton = document.querySelector('.show-comments');
        this.commentsTreeBlock = document.querySelector('.comments-tree-block');
        this.parentCommentSmall = document.querySelector('.parent-comment-small');
        this.parentCommentText = document.querySelector('.parent-comment-text');
        this.closeAnswerButton = document.querySelector(".close-answer-button")
        this.setHandlers();
    }

    renderCommentsList() {
        let articleId = this.commentsTreeBlock.dataset.articleId,
            url = `/comments/get-comments-tree/${articleId}`;

        $.ajax({
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
        this.showCommentsButton.addEventListener('click', evt => {
            this.commentsTreeBlock.classList.toggle('hidden');
            this.renderCommentsList();
        })

        if (this.commentSubmitButton) {
            this.commentSubmitButton.addEventListener('click', evt => {
                this.postComment(evt);
                this.commentForm.reset();
            })
        }

        this.closeAnswerButton.addEventListener('click', evt => {
            this.resetAndCloseAnswerBlock();
        })
    }

    setAfterRenderHandlers() {
        this.commentBlocks = document.querySelectorAll('.author-comment');
        this.answerButtons = document.querySelectorAll('.answer-button');

        this.commentBlocks.forEach(block => {
            block.addEventListener('mouseenter', evt => {
                this.answerButton = evt.target.querySelector('.answer-button');
                this.answerButton.classList.toggle('hidden');
            })

            block.addEventListener('mouseleave', evt => {
                this.answerButton.classList.toggle('hidden')
            })
        })

        this.answerButtons.forEach(button => {
            button.addEventListener('click', evt => {
                this.parentCommentSmall.classList.remove('hidden');
                let text = evt.target.parentNode.querySelector('.author-text p').textContent;
                text = this.truncateChars(text);
                document.querySelector('.comment-area').focus();
                this.parentCommentText.innerHTML = text;
                this.currentParentId = evt.currentTarget.dataset.answerTo;
            })
        })
    }

    truncateChars(str) {
        if (str.length > this.settings.truncateCharsLength) {
            return str.slice(0, this.settings.truncateCharsLength) + '...';
        }
        return str
    }
}

const commentForm = new Comment();