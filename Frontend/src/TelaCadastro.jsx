import { useState } from "react";

function Cadastro() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log({
      nome,
      email,
      senha,
    });

    alert("Cadastro enviado!");

    // limpa os campos
    setNome("");
    setEmail("");
    setSenha("");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Cadastro</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            placeholder="Nome"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
        </div>

        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div>
          <input
            type="password"
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
        </div>

        <button type="submit">Cadastrar</button>
      </form>
    </div>
  );
}

export default Cadastro;