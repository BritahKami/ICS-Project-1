// Get DOM elements
const modal = document.getElementById('addItems');
const addJob = document.getElementById('openModalBtn');
const addPath = document.getElementById('openModalBtn2')
const addGig = document.getElementById('openModalBtn3')
const addProject = document.getElementById('openModalBtn4')
const closeBtn = document.getElementById('closeBtn');
const optionSelect = document.getElementById('optionSelect');
const priceField = document.getElementById('priceField');


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
//Display or Hide price
if (optionSelect && priceField) {
    optionSelect.addEventListener('change', function () {
        if (this.value === 'gig') {
            priceField.style.display = 'block';
        } else {
            priceField.style.display = 'none';
        }
    });
}

// Event listeners
if (addJob) addJob.addEventListener('click', showModal);
if (addPath) addPath.addEventListener('click', showModal);
if (addGig) addGig.addEventListener('click', showModal);
if (addProject) addProject.addEventListener('click', showModal);
if (closeBtn) closeBtn.addEventListener('click', closeModal);

// Existing logic for student modal...
const editModal = document.getElementById('editStudentModal');
const openEditBtn = document.getElementById('editStudentBtn');
const closeEditBtn = document.getElementById('closeEditBtn');

if (openEditBtn) openEditBtn.addEventListener('click', () => {
    editModal.style.display = 'block';
});
if (closeEditBtn) closeEditBtn.addEventListener('click', (e) => {
    e.preventDefault();
    editModal.style.display = 'none';
});

// 🆕 Business Modal Logic
const businessModal = document.getElementById('editBusinessModal');
const openBusinessBtn = document.getElementById('editBusinessBtn');
const closeBusinessBtn = document.getElementById('closeBusinessBtn');

if (openBusinessBtn) openBusinessBtn.addEventListener('click', () => {
    businessModal.style.display = 'block';
});
if (closeBusinessBtn) closeBusinessBtn.addEventListener('click', (e) => {
    e.preventDefault();
    businessModal.style.display = 'none';
});

// Close Modals on Outside Click
window.addEventListener('click', function (e) {
    if (e.target === editModal) editModal.style.display = 'none';
    if (e.target === businessModal) businessModal.style.display = 'none';
});

