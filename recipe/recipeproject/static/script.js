
  document.addEventListener('DOMContentLoaded',()=>{
      let searchinput = document.getElementById('searchs')
      let searchbutton = document.getElementById('searchb')
    
      searchbutton.addEventListener('click',(e)=>{
         event.preventDefault();
        let query = encodeURIComponent(searchinput.value.trim());
        if (query) {
            window.location.href = `${window.location.origin}/searchfood/${query}/`;
        }
    });
});

