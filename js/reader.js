
(function(){
  const shell=document.querySelector(".reader-shell");
  if(!shell) return;
  const progress=document.querySelector(".reader-progress i");
  const settings=document.querySelector(".reader-settings");
  const article=document.querySelector(".mag-page");
  const fontValue=document.querySelector("#fontValue");

  function updateProgress(){
    const top=window.scrollY;
    const max=document.documentElement.scrollHeight-window.innerHeight;
    progress.style.width=(max>0?Math.min(100,Math.max(0,top/max*100)):0)+"%";
  }
  window.addEventListener("scroll",updateProgress,{passive:true});
  updateProgress();

  document.querySelector("#settingsBtn")?.addEventListener("click",()=>settings.classList.toggle("open"));
  document.querySelector("#fontDown")?.addEventListener("click",()=>{
    const current=parseFloat(getComputedStyle(article.querySelector("p")).fontSize);
    const next=Math.max(14,current-1);
    article.style.setProperty("--reader-font",next+"px");
    article.querySelectorAll("p,li").forEach(x=>x.style.fontSize=next+"px");
    if(fontValue) fontValue.textContent=Math.round(next)+"px";
  });
  document.querySelector("#fontUp")?.addEventListener("click",()=>{
    const current=parseFloat(getComputedStyle(article.querySelector("p")).fontSize);
    const next=Math.min(24,current+1);
    article.style.setProperty("--reader-font",next+"px");
    article.querySelectorAll("p,li").forEach(x=>x.style.fontSize=next+"px");
    if(fontValue) fontValue.textContent=Math.round(next)+"px";
  });
  document.querySelector("#themeSepia")?.addEventListener("click",()=>shell.classList.toggle("sepia"));
  document.querySelector("#themeDark")?.addEventListener("click",()=>shell.classList.toggle("dark-paper"));
  document.querySelector("#themeLight")?.addEventListener("click",()=>shell.classList.remove("sepia","dark-paper"));

  document.querySelector("#topBtn")?.addEventListener("click",()=>window.scrollTo({top:0,behavior:"smooth"}));

  document.addEventListener("keydown",e=>{
    if(e.key==="Home") window.scrollTo({top:0,behavior:"smooth"});
    if(e.key==="Escape") settings?.classList.remove("open");
  });

  // Touch swipe: left/right moves between article pages when links exist.
  let sx=0,sy=0;
  document.addEventListener("touchstart",e=>{sx=e.changedTouches[0].clientX;sy=e.changedTouches[0].clientY},{passive:true});
  document.addEventListener("touchend",e=>{
    const dx=e.changedTouches[0].clientX-sx, dy=e.changedTouches[0].clientY-sy;
    if(Math.abs(dx)>80 && Math.abs(dx)>Math.abs(dy)){
      const link=dx<0?document.querySelector("[data-next]"):document.querySelector("[data-prev]");
      if(link) location.href=link.href;
    }
  },{passive:true});
})();
