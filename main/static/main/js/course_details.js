document.addEventListener('DOMContentLoaded', function () {
    const topicCardsTitles = document.querySelectorAll('.topic-card h4');

    topicCardsTitles.forEach(cardTitle => {
        cardTitle.addEventListener('click', function () {
            // 'this' refers to the h4 element that was clicked
            const detailContent = this.nextElementSibling;
            const icon = this.querySelector('.topic-toggle-icon');

            if (detailContent && detailContent.classList.contains('topic-detail-content')) {
                if (detailContent.style.display === 'block') {
                    detailContent.style.display = 'none';
                    if (icon) {
                        icon.textContent = '+';
                        icon.classList.remove('expanded');
                    }
                } else {
                    detailContent.style.display = 'block';
                    if (icon) {
                        icon.textContent = '-';
                        icon.classList.add('expanded');
                    }
                }
            }
        });
    });
});
