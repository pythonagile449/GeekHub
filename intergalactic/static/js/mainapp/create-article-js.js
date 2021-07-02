"use strict"

class Page {
    constructor() {
        this.form = document.querySelector('.create-article-form');
        this.saveAsDraftButton = document.querySelector('.save-as-draft-button');
        this.setHandlers();
    }

    setHandlers() {
        this.saveAsDraftButton.addEventListener('click', (evt) => {
            this.form.setAttribute('action', '/create-draft/');
            this.form.submit();
        })
    }
}

const page = new Page();