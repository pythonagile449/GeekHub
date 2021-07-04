class Comment {
    constructor() {
        this.commentForm = document.querySelector('.comment-form');
        this.commentSubmitButton = document.querySelector('.send-comment-button');
        this.setHandlers();
    }

    setHandlers() {
        if (this.commentSubmitButton) {
            this.commentSubmitButton.addEventListener('click', (evt => {
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
                        console.log(data)
                    },
                    error: d => {
                        console.log(d);
                    }
                });
            }))

        }
    }
}

const commentForm = new Comment();