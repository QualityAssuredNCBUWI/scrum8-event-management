

// let login_form = document.querySelector(".login-form form")
// let form_data = new FormData(login_form);

// let email = form_data.get("email")
// let password = form_data.get("password")
// let sub = {}
// sub.email = email;
// sub.password = password;
// let self = this;
// fetch("/api/auth/login", {
//     method: 'POST',
//     body: sub,
//     headers : {
//         'Accept': 'application/json',
//         "Content-Type":"application/json"
//     },
//     body: JSON.stringify(sub)
//     // headers: {'X-CSRFToken': token    },    credentials: 'same-origin'
// })    
// .then(function (response) {        
//     if(response.status == 404){
//     response.json().then((data) => {
//         router.push({ name: 'Login', params: { flashes: JSON.stringify(
//         [{
//             message: "Email or password is incorrect",
//             category: "danger"
//             }]
//         )}})
//     });
//     } else if (response.status == 200){
//     response.json().then((data) => {
//         window.location.replace('http://localhost:8079/')
//         localStorage.setItem('token', data.token)
//     });
//     }
//     })    
// .then(function (jsonResponse) {
//     // display a success message
//     console.log(jsonResponse);

//     self.message=jsonResponse.message;
//     if(self.message == "Login successful") {
//         self.$router.push("/login")
//         localStorage.setItem('token', jsonResponse.token)
//     }
//     })    
// .catch(function (error) {
//     console.log(error);

//     self.error=error.message;   
// });