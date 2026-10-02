"use client"

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react"

import { auth, type AuthUser } from "@/lib/api"

import {
  clearAuth,
  getRefreshToken,
  getStoredUser,
  setAuth,
} from "@/lib/auth/storage"

type AuthContextValue = {
  user: AuthUser | null
  loading: boolean
  isAuthenticated: boolean
  login: (
    email: string,
    password: string,
  ) => Promise<AuthUser>
  logout: () => Promise<void>
}

const AuthContext = createContext<
  AuthContextValue | undefined
>(undefined)

export function AuthProvider({
  children,
}: {
  children: ReactNode
}) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedUser = getStoredUser()

    if (!storedUser) {
      setLoading(false)
      return
    }

    auth
      .me()
      .then((currentUser) => {
        setUser(currentUser)
      })
      .catch(() => {
        clearAuth()
        setUser(null)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  async function login(
    email: string,
    password: string,
  ): Promise<AuthUser> {
    const response = await auth.login(
      email,
      password,
    )

    setAuth(
      response.access_token,
      response.refresh_token,
      response.user,
    )

    setUser(response.user)

    return response.user
  }

  async function logout(): Promise<void> {
    try {
      const refreshToken = getRefreshToken()

      if (refreshToken) {
        await auth.logout(refreshToken)
      }
    } catch {
      // Even if backend logout fails,
      // local authentication must still be cleared.
    } finally {
      clearAuth()
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: Boolean(user),
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider",
    )
  }

  return context
}