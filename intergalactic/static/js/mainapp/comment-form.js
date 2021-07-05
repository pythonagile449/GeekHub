class Comment {
    constructor() {
        this.commentForm = document.querySelector('.comment-form');
        this.commentSubmitButton = document.querySelector('.send-comment-button');
        this.showCommentsButton = document.querySelector('.show-comments');
        this.commentsTreeBlock = document.querySelector('.comments-tree-block');
        this.setHandlers();
    }

    sendAjax(url = '', method = '', formData = null, renderResultTo = '') {
        return $.ajax({
            url: url,
            type: method,
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: data => {
                console.log(data)
                if (renderResultTo) {
                    renderResultTo.insertAdjacentHTML('afterbegin', data);
                }
            },
            error: d => {
                console.log(d);
            }
        });
    }

    setHandlers() {
        this.showCommentsButton.addEventListener('click', evt => {
            this.commentsTreeBlock.classList.toggle('hidden');
            let articleId = this.commentsTreeBlock.dataset.articleId;
            let url = `/comments/get-comments-tree/${articleId}`;
            this.sendAjax(url, "GET", null, this.commentsTreeBlock);

        })

        if (this.commentSubmitButton) {
            this.commentSubmitButton.addEventListener('click', (evt => {
                let articleId = evt.currentTarget.dataset.articleId,
                    url = '/comments/create-comment/';

                let formData = new FormData(this.commentForm);
                formData.append('article_id', articleId);

                this.sendAjax(url, 'POST', formData, this.commentsTreeBlock)
            }))

        }
    }
}

const commentForm = new Comment();