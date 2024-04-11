document.addEventListener("DOMContentLoaded", function() {
    const username = localStorage.getItem('username');
    if (username) {
        const newMessage = document.getElementById('newMessage');
        newMessage.textContent = `Bem-vindo, ${username}!`;
    }
});

//Event profile SUBMENU

document.addEventListener("DOMContentLoaded", function() {
    var photoProfile = document.querySelector(".photo-profile");
    var submenu = document.getElementById("submenu");
    var timeoutId;
  
    photoProfile.addEventListener("mouseenter", function() {
      clearTimeout(timeoutId);
      submenu.style.display = "block"; 
  });
  
  photoProfile.addEventListener("mouseleave", function() {
   
      timeoutId = setTimeout(function() {
          submenu.style.display = "none";
      }, 100);
  });
  
  submenu.addEventListener("mouseenter", function() {
      clearTimeout(timeoutId);
      submenu.style.display = "block";
  });
  
  submenu.addEventListener("mouseleave", function() {
      timeoutId = setTimeout(function() {
          submenu.style.display = "none";
      }, 100);
  });
  });
  
  //=================================================================================================================

  function op1() {
    var data = document.getElementById('nameData');
    data.textContent = "CALCULATE RISK RETURN"
    document.getElementById('wallet').src = "{{url_for('gerarminhacarteira')}}";
}
function op2() {
    var data = document.getElementById('nameData');
    data.textContent = "Wallet"
}
function op3() {
    var iframe = document.getElementById('iframeTarget');
    iframe.src = "{{url_for('/minhacarteira')}}";
    var data = document.getElementById('nameData');
    data.textContent = "Ranking Dividends"
}
function op4() {
    var iframe = document.getElementById('iframeTarget');
    iframe.src = "{{url_for('calcularRiscoRetorno', opcao=GET)}}";
    var data = document.getElementById('nameData');
    data.textContent = "Correlacao Indicators"
}
function op5() {

    var data = document.getElementById('nameData');
    data.textContent = "data"
}
