"use strict"

class Page {
    constructor() {
        this.is_form_changed = false;
        this.form = document.querySelector('.create-article-form');
        this.publishArticleButton = document.querySelector('.publish-article-button');
        this.saveAsDraftButton = document.querySelector('.save-as-draft-button');
        this.saveEditDraftButton = document.querySelector('#save-editing-draft-button');
        this.answerBlock = document.querySelector('.answer');

        this.inputTitle = document.querySelector('#id_title');
        this.selectHab = document.querySelector('#id_hub');
        this.textAreaCK = document.querySelector('#cke_1_contents');
        this.firstFormState = {
            title: this.inputTitle.value,
            hub: this.selectHab.value,
            content: this.textAreaCK?.value,
        }

        this.setHandlers();
        this.listenFormInputs();
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

    listenFormInputs() {
        this.inputTitle?.addEventListener('change', () => this.is_form_changed = true);
        this.selectHab?.addEventListener('change', () => this.is_form_changed = true);
        this.textAreaCK?.addEventListener('change', () => console.log('change textarea'));
        console.log(this.is_form_changed);
        console.log(this.firstFormState);
    }
}

const page = new Page();

