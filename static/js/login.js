
function checkLogin(username, password) {
    if (username === 'nathan@nathan.com' && password === '123') {
      return true;
    } else {
      return false;
    }
  }

  

  loginForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (checkLogin(email, password)) {
      window.location.href = '/';
      document.getElementById("loginbtn").innerHTML = "Sair";
    } else {
      alert('Email ou senha incorretos. Tente novamente.');
    }
  });
  