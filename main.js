
(function(){
  document.documentElement.classList.add('js');
  var y=document.getElementById('year'); if(y) y.textContent=new Date().getFullYear();
  var toggle=document.querySelector('.navtoggle');
  var menu=document.getElementById('mmenu');
  function setMenu(open){
    if(!menu||!toggle) return;
    menu.classList.toggle('open',open);toggle.classList.toggle('open',open);
    toggle.setAttribute('aria-expanded',open?'true':'false');
    document.body.classList.toggle('menu-open',open);
  }
  if(toggle){toggle.addEventListener('click',function(){setMenu(!menu.classList.contains('open'));});}
  if(menu){menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setMenu(false);});});}
  window.addEventListener('resize',function(){if(window.innerWidth>720) setMenu(false);});
  var mq=window.matchMedia('(prefers-reduced-motion: reduce)');
  if('IntersectionObserver' in window && !mq.matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.14});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  } else { document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');}); }
})();
