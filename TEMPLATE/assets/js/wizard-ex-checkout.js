document.addEventListener("DOMContentLoaded",function(e){var t=parseInt(window.Helpers.getCssVar("gray-200",!0).slice(1,3),16),r=parseInt(window.Helpers.getCssVar("gray-200",!0).slice(3,5),16),a=parseInt(window.Helpers.getCssVar("gray-200",!0).slice(5,7),16),l=document.querySelectorAll(".read-only-ratings");let n="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='16' %3E%3Cpath fill='rgb("+t+","+r+","+a+")' d='M21.947 9.179a1 1 0 0 0-.868-.676l-5.701-.453l-2.467-5.461a.998.998 0 0 0-1.822-.001L8.622 8.05l-5.701.453a1 1 0 0 0-.619 1.713l4.213 4.107l-1.49 6.452a1 1 0 0 0 1.53 1.057L12 18.202l5.445 3.63a1.001 1.001 0 0 0 1.517-1.106l-1.829-6.4l4.536-4.082c.297-.268.406-.686.278-1.065'/%3E%3C/svg%3E";l.forEach(e=>{new Raty(e,{starOn:"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='16' %3E%3Cpath fill='%23FFD700' d='M21.947 9.179a1 1 0 0 0-.868-.676l-5.701-.453l-2.467-5.461a.998.998 0 0 0-1.822-.001L8.622 8.05l-5.701.453a1 1 0 0 0-.619 1.713l4.213 4.107l-1.49 6.452a1 1 0 0 0 1.53 1.057L12 18.202l5.445 3.63a1.001 1.001 0 0 0 1.517-1.106l-1.829-6.4l4.536-4.082c.297-.268.406-.686.278-1.065'/%3E%3C/svg%3E",starOff:n}).init()})}),(()=>{window.Helpers.initCustomOptionCheck();let t=document.querySelector(".credit-card-mask"),r=document.querySelector(".expiry-date-mask"),a=document.querySelector(".cvv-code-mask");t&&(t.addEventListener("input",e=>{t.value=formatCreditCard(e.target.value);e=e.target.value.replace(/\D/g,""),e=getCreditCardType(e);document.querySelector(".card-type").innerHTML=e&&"unknown"!==e&&"general"!==e?`<img src="${assetsPath}img/icons/payments/${e}-cc.png" height="19"/>`:""}),registerCursorTracker({input:t,delimiter:" "})),r&&(r.addEventListener("input",e=>{r.value=formatDate(e.target.value,{delimiter:"/",datePattern:["m","y"]})}),registerCursorTracker({input:r,delimiter:"-"})),a&&a.addEventListener("input",e=>{a.value=formatNumeral(e.target.value,{numeralThousandsGroupStyle:"thousand"})});var e=document.querySelector("#wizard-checkout"),l=[].slice.call(e.querySelectorAll(".btn-next")),n=e.querySelector(".btn-submit");if(null!==e){let t=new Stepper(e,{linear:!1});l&&l.forEach(e=>{e.addEventListener("click",e=>{t.next()})}),n&&n.addEventListener("click",e=>{alert("Submitted..!!")})}})();