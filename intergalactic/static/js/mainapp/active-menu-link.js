"use stict"

document.addEventListener('DOMContentLoaded', () => {
    let menuLinks = document.querySelectorAll('ul.menu-left li a.link-menu');
    let url = document.location.href;

    menuLinks.forEach(link => {
        if (link.href === url) {
            link.classList.add('active-menu-link');
        }
    })
})