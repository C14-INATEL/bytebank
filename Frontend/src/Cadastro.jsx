import { useState } from "react";

function Cadastro() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    alert("Cadastro enviado!");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Cadastro</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />
        <br /><br />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <br /><br />

        <input
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        <br /><br />

        <button type="submit">Cadastrar</button>
      </form>
    </div>
  );
}

export default Cadastro;