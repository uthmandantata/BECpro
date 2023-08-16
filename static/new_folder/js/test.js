const emailField = document.querySelector('#emailField')
const feedBackArea = document.querySelector('.invalid_feedback')
const emailfeedBackArea = document.querySelector('.invalid_email')
const userameSuccessOutput = document.querySelector('.userameSuccessOutput')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')


const handleToggleInput=(e)=>{
    if(showPasswordToggle.textContent==='SHOW'){
        showPasswordToggle.textContent = 'HIDE';
        passwordField.setAttribute("type", "text")
    }
    else{
        showPasswordToggle.textContent = "SHOW"
        passwordField.setAttribute("type", "password")
    }
}


usernameField.addEventListener('keyup',(e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid');
    feedBackArea.style.display = 'none'
    userameSuccessOutput.textContent=`Checking ${usernameVal}`;
    userameSuccessOutput.style.display = 'block'
    
    if(usernameVal.length > 0){
        fetch('/authenticate/validate-username', {
            body:JSON.stringify({username:usernameVal}), 
            method:"POST",
        }).then((res)=>res.json()).then((data)=>{
            console.log('data',data);
            userameSuccessOutput.style.display = 'none'
            if(data.username_error){
                submitBtn.disabled = true;
                usernameField.classList.add('is-invalid');
                feedBackArea.style.display = 'block'
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`
            }
            else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
})


emailField.addEventListener('keyup',(e) => {
    const emailVal = e.target.value;
    emailField.classList.remove('is-invalid');
    emailfeedBackArea.style.display = 'none'
    emailSuccessOutput.textContent=`Checking ${emailVal}`;
    emailSuccessOutput.style.display = 'block'
    
    
    
    
    if(emailVal.length > 0){
        fetch('/authentication/validate-email', {
            body:JSON.stringify({email:emailVal}), 
            method:"POST",
        }).then((res)=>res.json()).then((data)=>{
            console.log('data',data);
            emailSuccessOutput.style.display = 'none'
            if(data.email_error){
                emailField.classList.add('is-invalid');
                emailfeedBackArea.style.display = 'block'
                emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`
                submitBtn.disabled=true;
            }else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
})


showPasswordToggle.addEventListener('click', handleToggleInput)