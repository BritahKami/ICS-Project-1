// addgigs details
const add_gig_btn= document.getElementById('add_gig_btn');
const addgigs_container= document.querySelector('.addgigs_container');
const close_gig_btn= document.getElementById('close_gig_btn');

// addproject details
const add_project_btn= document.getElementById('add_project_btn');
const addproject_container= document.querySelector('.addproject_container');
const close_project_btn= document.getElementById('close_project_btn');

// display addgigs form
add_gig_btn.addEventListener('click', () =>{

    addgigs_container.classList.add('show');

});
// hide addgigs form
close_gig_btn.addEventListener('click', () =>{

    addgigs_container.classList.remove('show');

});

// display addgigs form
add_project_btn.addEventListener('click', () =>{

    addproject_container.classList.add('show');

});
// hide addgigs form
close_project_btn.addEventListener('click', () =>{

    addproject_container.classList.remove('show');

});
