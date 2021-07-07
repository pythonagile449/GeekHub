// "use strict"

// $('.create-article-form').data('serialize', $('.create-article-form').serialize()); // On load save form current state
//
// $(window).bind('beforeunload', function (e) {
//     if ($('.create-article-form').serialize() != $('.create-article-form').data('serialize')) return true;
//     else e = null; // i.e; if form state change show warning box, else don't show it.
// });

class Page {
    constructor() {
        this.form = document.querySelector('.create-article-form');
        this.publishArticleButton = document.querySelector('.publish-article-button');
        this.saveAsDraftButton = document.querySelector('.save-as-draft-button');
        this.saveEditDraftButton = document.querySelector('#save-editing-draft-button');
        this.answerBlock = document.querySelector('.answer');
        this.setHandlers();
    }

    setHandlers() {
        if (this.publishArticleButton) {
            this.publishArticleButton.addEventListener('click', evt => {
            })
        }

        if (this.saveAsDraftButton) {
            this.saveAsDraftButton.addEventListener('click', (evt) => {
                this.form.setAttribute('action', '/create-draft/');
                this.form.submit();
            })
        }

        if (this.saveEditDraftButton) {
            this.saveEditDraftButton.addEventListener('click', (evt) => {
                let uuid = evt.currentTarget.dataset.uuid;
                let url = `/edit-draft/${uuid}/`;
                let form_data = new FormData(this.form);

                if (CKEDITOR.instances["id_contents"] !== undefined) {
                    let ckeditorData = CKEDITOR.instances["id_contents"].getData();
                    form_data.append('contents', ckeditorData);
                }

                $.ajax({
                    url: url,
                    type: 'POST',
                    data: form_data,
                    cache: false,
                    processData: false,
                    contentType: false,
                    enctype: 'multipart/form-data',
                    success: data => {
                        if (data === 'Success') {
                            this.answerBlock.classList.remove('error');
                            this.answerBlock.classList.remove('hidden');
                            $('.answer').html('Черновик сохранен');
                        }

                        if (data === 'Error') {
                            this.answerBlock.classList.remove('hidden');
                            this.answerBlock.classList.add('error');
                            $('.answer').html('Черновик не сохранен, заполните все обязательные поля.');
                        }
                    },
                    error: d => {
                        console.log(d);
                    }
                });
            })
        }

    }
}

const page = new Page();

