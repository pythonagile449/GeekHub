"use strict"

class Search {
    constructor() {
        this.searchForm = document.querySelector('.search-form');
        this.input = document.querySelector('.search-input');
        this.filtersLinks = document.querySelectorAll('.search-tab-link');
        this.requestParams = new URLSearchParams(location.search);
        this.targetType = this.requestParams.get('target_type') ? this.requestParams.get('target_type') : 'posts';
        this.setFocus();
        this.setHandlers();
        this.checkActiveTargetType();
    }


    setFocus() {
        this.input.focus();
        this.input.value = '';
        this.input.value = this.requestParams.get('q');
    }

    setHandlers() {
        this.searchForm.addEventListener('submit', evt => {
            location.href = `/search/?q=${this.input.value}&target_type=${this.targetType}`;
            evt.preventDefault()
        })

        this.input.addEventListener('keyup', evt => {
            if (evt.key === 'Enter') {
                console.log('entrr')
                // this.searchForm.action = `/search/?q=${this.input.value}&target_type=${this.targetType}/`;
                location.href = `/search/?q=${this.input.value}&target_type=${this.targetType}`;
        // this.searchForm.submit()
        evt.preventDefault()
        }
        })


        this.filtersLinks.forEach(link => {
            link.addEventListener('click', evt => {
                let target_type = link.dataset.targetType,
                    value = this.input.value;
                link.setAttribute('href', `/search/?q=${value}&target_type=${target_type}`);
            })
        })
    }

    checkActiveTargetType() {
        this.filtersLinks.forEach(link => {
            if (link.dataset.targetType === this.targetType) {
                link.setAttribute('style', 'color:red;');
            }
        })
    }
}

const search = new Search();