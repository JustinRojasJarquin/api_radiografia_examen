import { useEffect } from "react";
import API from "../api/api";

declare global {
  interface Window {
    google: any;
  }
}

export default function Login() {
  useEffect(() => {
    if (!window.google) return;

    window.google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: handleCredentialResponse,
    });

    window.google.accounts.id.renderButton(
      document.getElementById("googleBtn"),
      {
        theme: "outline",
        size: "large",
        width: 320,
      }
    );
  }, []);

  const handleCredentialResponse = async (response: any) => {
    try {
      const res = await API.post("/auth/google/login", {
        token: response.credential,
      });

      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/records";
    } catch (error: any) {
      console.error("Google login error:", error);
      console.log("Backend response:", error?.response?.data);
      alert(JSON.stringify(error?.response?.data || "Google login failed"));
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.overlay}>
        <div style={styles.card}>
          <div style={styles.logoCircle}>+</div>
          <h1 style={styles.title}>PLACAS RADIOGRAFICAS</h1>
          <p style={styles.subtitle}>
           Acceso clínico seguro para registros radiográficos
          </p>

          <div style={styles.loginBox}>
            <p style={styles.loginLabel}>Iniciar sesion con google</p>
            <div style={styles.googleButtonWrapper}>
              <div id="googleBtn"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #0056b3 0%, #0b3d91 100%)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "2rem",
  },
  overlay: {
    width: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  card: {
    width: "100%",
    maxWidth: "460px",
    background: "#ffffff",
    borderRadius: "20px",
    padding: "3rem 2.5rem",
    boxShadow: "0 16px 40px rgba(0, 0, 0, 0.18)",
    textAlign: "center" as const,
  },
  logoCircle: {
    width: "72px",
    height: "72px",
    borderRadius: "50%",
    background: "#0056b3",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "2rem",
    fontWeight: 700,
    margin: "0 auto 1rem auto",
  },
  title: {
    margin: 0,
    color: "#0b2f66",
    fontSize: "2.3rem",
    fontWeight: 700,
  },
  subtitle: {
    marginTop: "0.8rem",
    marginBottom: "2rem",
    color: "#5b6470",
    fontSize: "1rem",
  },
  loginBox: {
    background: "#f4f8fc",
    border: "1px solid #d9e6f2",
    borderRadius: "14px",
    padding: "1.5rem",
  },
  loginLabel: {
    marginTop: 0,
    marginBottom: "1rem",
    color: "#24456d",
    fontWeight: 600,
  },
  googleButtonWrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
};