// Script para destacar o botão ativo baseado na URL atual
document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.main-nav a');
    
    links.forEach(link => {
        const href = link.getAttribute('href');
        if ((href === '/' && currentPath === '/') || 
            (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
