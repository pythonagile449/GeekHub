"use strict"

class Search {
    constructor() {
        this.input = document.querySelector('.search-input');
        this.setFocus();
    }


    setFocus() {
        let startValue = this.input.value;
        this.input.focus();
        this.input.value = '';
        this.input.value = startValue;
    }
}

const search = new Search();