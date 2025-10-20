export function clearTempStorage(){
    if (localStorage.getItem("isLoggedIn") !== null){
        localStorage.removeItem("isLoggedIn")
        localStorage.removeItem("timeToken")
        localStorage.removeItem("userEmail")
        return true
    } else {
        return false
    }
}

export function setTempStorage(userEmail){
    localStorage.setItem("isLoggedIn",true)
    localStorage.setItem("userEmail",userEmail)
    const currentTime = new Date()
    localStorage.setItem("timeToken",currentTime.getTime())
}