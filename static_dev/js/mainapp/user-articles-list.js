"use strict"

class UserArticlesTable {
    constructor() {
        this.articleRows = document.querySelectorAll('.article-row');
        this.setHandlers();
    }

    setHandlers() {
        if (this.articleRows) {
            this.articleRows.forEach(row => {
                row.addEventListener('mouseenter', evt => {
                    this.actionsButtons = evt.target.querySelector('.cell-actions');
                    this.dateCell = evt.target.querySelector('.cell-date');
                    let blockWidth = this.dateCell.offsetWidth;
                    this.dateCell.classList.toggle('hidden');
                    // this.actionsButtons.style.width = `${blockWidth}px`;
                    this.actionsButtons.classList.toggle('hidden');
                });

                row.addEventListener('mouseleave', evt => {
                    this.dateCell.classList.toggle('hidden');
                    this.actionsButtons.classList.toggle('hidden');
                });

            })
        }
    }
}

const userArticlesTable = new UserArticlesTable();