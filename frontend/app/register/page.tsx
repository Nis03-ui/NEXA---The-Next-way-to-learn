"use client"

import Link from "next/link"
import {
  ArrowLeft,
  Brain,
  Loader2,
} from "lucide-react"

import {
  useState,
  type FormEvent,
} from "react"

import {
  useRouter,
} from "next/navigation"

import {
  auth,
} from "@/lib/api"

import {
  useAuth,
} from "@/providers/AuthProvider"


export default function RegisterPage() {

  const router = useRouter()

  const {
    login,
  } = useAuth()


  const [name,setName] = useState("")
  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")
  const [confirmPassword,setConfirmPassword] = useState("")

  const [error,setError] = useState("")
  const [loading,setLoading] = useState(false)



  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ){

    event.preventDefault()

    setError("")


    if(password !== confirmPassword){

      setError(
        "Passwords do not match"
      )

      return
    }


    try{

      setLoading(true)


      await auth.register(
        name,
        email,
        password,
      )


      const user = await login(
        email,
        password,
      )


      if(user.role === "ADMIN"){

        router.push("/admin")

      }
      else if(user.role === "TEACHER"){

        router.push("/teacher")

      }
      else{

        router.push("/dashboard")

      }


    }
    catch(error){

      setError(
        error instanceof Error
        ? error.message
        : "Registration failed"
      )

    }
    finally{

      setLoading(false)

    }

  }



return (

<main className="min-h-screen bg-[#f8fafc]">

<div className="grid min-h-screen lg:grid-cols-2">


{/* Brand */}

<section
className="
hidden
bg-slate-950
p-10
text-white
lg:flex
lg:flex-col
lg:justify-between
"
>


<Link
href="/"
className="
flex
items-center
gap-3
"
>

<div
className="
grid
h-10
w-10
place-items-center
rounded-xl
bg-white
text-sm
font-bold
text-slate-950
"
>
N
</div>


<div>

<p className="text-sm font-bold">
NEXA
</p>

<p
className="
text-[10px]
uppercase
tracking-[0.18em]
text-slate-500
"
>
The Next Way to Learn
</p>

</div>


</Link>



<div className="max-w-lg">


<div
className="
mb-6
grid
h-12
w-12
place-items-center
rounded-2xl
bg-white/10
"
>

<Brain size={22}/>

</div>



<h1
className="
text-5xl
font-bold
tracking-[-0.04em]
"
>

Start learning

<span
className="
block
text-slate-500
"
>
differently.
</span>

</h1>



<p
className="
mt-6
max-w-md
text-base
leading-7
text-slate-400
"
>

Create your NEXA account and transform your
course material into an interactive AI learning
experience.

</p>


</div>



<p className="text-xs text-slate-600">

© {new Date().getFullYear()} NEXA

</p>


</section>





{/* Register Form */}

<section
className="
flex
items-center
justify-center
px-6
py-12
"
>


<div
className="
w-full
max-w-md
"
>


<Link
href="/"
className="
mb-8
inline-flex
items-center
gap-2
text-sm
font-medium
text-slate-500
transition
hover:text-slate-950
"
>

<ArrowLeft size={16}/>

Back to NEXA

</Link>





<div
className="
nexa-card
p-7
sm:p-9
"
>


<div className="mb-8">


<h2
className="
text-2xl
font-bold
tracking-tight
text-slate-950
"
>
Create your account
</h2>


<p
className="
mt-2
text-sm
leading-6
text-slate-500
"
>

Start your learning journey with NEXA.

</p>


</div>




{
error && (

<div
className="
mb-5
rounded-xl
border
border-red-200
bg-red-50
px-4
py-3
text-sm
text-red-700
"
>

{error}

</div>

)
}






<form
onSubmit={handleSubmit}
className="space-y-5"
>



<div>

<label
className="
mb-2
block
text-sm
font-semibold
text-slate-700
"
>

Full name

</label>


<input

type="text"

value={name}

onChange={
(e)=>setName(e.target.value)
}

required

disabled={loading}

placeholder="Your name"

className="
nexa-focus
h-11
w-full
rounded-xl
border
border-slate-200
bg-white
px-3.5
text-sm
outline-none
"
/>


</div>





<div>


<label
className="
mb-2
block
text-sm
font-semibold
text-slate-700
"
>
Email
</label>



<input

type="email"

value={email}

onChange={
(e)=>setEmail(e.target.value)
}

required

disabled={loading}

placeholder="you@example.com"

className="
nexa-focus
h-11
w-full
rounded-xl
border
border-slate-200
bg-white
px-3.5
text-sm
outline-none
"

/>


</div>





<div>


<label
className="
mb-2
block
text-sm
font-semibold
text-slate-700
"
>
Password
</label>



<input

type="password"

value={password}

onChange={
(e)=>setPassword(e.target.value)
}

required

disabled={loading}

placeholder="Create a password"

className="
nexa-focus
h-11
w-full
rounded-xl
border
border-slate-200
bg-white
px-3.5
text-sm
outline-none
"

/>


</div>






<div>


<label
className="
mb-2
block
text-sm
font-semibold
text-slate-700
"
>
Confirm password
</label>



<input

type="password"

value={confirmPassword}

onChange={
(e)=>setConfirmPassword(e.target.value)
}

required

disabled={loading}

placeholder="Repeat your password"

className="
nexa-focus
h-11
w-full
rounded-xl
border
border-slate-200
bg-white
px-3.5
text-sm
outline-none
"

/>


</div>






<button

disabled={loading}

type="submit"

className="
inline-flex
h-11
w-full
items-center
justify-center
gap-2
rounded-xl
bg-slate-950
text-sm
font-semibold
text-white
transition
hover:bg-slate-800
disabled:opacity-50
"

>


{
loading
?

<>

<Loader2
size={16}
className="animate-spin"
/>

Creating account...

</>

:

"Create account"

}



</button>




</form>





<p
className="
mt-7
text-center
text-sm
text-slate-500
"
>

Already have an account?{" "}

<Link

href="/login"

className="
font-semibold
text-blue-600
hover:text-blue-700
"

>

Sign in

</Link>


</p>



</div>


</div>


</section>


</div>


</main>


)

}