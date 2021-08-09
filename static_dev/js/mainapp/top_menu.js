"use strict"

class TopMenu {
    constructor() {
        this.getDomElements();
        const cookie = this.getCookie();
        this.getTopData(this.hubName, cookie);
        this.updateBlockInterval = 300000;
        this.intervalId = window.setInterval(this.getTopData, this.updateBlockInterval, this.hubName);
        this.initHandlers();
    }

    getDomElements() {
        this.sectionRightBlock = document.querySelector('.section-right-block');
        this.hubName = document.querySelector('.section-title h2').innerText;
        this.dropDownMenu = document.querySelector('#top-menu-dropdown');
        this.topTitle = document.querySelector('.top-info-title');
    }

    setTopInfoTitle(sortBy) {
        switch (sortBy) {
            case 'rating':
                this.topTitle.innerHTML = `<h6-2>По рейтингу</h6-2>`;
                break;
            case 'date':
                this.topTitle.innerHTML = `<h6-2>По дате</h6-2>`;
                break;
            case 'views':
                this.topTitle.innerHTML = `<h6-2>По просмотрам</h6-2>`;
                break;
            case 'comments':
                this.topTitle.innerHTML = `<h6-2>По комментариям</h6-2>`;
                break;
            default:
                this.topTitle.innerHTML = `<h6-2>Топ-лист</h6-2>`;
                break;

        }
    }

    initHandlers() {
        this.dropDownMenu.addEventListener('click', evt => {
            let sortBy = evt.target.dataset.sortedBy;
            this.setTopInfoTitle(sortBy);
            if (sortBy) this.getTopData(this.hubName, sortBy)
        });

    }

    setCookie(sortBy) {
        document.cookie = `sorted=${sortBy}`;
    }

    getCookie() {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; sorted=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift()
        } else return 'rating'
    }

    getTopData(hubName, sortBy) {
        $.ajax({
            url: `/get-top-menu/${hubName}/?sorted_by=${sortBy}`,
            type: "GET",
            success: data => {
                $(`.section-right`).html(data);
                topMenu.getDomElements();
                topMenu.setTopInfoTitle(sortBy);
                topMenu.initHandlers();
                topMenu.setCookie(sortBy);
            },
            error: d => {
                console.log(d);
            }
        });
    }
}

const topMenu = new TopMenu();