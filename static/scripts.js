// Code by chatgpt: animate content cards for landing page

document.addEventListener("DOMContentLoaded", function() {
    const blocks = document.querySelectorAll('.content-block');

    function checkVisibility() {
        const triggerBottom = window.innerHeight / 5 * 4;

        blocks.forEach(block => {
            const blockTop = block.getBoundingClientRect().top;

            if (blockTop < triggerBottom) {
                block.classList.add('visible');
            }
        });
    }

    window.addEventListener('scroll', checkVisibility);
    checkVisibility();
});
