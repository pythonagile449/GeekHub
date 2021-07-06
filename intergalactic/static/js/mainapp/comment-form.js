class Comment {
    constructor() {
        this.commentForm = document.querySelector('.comment-form');
        this.commentSubmitButton = document.querySelector('.send-comment-button');
        this.showCommentsButton = document.querySelector('.show-comments');
        this.commentsTreeBlock = document.querySelector('.comments-tree-block');
        this.parentCommentSmall = document.querySelector('.parent-comment-small');
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

    setAfterRenderHandlers() {
        this.commentBlocks = document.querySelectorAll('.author-comment');
        this.answerButton = '';

        this.commentBlocks.forEach(block => {
            block.addEventListener('mouseenter', evt => {
                // let answerButton = evt.target.querySelector('.answer-button');
                this.answerButton = evt.target.querySelector('.answer-button');
                this.answerButton.classList.toggle('hidden')

                this.answerButton.addEventListener('click', evt => {
                    document.querySelector('.comment-area').focus();
                    this.parentCommentSmall.classList.remove('hidden');
                    let text = block.querySelector('.author-text p');
                    console.log(text);
                })
            })

            block.addEventListener('mouseleave', evt => {
                // let answerButton = evt.target.querySelector('.answer-button');
                this.answerButton.classList.toggle('hidden')
            })
        })


    }
}

const commentForm = new Comment();