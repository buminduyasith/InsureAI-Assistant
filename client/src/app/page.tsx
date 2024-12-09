"use client"
import Image from "next/image";
import styles from "./page.module.css";
import LoginForm from "@/app/components/LoginForm";
import useAuthRedirect from "@/app/hooks/useAuthRedirect";

export default function Home() {
  useAuthRedirect(); 
  return (
    <LoginForm />
  );
}
