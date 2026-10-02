import { ChatDemoSection } from "@/components/landing/ChatDemoSection"
import { FeatureShowcase } from "@/components/landing/FeatureShowcase"
import { HeroSection } from "@/components/landing/HeroSection"
import { HowNexaWorks } from "@/components/landing/HowNexaWorks"
import { LandingFooter } from "@/components/landing/LandingFooter"
import { LandingNavbar } from "@/components/landing/LandingNavbar"

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f8fafc]">
      <LandingNavbar />
      <HeroSection />
      <HowNexaWorks />
      <FeatureShowcase />
      <ChatDemoSection />
      <LandingFooter />
    </main>
  )
}