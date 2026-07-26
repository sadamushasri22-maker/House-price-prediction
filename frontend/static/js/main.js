/**
 * EstimaHouse AI - Interactive Client Script
 * Handles real-time form interactions and asynchronous API requests.
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const btnText = document.querySelector('.btn-text');
    const btnSpinner = document.querySelector('.btn-spinner');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        // Toggle spinner animation state
        if (btnText && btnSpinner) {
            btnText.classList.add('hidden');
            btnSpinner.classList.remove('hidden');
        }

        // Allow standard HTTP POST if JavaScript API fallback is needed
        // The form will post normally to /predict, rendering index.html with predictions
    });
});
