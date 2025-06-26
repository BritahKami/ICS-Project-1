const searchInput = document.querySelector('.search-bar input');

if (searchInput) {
  searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();

    //project search
    const projectContainer = document.querySelector('.project_container');
    if (projectContainer) {
      let noResultsMsg = projectContainer.querySelector('.no-results-msg');
      if (!noResultsMsg) {
        noResultsMsg = document.createElement('p');
        noResultsMsg.className = 'no-results-msg';
        noResultsMsg.textContent = 'No results found.';
        noResultsMsg.style.display = 'none';
        noResultsMsg.style.fontWeight = 'bold';
        noResultsMsg.style.color = 'red';
        projectContainer.appendChild(noResultsMsg);
      }

      const projects = document.querySelectorAll('.project1');
      let anyVisible = false;

      projects.forEach(project => {
        const titleElement = project.querySelector('.project_title h3');
        const descElement = project.querySelector('.project_description p');
        const titleText = titleElement.textContent;
        const descText = descElement.textContent;
        const titleMatch = titleText.toLowerCase().includes(searchTerm);
        const descMatch = descText.toLowerCase().includes(searchTerm);

        if (searchTerm === "") {
          titleElement.innerHTML = titleText;
          descElement.innerHTML = descText;
          project.style.display = 'block';
          anyVisible = true;
        } else if (titleMatch || descMatch) {
          titleElement.innerHTML = highlightMatch(titleText, searchTerm);
          descElement.innerHTML = highlightMatch(descText, searchTerm);
          project.style.display = 'block';
          anyVisible = true;
        } else {
          titleElement.innerHTML = titleText;
          descElement.innerHTML = descText;
          project.style.display = 'none';
        }
      });

      if (anyVisible) {
      noResultsMsg.style.display = 'none';
      } else {
      noResultsMsg.style.display = 'block';
      }

    }

  //jobs search
    const jobContainer = document.querySelector('.job_container');
    if (jobContainer) {
      let noResultsMsg = jobContainer.querySelector('.no-results-msg');
      if (!noResultsMsg) {
        noResultsMsg = document.createElement('p');
        noResultsMsg.className = 'no-results-msg';
        noResultsMsg.textContent = 'No results found.';
        noResultsMsg.style.display = 'none';
        noResultsMsg.style.fontWeight = 'bold';
        noResultsMsg.style.color = 'red';
        jobContainer.appendChild(noResultsMsg);
      }

      const jobs = document.querySelectorAll('.job1');
      let anyVisible = false;

      jobs.forEach(job => {
        const titleElement = job.querySelector('.job_title h3');
        const descElement = job.querySelector('.job_description p');
        const titleText = titleElement.textContent;
        const descText = descElement.textContent;
        const titleMatch = titleText.toLowerCase().includes(searchTerm);
        const descMatch = descText.toLowerCase().includes(searchTerm);

        if (searchTerm === "") {
          titleElement.innerHTML = titleText;
          descElement.innerHTML = descText;
          job.style.display = 'block';
          anyVisible = true;
        } else if (titleMatch || descMatch) {
          titleElement.innerHTML = highlightMatch(titleText, searchTerm);
          descElement.innerHTML = highlightMatch(descText, searchTerm);
          job.style.display = 'block';
          anyVisible = true;
        } else {
          titleElement.innerHTML = titleText;
          descElement.innerHTML = descText;
          job.style.display = 'none';
        }
      });

      if (anyVisible) {
      noResultsMsg.style.display = 'none';
      } else {
      noResultsMsg.style.display = 'block';
      }

    }
  });
}

function highlightMatch(text, term) {
  if (!term) return text;
   //Escape special characters in term to prevent regex issues
  const safeTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${safeTerm})`, 'ig');
  return text.replace(regex, '<mark>$1</mark>');
}
