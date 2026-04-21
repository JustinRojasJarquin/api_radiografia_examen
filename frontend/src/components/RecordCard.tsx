import { Link } from "react-router-dom";

type Props = {
  record: any;
  onDelete: (id: number) => Promise<void>;
  onViewImage: (id: number) => Promise<void>;
};

export default function RecordCard({ record, onDelete, onViewImage }: Props) {
  return (
    <div style={styles.card}>
      <div style={styles.topRow}>
        <div>
          <h3 style={styles.name}>{record.patient_full_name}</h3>
          <p style={styles.meta}>Record ID: #{record.id}</p>
        </div>

        <span style={styles.badge}>Protegido</span>
      </div>

      <div style={styles.grid}>
        <div>
          <span style={styles.label}>Cedula del paciente</span>
          <p style={styles.value}>{record.patient_identifier}</p>
        </div>

        <div>
          <span style={styles.label}>Fecha del estudio</span>
          <p style={styles.value}>{record.study_date}</p>
        </div>
      </div>

      <div style={styles.block}>
        <span style={styles.label}>Referencia clínica</span>
        <p style={styles.value}>{record.clinical_reference}</p>
      </div>

      <div style={styles.actions}>
        <button style={styles.primaryButton} onClick={() => onViewImage(record.id)}>
          Ver placa radiográfica
        </button>

        <Link to={`/records/edit/${record.id}`} style={styles.secondaryButton}>
          Editar
        </Link>

        <button style={styles.dangerButton} onClick={() => onDelete(record.id)}>
          Eliminar
        </button>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: "#ffffff",
    border: "1px solid #dbe8f4",
    borderRadius: "16px",
    padding: "1.4rem",
    boxShadow: "0 8px 20px rgba(14, 55, 97, 0.06)",
  },
  topRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "1rem",
  },
  name: {
    margin: 0,
    color: "#123c74",
  },
  meta: {
    margin: "0.35rem 0 0 0",
    color: "#6b7280",
    fontSize: "0.9rem",
  },
  badge: {
    background: "#e6f2ff",
    color: "#0056b3",
    padding: "0.4rem 0.7rem",
    borderRadius: "999px",
    fontSize: "0.8rem",
    fontWeight: 700,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "1rem",
    marginBottom: "1rem",
  },
  block: {
    marginBottom: "1rem",
  },
  label: {
    display: "block",
    fontSize: "0.85rem",
    fontWeight: 700,
    color: "#4b6480",
    marginBottom: "0.35rem",
    textTransform: "uppercase" as const,
    letterSpacing: "0.03em",
  },
  value: {
    margin: 0,
    color: "#253443",
  },
  actions: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: "0.8rem",
  },
  primaryButton: {
    background: "#0056b3",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    padding: "0.75rem 1rem",
    fontWeight: 700,
    cursor: "pointer",
  },
  secondaryButton: {
    background: "#ffffff",
    color: "#0b3d91",
    border: "1px solid #b7d0ea",
    borderRadius: "10px",
    padding: "0.75rem 1rem",
    fontWeight: 700,
    textDecoration: "none",
  },
  dangerButton: {
    background: "#fff1f2",
    color: "#b42318",
    border: "1px solid #f3c7cb",
    borderRadius: "10px",
    padding: "0.75rem 1rem",
    fontWeight: 700,
    cursor: "pointer",
  },
};