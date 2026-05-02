import { useState } from "react";

function Cadastro({ mudarTela }) {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!nome || !email || !senha) {
      setErro("Preencha todos os campos");
      return;
    }

    if (!email.includes("@")) {
      setErro("Email inválido");
      return;
    }

    if (senha.length < 6) {
      setErro("A senha deve ter no mínimo 6 caracteres");
      return;
    }

    setErro("");
    setTimeout(() => {
      alert("Conta criada com sucesso!");
    }, 1000);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.logo}>ByteBank</h1>
        <p style={styles.subtitle}>Crie sua conta gratuita</p>

        {/* 🔴 ERRO COM ESPAÇO FIXO */}
        <p style={styles.erro}>{erro || " "}</p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="text"
            placeholder="Seu nome"
            value={nome}
            onChange={(e) => {
              setNome(e.target.value);
              setErro("");
            }}
            style={styles.input}
          />

          <input
            type="email"
            placeholder="Seu email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setErro("");
            }}
            style={styles.input}
          />

          <input
            type="password"
            placeholder="Crie uma senha"
            value={senha}
            onChange={(e) => {
              setSenha(e.target.value);
              setErro("");
            }}
            style={styles.input}
          />

          <button type="submit" style={styles.button}>
            Criar conta
          </button>
        </form>

        <p style={styles.footer}>
          Já tem conta?{" "}
          <span style={styles.link} onClick={mudarTela}>
            Entrar
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
     marginTop: "45px",
  },
  erro: {
    color: "#ef4444",
    marginBottom: "10px",
    fontSize: "14px",
    minHeight: "20px", 
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

export default Cadastro;