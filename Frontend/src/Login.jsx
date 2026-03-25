import { useState } from "react";

function Login({ mudarTela }) {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Login realizado!");
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.logo}>ByteBank</h1>
        <p style={styles.subtitle}>Acesse sua conta</p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="email"
            placeholder="Seu email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
          />

          <input
            type="password"
            placeholder="Sua senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            style={styles.input}
          />

          <button type="submit" style={styles.button}>
            Entrar
          </button>
        </form>

        <p style={styles.footer}>
          Não tem conta?{" "}
          <span style={styles.link} onClick={mudarTela}>
            Cadastrar
          </span>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a",
  },
  card: {
    background: "#1e293b",
    padding: "40px",
    borderRadius: "16px",
    width: "320px",
    textAlign: "center",
    boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
  },
  logo: {
    color: "#22c55e",
    marginBottom: "10px",
    marginTop: "-10px",
  },
  subtitle: {
    color: "#94a3b8",
    marginBottom: "25px",
    marginTop: "20px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
  },
  input: {
    padding: "12px",
    margin: "8px 0",
    borderRadius: "8px",
    border: "none",
    background: "#334155",
    color: "#fff",
    outline: "none",
  },
  button: {
    marginTop: "15px",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#22c55e",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },
  footer: {
    marginTop: "20px",
    color: "#94a3b8",
  },
  link: {
    color: "#22c55e",
    cursor: "pointer",
  },
};

export default Login;
