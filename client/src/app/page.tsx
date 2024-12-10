"use client"
import LoginForm from "@/app/components/LoginForm";
import useAuthRedirect from "@/app/hooks/useAuthRedirect";

export default function Home() {
  useAuthRedirect(); 
  return (
    <LoginForm />
  );
}
