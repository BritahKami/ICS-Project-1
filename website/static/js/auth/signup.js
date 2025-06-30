function contextchange(targetDivId) {
    const sections = document.querySelectorAll('.auth.division');
    sections.forEach(section => {
        if (section.id === targetDivId) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
}

// On page load, show student section by default
document.addEventListener('DOMContentLoaded', () => {
    contextchange('studentForm');
});