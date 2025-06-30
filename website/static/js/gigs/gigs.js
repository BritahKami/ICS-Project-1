const add_gig_btn= document.getElementById('add_gig_btn');
const addgigs_container= document.querySelector('.addgigs_container');
const close_gig_btn= document.getElementById('close_gig_btn');

add_gig_btn.addEventListener('click', () =>{

    addgigs_container.classList.add('show');

});

close_gig_btn.addEventListener('click', () =>{

    addgigs_container.classList.remove('show');

});
