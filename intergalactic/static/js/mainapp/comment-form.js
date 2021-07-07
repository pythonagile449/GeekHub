import {CommentsRating} from './rating.js';

class Comment {
    constructor() {
        this.commentForm = document.querySelector('.comment-form');
        this.commentSubmitButton = document.querySelector('.send-comment-button');
        this.showCommentsButton = document.querySelector('.show-comments');
        this.commentsTreeBlock = document.querySelector('.comments-tree-block');
        this.setHandlers();
    }

    renderCommentsList() {
        let articleId = this.commentsTreeBlock.dataset.articleId,
            url = `/comments/get-comments-tree/${articleId}`;

        $.ajax({
            url: url,
            type: "GET",
            success: data => {
                // console.log(data)
                $(`.comments-tree-root`).html(data);
                const commentsRating = new CommentsRating();
            },
            error: d => {
                console.log(d);
            }
        });
    }

    postComment(evt) {
        let articleId = evt.currentTarget.dataset.articleId,
            url = '/comments/create-comment/';

        let formData = new FormData(this.commentForm);
        formData.append('article_id', articleId);

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: data => {
                console.log(data);
                this.renderCommentsList();
                $('.comments-counter').html(data.comments_count);
            },
            error: d => {
                console.log(d);
            }
        });
    }

    setHandlers() {
        this.showCommentsButton.addEventListener('click', evt => {
            this.commentsTreeBlock.classList.toggle('hidden');
            this.renderCommentsList();
        })

        if (this.commentSubmitButton) {
            this.commentSubmitButton.addEventListener('click', (evt => {
                this.postComment(evt);
                this.commentForm.reset();
            }))

        }
    }
}

const commentForm = new Comment();