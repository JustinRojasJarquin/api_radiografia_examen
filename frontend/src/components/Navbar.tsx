import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav style={styles.nav}>
      <div style={styles.brand}>
        <div style={styles.brandIcon}>+</div>
        <div>
          <div style={styles.brandTitle}>API Placas Radiográficas</div>
          <div style={styles.brandSubtitle}>Web Información Clínica</div>
        </div>
      </div>

      <div style={styles.links}>
        <Link
          to="/records"
          style={{
            ...styles.link,
            ...(isActive("/records") ? styles.activeLink : {}),
          }}
        >
          Registros
        </Link>

        <Link
          to="/records/create"
          style={{
            ...styles.link,
            ...(isActive("/records/create") ? styles.activeLink : {}),
          }}
        >
          Crear registro
        </Link>

        <button onClick={handleLogout} style={styles.logoutButton}>
          Cerrar sesión
        </button>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    background: "linear-gradient(90deg, #0b3d91 0%, #0056b3 100%)",
    color: "#fff",
    padding: "1rem 2rem",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    boxShadow: "0 4px 10px rgba(0,0,0,0.12)",
    position: "sticky" as const,
    top: 0,
    zIndex: 100,
  },
  brand: {
    display: "flex",
    alignItems: "center",
    gap: "0.9rem",
  },
  brandIcon: {
    width: "42px",
    height: "42px",
    borderRadius: "50%",
    background: "#ffffff",
    color: "#0b3d91",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 700,
    fontSize: "1.2rem",
  },
  brandTitle: {
    fontWeight: 700,
    fontSize: "1.05rem",
  },
  brandSubtitle: {
    fontSize: "0.8rem",
    opacity: 0.85,
  },
  links: {
    display: "flex",
    alignItems: "center",
    gap: "0.8rem",
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    padding: "0.65rem 1rem",
    borderRadius: "10px",
    fontWeight: 600,
    transition: "0.2s",
  },
  activeLink: {
    background: "rgba(255,255,255,0.18)",
  },
  logoutButton: {
    background: "#ffffff",
    color: "#0b3d91",
    border: "none",
    borderRadius: "10px",
    padding: "0.7rem 1rem",
    fontWeight: 700,
    cursor: "pointer",
  },
};