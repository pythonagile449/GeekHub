"use stict"

document.addEventListener('DOMContentLoaded', () => {
    let toolBarLinks = document.querySelectorAll('ul.section-menu li a.link-menu');
    let url = document.location.href;

    toolBarLinks.forEach(link => {
        if (link.href === url) {
            link.classList.add('active-menu-link');
        }
    })
})