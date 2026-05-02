import { useMemo, useState } from "react";

function Dashboard({ sair }) {
  const [descricao, setDescricao] = useState("");
  const [valor, setValor] = useState("");
  const [tipo, setTipo] = useState("receita");
  const [erro, setErro] = useState("");
  const [transacoes, setTransacoes] = useState([
    { id: 1, descricao: "Salário", tipo: "receita", valor: 3500 },
    { id: 2, descricao: "Mercado", tipo: "despesa", valor: 280 },
    { id: 3, descricao: "Uber", tipo: "despesa", valor: 45.5 },
  ]);

  const receitas = useMemo(() => {
    return transacoes
      .filter((item) => item.tipo === "receita")
      .reduce((acc, item) => acc + item.valor, 0);
  }, [transacoes]);

  const despesas = useMemo(() => {
    return transacoes
      .filter((item) => item.tipo === "despesa")
      .reduce((acc, item) => acc + item.valor, 0);
  }, [transacoes]);

  const saldo = receitas - despesas;

  const handleAdicionar = (e) => {
    e.preventDefault();

    if (!descricao || !valor) {
      setErro("Preencha descrição e valor");
      return;
    }

    const valorNumero = Number(valor);

    if (Number.isNaN(valorNumero) || valorNumero <= 0) {
      setErro("Digite um valor válido");
      return;
    }

    const novaTransacao = {
      id: Date.now(),
      descricao,
      tipo,
      valor: valorNumero,
    };

    setTransacoes([novaTransacao, ...transacoes]);
    setDescricao("");
    setValor("");
    setTipo("receita");
    setErro("");
  };

  const removerTransacao = (id) => {
    const novaLista = transacoes.filter((item) => item.id !== id);
    setTransacoes(novaLista);
  };

  const formatarMoeda = (numero) => {
    return numero.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  };

  return (
    <div style={styles.container}>
      <div style={styles.topbar}>
        <h1 style={styles.logo}>ByteBank</h1>
        <button style={styles.logoutButton} onClick={sair}>
          Sair
        </button>
      </div>

      <div style={styles.content}>
        <h2 style={styles.title}>Dashboard</h2>
        <p style={styles.subtitle}>Gerencie suas receitas e despesas</p>

        <div style={styles.cards}>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Saldo atual</p>
            <h3
              style={
                saldo >= 0 ? styles.cardValueGreen : styles.cardValueRed
              }
            >
              {formatarMoeda(saldo)}
            </h3>
          </div>

          <div style={styles.card}>
            <p style={styles.cardLabel}>Receitas</p>
            <h3 style={styles.cardValueGreen}>{formatarMoeda(receitas)}</h3>
          </div>

          <div style={styles.card}>
            <p style={styles.cardLabel}>Despesas</p>
            <h3 style={styles.cardValueRed}>{formatarMoeda(despesas)}</h3>
          </div>
        </div>

        <div style={styles.grid}>
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Nova transação</h3>

            <p style={styles.erro}>{erro || " "}</p>

            <form onSubmit={handleAdicionar} style={styles.form}>
              <input
                type="text"
                placeholder="Descrição"
                value={descricao}
                onChange={(e) => {
                  setDescricao(e.target.value);
                  setErro("");
                }}
                style={styles.input}
              />

              <input
                type="number"
                step="0.01"
                placeholder="Valor"
                value={valor}
                onChange={(e) => {
                  setValor(e.target.value);
                  setErro("");
                }}
                style={styles.input}
              />

              <select
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
                style={styles.select}
              >
                <option value="receita">Receita</option>
                <option value="despesa">Despesa</option>
              </select>

              <button type="submit" style={styles.addButton}>
                Adicionar
              </button>
            </form>
          </div>

          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Transações</h3>

            <div style={styles.table}>
              {transacoes.length === 0 ? (
                <p style={styles.emptyText}>Nenhuma transação cadastrada.</p>
              ) : (
                transacoes.map((item) => (
                  <div key={item.id} style={styles.row}>
                    <div>
                      <p style={styles.rowTitle}>{item.descricao}</p>
                      <p style={styles.rowCategory}>
                        {item.tipo === "receita" ? "Receita" : "Despesa"}
                      </p>
                    </div>

                    <div style={styles.rowRight}>
                      <p
                        style={
                          item.tipo === "receita"
                            ? styles.rowValueGreen
                            : styles.rowValueRed
                        }
                      >
                        {item.tipo === "receita" ? "+" : "-"}{" "}
                        {formatarMoeda(item.valor)}
                      </p>

                      <button
                        style={styles.removeButton}
                        onClick={() => removerTransacao(item.id)}
                      >
                        Remover
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "#0f172a",
    color: "#fff",
    padding: "30px",
    fontFamily: "Arial, sans-serif",
  },
  topbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
  },
  logo: {
    color: "#22c55e",
    margin: 0,
  },
  logoutButton: {
    background: "#ef4444",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "10px 16px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  content: {
    maxWidth: "1100px",
    margin: "0 auto",
  },
  title: {
    marginBottom: "8px",
  },
  subtitle: {
    color: "#94a3b8",
    marginBottom: "25px",
  },
  cards: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
    marginBottom: "30px",
  },
  card: {
    background: "#1e293b",
    borderRadius: "16px",
    padding: "20px",
    boxShadow: "0 10px 20px rgba(0,0,0,0.25)",
  },
  cardLabel: {
    color: "#94a3b8",
    marginBottom: "10px",
  },
  cardValueGreen: {
    margin: 0,
    fontSize: "24px",
    color: "#22c55e",
  },
  cardValueRed: {
    margin: 0,
    fontSize: "24px",
    color: "#ef4444",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1.4fr",
    gap: "20px",
  },
  section: {
    background: "#1e293b",
    borderRadius: "16px",
    padding: "20px",
    boxShadow: "0 10px 20px rgba(0,0,0,0.25)",
  },
  sectionTitle: {
    marginTop: 0,
    marginBottom: "16px",
  },
  erro: {
    color: "#ef4444",
    minHeight: "20px",
    marginBottom: "10px",
    fontSize: "14px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  input: {
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#334155",
    color: "#fff",
    outline: "none",
  },
  select: {
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#334155",
    color: "#fff",
    outline: "none",
  },
  addButton: {
    marginTop: "8px",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#22c55e",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },
  table: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "14px",
    background: "#334155",
    borderRadius: "10px",
    gap: "12px",
  },
  rowTitle: {
    margin: 0,
    fontWeight: "bold",
  },
  rowCategory: {
    margin: 0,
    fontSize: "14px",
    color: "#cbd5e1",
  },
  rowRight: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
  },
  rowValueGreen: {
    margin: 0,
    fontWeight: "bold",
    color: "#22c55e",
  },
  rowValueRed: {
    margin: 0,
    fontWeight: "bold",
    color: "#ef4444",
  },
  removeButton: {
    background: "#475569",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "8px 12px",
    cursor: "pointer",
  },
  emptyText: {
    color: "#cbd5e1",
  },
};

export default Dashboard;