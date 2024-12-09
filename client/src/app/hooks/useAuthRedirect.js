import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUserClaims } from "@/app/services/authService";
const useAuthRedirect = () => {
    const router = useRouter();

    useEffect( () => {
        const checkAuth = async () => {
            const token = localStorage.getItem("authToken");
            if (!token) {
                router.push("/");
                return;
            }

            try {
                var data = await getUserClaims();
                if(data.claims.role == "Admin"){
                    router.push("/dashboard");
                }
                else{
                    router.push("/chat");
                }

            } catch (error) {
                console.error("Error fetching user claims:", error);
                router.push("/");
            }
        };

        checkAuth();
    }, [router]);
};

export default useAuthRedirect;
