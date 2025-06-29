// Function to show the FAQ answer
function showCardAns(event) {
    const faqCard = event.target.closest('.faq-card');
    const answer = faqCard.querySelector('.faq-card-a');
    const icon = event.target;

    // Show the answer and update the icon
    answer.classList.add('active');
    icon.classList.replace('bx-chevron-right', 'bx-chevron-down');
    icon.setAttribute('onclick', 'hideCardAns(event)');
}

// Function to hide the FAQ answer
function hideCardAns(event) {
    const faqCard = event.target.closest('.faq-card');
    const answer = faqCard.querySelector('.faq-card-a');
    const icon = event.target;

    // Hide the answer and update the icon
    answer.classList.remove('active');
    icon.classList.replace('bx-chevron-down', 'bx-chevron-right');
    icon.setAttribute('onclick', 'showCardAns(event)');
}