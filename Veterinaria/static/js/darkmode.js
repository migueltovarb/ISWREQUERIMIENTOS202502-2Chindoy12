document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('darkModeToggle');
  const body = document.body;
  const current = localStorage.getItem('vet_dark') || 'light';
  body.className = current;
  if(btn){
    btn.addEventListener('click', ()=>{
      const next = body.className === 'light' ? 'dark' : 'light';
      body.className = next;
      localStorage.setItem('vet_dark', next);
    });
  }
});
