// Get DOM elements
const modal = document.getElementById('addItems');
const addJob = document.getElementById('openModalBtn');
const addPath = document.getElementById('openModalBtn2')
const addGig = document.getElementById('openModalBtn3')
const addProject = document.getElementById('openModalBtn4')
const closeBtn = document.getElementById('closeBtn');

// Show modal
function showModal() {
    if (modal) {
        modal.style.display = 'block';
    }
}

// Hide modal
function closeModal(e) {
    // Preventing Default Submission
    e.preventDefault();

    if (modal) {
        modal.style.display = 'none';
    }
}

// Event listeners
if (addJob) addJob.addEventListener('click', showModal);
if (addPath) addPath.addEventListener('click', showModal);
if (addGig) addGig.addEventListener('click', showModal);
if (addProject) addProject.addEventListener('click', showModal);
if (closeBtn) closeBtn.addEventListener('click', closeModal);