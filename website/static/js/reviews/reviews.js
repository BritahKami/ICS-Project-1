// Get DOM elements
const reviewContainer = document.getElementById('review_container');
const addReview= document.getElementById('review-button');
const closeButton = document.getElementById('close_btn');

// Show modal
function showModal() {
    if (reviewContainer) {
        reviewContainer.style.display = 'block';
    }
}

// Hide reviewContainer
function closeModal(e) {
    // Preventing Default Submission
    e.preventDefault();

    if (reviewContainer) {
        reviewContainer.style.display = 'none';
    }
}

// Event listeners
if (addReview) addReview.addEventListener('click', showModal);
if (closeButton) closeButton.addEventListener('click', closeModal);