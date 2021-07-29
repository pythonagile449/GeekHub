class TopMenu {
    constructor() {
        this.getDomeElements();
        this.getTopData();
        this.updateBlockInterval = 300000;
        this.intervalId = window.setInterval(this.getTopData, this.updateBlockInterval, this.hubName);
        this.initHandlers();
    }

    getDomeElements() {
        this.sectionRightBlock = document.querySelector('.section-right-block');
        this.hubName = document.querySelector('.section-title h2').innerText;
        this.dropDownMenu = document.querySelector('#top-menu-dropdown');
    }

    initHandlers() {
        this.dropDownMenu.addEventListener('click', evt => {
            console.log(evt);
            console.log(this.hubName);
        })

    }

    getTopData() {
        $.ajax({
            url: '/get-top-menu/' + this.hubName,
            type: "GET",
            success: data => {
                $(`.section-right`).html(data);
                topMenu.getDomeElements();
                topMenu.initHandlers();
            },
            error: d => {
                console.log(d);
            }
        });
    }
}

const topMenu = new TopMenu();

