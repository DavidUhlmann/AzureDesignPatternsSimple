function resetSessionAndReload() {
    fetch('/reset_session', {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to reset session');
        }
        window.location = '/restart';  // Adjust the URL if necessary
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var repeatQuizButton = document.getElementById('repeat-quiz-btn');
    if (repeatQuizButton) {
        repeatQuizButton.addEventListener('click', resetSessionAndReload);
    }
});

function initHomePage() {
    const updateProgress = () => {
        fetch('/progress')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const progressTableBody = document.getElementById('progress-table-body');
                progressTableBody.innerHTML = '';
                const progressRow = document.createElement('tr');

                const totalPatternsCell = document.createElement('td');
                totalPatternsCell.textContent = data.total_patterns;
                progressRow.appendChild(totalPatternsCell);

                const loadedPatternsCell = document.createElement('td');
                loadedPatternsCell.textContent = data.loaded_patterns;
                progressRow.appendChild(loadedPatternsCell);

                progressTableBody.appendChild(progressRow);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    };

    document.getElementById('scrape-button').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('load-button').disabled = true;
        fetch('/load', { method: 'POST', body: new FormData(event.target.form) })
            .then(() => {
                updateProgress();
            });
    });

    setInterval(updateProgress, 5000);
}

// Call initHomePage to initialize everything
initHomePage();