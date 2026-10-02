export function getToken(){

if(typeof window==="undefined")
return null

return localStorage.getItem("nexa_token")

}


export function logout(){

localStorage.removeItem("nexa_token")

window.location.href="/login"

}
