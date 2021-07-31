"use strict"

class TopMenu {
    constructor() {
        this.getDomElements();
        this.getTopData(this.hubName, 'rating');
        this.updateBlockInterval = 300000;
        this.intervalId = window.setInterval(this.getTopData, this.updateBlockInterval, this.hubName);
        this.initHandlers();
    }

    getDomElements() {
        this.sectionRightBlock = document.querySelector('.section-right-block');
        this.hubName = document.querySelector('.section-title h2').innerText;
        this.dropDownMenu = document.querySelector('#top-menu-dropdown');
    }

    initHandlers() {
        this.dropDownMenu.addEventListener('click', evt => {
            let sortBy = evt.target.dataset.sortedBy;
            if (sortBy) this.getTopData(this.hubName, sortBy)
        })

    }

    getTopData(hubName, sortBy) {
        $.ajax({
            url: `/get-top-menu/${hubName}/?sorted_by=${sortBy}`,
            type: "GET",
            success: data => {
                $(`.section-right`).html(data);
                topMenu.getDomElements();
                topMenu.initHandlers();
            },
            error: d => {
                console.log(d);
            }
        });
    }
}

const topMenu = new TopMenu();