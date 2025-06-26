const addgigsbutton = document.querySelector('.option');
const gigsContainer= document.querySelector('.addgigs_container');

addgigsbutton.addEventListener('click', function(){
    if(gigsContainer.style.display==='none'|| gigsContainer.style.display===''){
        gigsContainer.style.display='block';
    }
    else{
        gigsContainer.style.display= 'none';
    }
});