const searchInput = document.querySelector('.search-bar input');

if (searchInput) {
  searchInput.addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase().trim();
    const allCards = document.querySelectorAll('.project_container .card-item');

    let anyMatch = false;

    allCards.forEach(card => {
      const isPlaceholder = card.querySelector('#internshipSpan')?.hasAttribute('hidden');
      const titleEl = card.querySelector('.card-content-title p');
      const descEl = card.querySelector('.card-content-description p');

      if (isPlaceholder) {
        // Hide the placeholder by default — we'll show it later if needed
        card.style.display = 'none';
        return;
      }

      if (!titleEl || !descEl) return;

      const rawTitle = titleEl.textContent;
      const rawDesc = descEl.textContent;

      const titleMatch = rawTitle.toLowerCase().includes(searchTerm);
      const descMatch = rawDesc.toLowerCase().includes(searchTerm);

      if (searchTerm === '') {
        // Reset view — show all regular cards, hide placeholder
        card.style.display = 'block';
        titleEl.innerHTML = rawTitle;
        descEl.innerHTML = rawDesc;
        anyMatch = true;
      } else if (titleMatch || descMatch) {
        card.style.display = 'block';
        titleEl.innerHTML = highlightMatch(rawTitle, searchTerm);
        descEl.innerHTML = highlightMatch(rawDesc, searchTerm);
        anyMatch = true;
      } else {
        card.style.display = 'none';
      }
    });

    // Now toggle the placeholder visibility based on any matches
    allCards.forEach(card => {
      const isPlaceholder = card.querySelector('#internshipSpan')?.hasAttribute('hidden');
      if (isPlaceholder) {
        card.style.display = anyMatch ? 'none' : 'block';
      }
    });
  });
}

// Highlight helper
function highlightMatch(text, term) {
  const safeTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // escape regex chars
  const regex = new RegExp(`(${safeTerm})`, 'ig');
  return text.replace(regex, '<mark>$1</mark>');
}
