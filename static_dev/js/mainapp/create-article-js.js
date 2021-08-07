"use strict"

var firstFormState = {}

document.addEventListener('DOMContentLoaded', () => {
    firstFormState = {
        title: document.querySelector('#id_title')?.value,
        hub: document.querySelector('#id_hub').value,
        content: document.querySelector('.create-article-form').elements.contents.value,
    }
    CKEDITOR.on('instanceReady', () => {
        firstFormState.content = CKEDITOR.instances["id_contents"].getData();
    })
})

window.onbeforeunload = (evt) => {
    let endFirmTitle = document.querySelector('#id_title')?.value,
        endHub = document.querySelector('#id_hub')?.value,
        endContent = document.querySelector('.create-article-form').elements.contents.value;

    if (CKEDITOR.instances["id_contents"] !== undefined) {
        endContent = CKEDITOR.instances["id_contents"].getData();
    }

    if (firstFormState.title === endFirmTitle && firstFormState.hub === endHub && firstFormState.content === endContent) {
        evt.preventDefault();
    } else {
        if (page.isActionButtonClicked) {
            evt.preventDefault();
        } else {
            return 'Changes will not be saved!';
        }
    }
}


class Page {
    constructor() {
        this.form = document.querySelector('.create-article-form');
        this.publishArticleButton = document.querySelector('.publish-article-button');
        this.saveAsDraftButton = document.querySelector('.save-as-draft-button');
        this.saveEditDraftButton = document.querySelector('#save-editing-draft-button');
        this.answerBlock = document.querySelector('.answer');
        this.isActionButtonClicked = false;
        this.setHandlers();
    }


    setHandlers() {
        if (this.publishArticleButton) {
            this.publishArticleButton.addEventListener('click', evt => {
            })
        }

        if (this.saveAsDraftButton) {
            this.saveAsDraftButton.addEventListener('click', (evt) => {
                this.isActionButtonClicked = true;
                this.form.setAttribute('action', '/create-draft/');
                this.form.submit();
            })
        }

        if (this.saveEditDraftButton) {
            this.saveEditDraftButton.addEventListener('click', (evt) => {
                this.isActionButtonClicked = true;
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
