import { useEffect, useMemo, useState, useCallback } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from "recharts";

const API = "http://127.0.0.1:5000/api";

function authHeaders() {
  const token = localStorage.getItem("token");
  return { "Content-Type": "application/json", Authorization: `Bearer ${token}` };
}

// ── Tooltip customizado para moeda BRL ──────────────────────────────────────
const TooltipMoeda = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "10px", padding: "10px 14px" }}>
      <p style={{ color: "#94a3b8", margin: "0 0 6px", fontSize: "13px", textTransform: "capitalize" }}>{label}</p>
      {payload.map(p => (
        <p key={p.name} style={{ color: p.color, margin: "2px 0", fontSize: "14px", fontWeight: "bold" }}>
          {p.name}: {Number(p.value).toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}
        </p>
      ))}
    </div>
  );
};

function Dashboard({ sair }) {
  const username = localStorage.getItem("username") || "Usuário";

  const [descricao, setDescricao]   = useState("");
  const [valor, setValor]           = useState("");
  const [tipo, setTipo]             = useState("receita");
  const [categoria, setCategoria]   = useState("outros");
  const [erro, setErro]             = useState("");
  const [editandoId, setEditandoId] = useState(null);
  const [busca, setBusca]           = useState("");
  const [loading, setLoading]       = useState(false);
  const [abaSidebar, setAbaSidebar] = useState("dashboard");
  const [transacoes, setTransacoes] = useState([]);

  // ── Carrega transações da API ──────────────────────────────────────────────
  const carregarTransacoes = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/transactions`, { headers: authHeaders() });
      if (res.status === 401) { sair(); return; }
      const data = await res.json();
      setTransacoes(Array.isArray(data) ? data : []);
    } catch {
      setErro("Erro ao carregar transações.");
    } finally {
      setLoading(false);
    }
  }, [sair]);

  useEffect(() => { carregarTransacoes(); }, [carregarTransacoes]);

  // ── Cálculos financeiros ───────────────────────────────────────────────────
  const receitas = useMemo(
    () => transacoes.filter(t => t.type === "receita").reduce((a, t) => a + t.amount, 0),
    [transacoes]
  );
  const despesas = useMemo(
    () => transacoes.filter(t => t.type === "despesa").reduce((a, t) => a + t.amount, 0),
    [transacoes]
  );
  const saldo = receitas - despesas;

  // ── Dados para gráfico de categorias (barras) ──────────────────────────────
  const dadosCategorias = useMemo(() => {
    const mapa = {};
    transacoes.filter(t => t.type === "despesa").forEach(t => {
      const cat = t.category || "outros";
      mapa[cat] = (mapa[cat] || 0) + t.amount;
    });
    return Object.entries(mapa)
      .map(([categoria, valor]) => ({ categoria, valor: Number(valor.toFixed(2)) }))
      .sort((a, b) => b.valor - a.valor);
  }, [transacoes]);

  // ── Dados para gráfico receita vs despesa por mês ─────────────────────────
  const dadosMensais = useMemo(() => {
    const mapa = {};
    transacoes.forEach(t => {
      if (!t.date) return;
      const data = new Date(t.date);
      const chave = `${String(data.getMonth() + 1).padStart(2, "0")}/${data.getFullYear()}`;
      if (!mapa[chave]) mapa[chave] = { mes: chave, receitas: 0, despesas: 0 };
      if (t.type === "receita") mapa[chave].receitas += t.amount;
      else mapa[chave].despesas += t.amount;
    });
    return Object.values(mapa)
      .sort((a, b) => {
        const [ma, ya] = a.mes.split("/");
        const [mb, yb] = b.mes.split("/");
        return new Date(`${ya}-${ma}`) - new Date(`${yb}-${mb}`);
      })
      .map(d => ({
        mes: d.mes,
        receitas: Number(d.receitas.toFixed(2)),
        despesas: Number(d.despesas.toFixed(2)),
      }));
  }, [transacoes]);

  // ── Filtragem por busca ────────────────────────────────────────────────────
  const transacoesFiltradas = useMemo(() => {
    if (!busca.trim()) return transacoes;
    const q = busca.toLowerCase();
    return transacoes.filter(t =>
      t.description?.toLowerCase().includes(q) ||
      t.category?.toLowerCase().includes(q) ||
      t.type?.toLowerCase().includes(q)
    );
  }, [transacoes, busca]);

  const formatarMoeda = (n) =>
    Number(n).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

  const limparFormulario = () => {
    setDescricao(""); setValor(""); setTipo("receita");
    setCategoria("outros"); setErro(""); setEditandoId(null);
  };

  // ── Adicionar / Editar transação ───────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!descricao || valor === "") { setErro("Preencha descrição e valor"); return; }
    const valorNumero = Number(valor);
    if (isNaN(valorNumero) || valorNumero < 0) { setErro("Digite um valor válido (0 ou maior)"); return; }

    const payload = {
      type: tipo, category: categoria,
      amount: valorNumero, description: descricao,
      date: new Date().toISOString(),
    };

    try {
      if (editandoId) {
        const res = await fetch(`${API}/transactions/${editandoId}`, {
          method: "PUT", headers: authHeaders(), body: JSON.stringify(payload),
        });
        if (!res.ok) { const d = await res.json(); setErro(d.error || "Erro ao editar"); return; }
      } else {
        const res = await fetch(`${API}/transactions`, {
          method: "POST", headers: authHeaders(), body: JSON.stringify(payload),
        });
        if (!res.ok) { const d = await res.json(); setErro(d.error || "Erro ao adicionar"); return; }
      }
      limparFormulario();
      carregarTransacoes();
    } catch (err) { setErro("Erro de conexão: " + err.message); }
  };

  const editarTransacao = (item) => {
    setDescricao(item.description || "");
    setValor(String(item.amount));
    setTipo(item.type || "receita");
    setCategoria(item.category || "outros");
    setEditandoId(item._id);
    setErro("");
    setAbaSidebar("dashboard");
  };

  const removerTransacao = async (id) => {
    if (!confirm("Deseja remover esta transação?")) return;
    try {
      const res = await fetch(`${API}/transactions/${id}`, {
        method: "DELETE", headers: authHeaders(),
      });
      if (!res.ok) { setErro("Erro ao remover transação."); return; }
      if (editandoId === id) limparFormulario();
      carregarTransacoes();
    } catch (err) { setErro("Erro de conexão: " + err.message); }
  };

  const handleSair = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    sair();
  };

  // ── Gráfico de barras — Gastos por categoria ───────────────────────────────
  const GraficoCategoria = () => (
    <div>
      <h4 style={{ color: "#94a3b8", margin: "0 0 16px" }}>Despesas por categoria</h4>
      {dadosCategorias.length === 0 ? (
        <p style={styles.smallText}>Nenhuma despesa registrada.</p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={dadosCategorias} margin={{ top: 4, right: 10, left: 10, bottom: 4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="categoria" tick={{ fill: "#94a3b8", fontSize: 12 }}
              tickFormatter={v => v.charAt(0).toUpperCase() + v.slice(1)} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }}
              tickFormatter={v => `R$${v}`} width={60} />
            <Tooltip content={<TooltipMoeda />} />
            <Bar dataKey="valor" name="Despesa" fill="#ef4444" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );

  // ── Gráfico de barras — Receitas vs Despesas por mês ──────────────────────
  const GraficoMensal = () => (
    <div>
      <h4 style={{ color: "#94a3b8", margin: "0 0 16px" }}>Receitas vs Despesas por mês</h4>
      {dadosMensais.length === 0 ? (
        <p style={styles.smallText}>Nenhum dado mensal disponível.</p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={dadosMensais} margin={{ top: 4, right: 10, left: 10, bottom: 4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="mes" tick={{ fill: "#94a3b8", fontSize: 12 }} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }}
              tickFormatter={v => `R$${v}`} width={60} />
            <Tooltip content={<TooltipMoeda />} />
            <Legend wrapperStyle={{ color: "#94a3b8", fontSize: "13px" }} />
            <Bar dataKey="receitas" name="Receitas" fill="#22c55e" radius={[6, 6, 0, 0]} />
            <Bar dataKey="despesas" name="Despesas" fill="#ef4444" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );

  // ── Renderiza conteúdo conforme aba ────────────────────────────────────────
  const renderConteudo = () => {

    if (abaSidebar === "transacoes" || abaSidebar === "historico") {
      return (
        <section style={styles.fullPanel}>
          <div style={styles.panelHeader}>
            <h3 style={styles.panelTitle}>
              {abaSidebar === "historico" ? "Histórico completo" : "Transações"}
            </h3>
            <span style={styles.badge}>{transacoesFiltradas.length} registros</span>
          </div>
          {loading && <p style={styles.smallText}>Carregando...</p>}
          <div style={styles.transactions}>
            {transacoesFiltradas.length === 0 && !loading && (
              <p style={styles.smallText}>Nenhuma transação encontrada.</p>
            )}
            {transacoesFiltradas.map(item => (
              <div key={item._id} style={styles.transactionRow}>
                <div>
                  <p style={styles.transactionTitle}>{item.description}</p>
                  <p style={styles.transactionType}>
                    {item.type === "receita" ? "Receita" : "Despesa"} · {item.category}
                    {item.date ? ` · ${new Date(item.date).toLocaleDateString("pt-BR")}` : ""}
                  </p>
                </div>
                <div style={styles.transactionActions}>
                  <strong style={item.type === "receita" ? styles.greenTextSmall : styles.redTextSmall}>
                    {item.type === "receita" ? "+" : "-"} {formatarMoeda(item.amount)}
                  </strong>
                  <button style={styles.editButton} onClick={() => { editarTransacao(item); setAbaSidebar("dashboard"); }}>Editar</button>
                  <button style={styles.removeButton} onClick={() => removerTransacao(item._id)}>Remover</button>
                </div>
              </div>
            ))}
          </div>
        </section>
      );
    }

    // ── Aba Análises — ambos os gráficos ──────────────────────────────────────
    if (abaSidebar === "analises") {
      return (
        <section style={styles.fullPanel}>
          <h3 style={styles.panelTitle}>Análises financeiras</h3>
          <div style={styles.cards}>
            <div style={styles.card}>
              <p style={styles.cardLabel}>Receita total</p>
              <h3 style={styles.greenText}>{formatarMoeda(receitas)}</h3>
            </div>
            <div style={styles.card}>
              <p style={styles.cardLabel}>Despesa total</p>
              <h3 style={styles.redText}>{formatarMoeda(despesas)}</h3>
            </div>
            <div style={styles.card}>
              <p style={styles.cardLabel}>Saldo atual</p>
              <h3 style={saldo >= 0 ? styles.greenText : styles.redText}>{formatarMoeda(saldo)}</h3>
            </div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginTop: "24px" }}>
            <div style={styles.chartPanel}><GraficoCategoria /></div>
            <div style={styles.chartPanel}><GraficoMensal /></div>
          </div>
        </section>
      );
    }

    if (abaSidebar === "configuracoes") {
      return (
        <section style={styles.fullPanel}>
          <h3 style={styles.panelTitle}>Configurações</h3>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Usuário logado</p>
            <p style={{ color: "#fff", fontSize: "18px", marginTop: "8px" }}>{username}</p>
          </div>
          <div style={{ ...styles.card, marginTop: "16px" }}>
            <p style={styles.cardLabel}>Sessão</p>
            <button style={{ ...styles.removeButton, marginTop: "12px", padding: "12px 20px" }} onClick={handleSair}>
              🚪 Encerrar sessão
            </button>
          </div>
        </section>
      );
    }

    if (abaSidebar === "ajuda") {
      return (
        <section style={styles.fullPanel}>
          <h3 style={styles.panelTitle}>Ajuda</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
            {[
              ["Como adicionar uma transação?", "No Dashboard, preencha descrição, valor, tipo e categoria no painel 'Nova transação' e clique em Adicionar."],
              ["Como editar uma transação?", "Clique no botão Editar ao lado da transação desejada. O formulário será preenchido com os dados atuais."],
              ["Como remover uma transação?", "Clique em Remover ao lado da transação. Uma confirmação será solicitada."],
              ["O que é saldo?", "É a diferença entre o total de receitas e o total de despesas registradas."],
              ["Como usar a busca?", "Digite no campo de busca no topo para filtrar transações por descrição, categoria ou tipo."],
            ].map(([pergunta, resposta]) => (
              <div key={pergunta} style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: "14px", padding: "16px" }}>
                <p style={{ color: "#22c55e", fontWeight: "bold", margin: "0 0 8px" }}>{pergunta}</p>
                <p style={{ color: "#94a3b8", margin: 0, fontSize: "14px" }}>{resposta}</p>
              </div>
            ))}
          </div>
        </section>
      );
    }

    // ── Dashboard principal ────────────────────────────────────────────────────
    return (
      <>
        <section style={styles.cards}>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Receita total</p>
            <h3 style={styles.greenText}>{formatarMoeda(receitas)}</h3>
            <small style={styles.smallGreen}>▲ Entradas registradas</small>
          </div>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Despesa total</p>
            <h3 style={styles.redText}>{formatarMoeda(despesas)}</h3>
            <small style={styles.smallRed}>▼ Saídas registradas</small>
          </div>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Saldo atual</p>
            <h3 style={saldo >= 0 ? styles.greenText : styles.redText}>{formatarMoeda(saldo)}</h3>
            <small style={styles.smallText}>Resultado financeiro</small>
          </div>
          <div style={styles.card}>
            <p style={styles.cardLabel}>Total de transações</p>
            <h3 style={styles.whiteText}>{transacoes.length}</h3>
            <small style={styles.smallText}>Movimentações cadastradas</small>
          </div>
        </section>

        <section style={styles.grid}>
          {/* Gráfico receitas vs despesas por mês */}
          <div style={styles.panelLarge}>
            <div style={styles.panelHeader}>
              <h3 style={styles.panelTitle}>Resumo mensal</h3>
              <span style={styles.badge}>Receitas vs Despesas</span>
            </div>
            <div style={{ marginTop: "12px" }}>
              <GraficoMensal />
            </div>
          </div>

          <div style={styles.panel}>
            <h3 style={styles.panelTitle}>Meu cartão</h3>
            <div style={styles.creditCard}>
              <p style={styles.cardBank}>BYTEBANK</p>
              <p style={styles.cardNumber}>•••• •••• •••• 7390</p>
              <div style={styles.cardBottom}>
                <span>{username}</span>
                <span>12/29</span>
              </div>
            </div>
            <button style={styles.addCardButton}>+ Adicionar novo cartão</button>
          </div>

          <div style={styles.panel}>
            <h3 style={styles.panelTitle}>{editandoId ? "Editar transação" : "Nova transação"}</h3>
            <p style={styles.error}>{erro || " "}</p>
            <form onSubmit={handleSubmit} style={styles.form}>
              <input style={styles.input} placeholder="Descrição" value={descricao}
                onChange={e => { setDescricao(e.target.value); setErro(""); }} />
              <input style={styles.input} type="number" step="0.01" min="0"
                placeholder="Valor (ex: 0.00)" value={valor}
                onChange={e => { setValor(e.target.value); setErro(""); }} />
              <select style={styles.input} value={tipo} onChange={e => setTipo(e.target.value)}>
                <option value="receita">Receita</option>
                <option value="despesa">Despesa</option>
              </select>
              <select style={styles.input} value={categoria} onChange={e => setCategoria(e.target.value)}>
                <option value="outros">Outros</option>
                <option value="alimentacao">Alimentação</option>
                <option value="transporte">Transporte</option>
                <option value="saude">Saúde</option>
                <option value="educacao">Educação</option>
                <option value="lazer">Lazer</option>
                <option value="moradia">Moradia</option>
                <option value="salario">Salário</option>
                <option value="investimento">Investimento</option>
              </select>
              <button style={styles.primaryButton} type="submit">
                {editandoId ? "Salvar edição" : "Adicionar"}
              </button>
              {editandoId && (
                <button style={styles.secondaryButton} type="button" onClick={limparFormulario}>
                  Cancelar edição
                </button>
              )}
            </form>
          </div>

          {/* Gráfico de categorias */}
          <div style={styles.panelLarge}>
            <div style={styles.panelHeader}>
              <h3 style={styles.panelTitle}>Gastos por categoria</h3>
              <span
                style={{ ...styles.smallText, cursor: "pointer", color: "#22c55e" }}
                onClick={() => setAbaSidebar("analises")}
              >
                Ver análise completa →
              </span>
            </div>
            <div style={{ marginTop: "12px" }}>
              <GraficoCategoria />
            </div>
          </div>

          <div style={styles.panel}>
            <h3 style={styles.panelTitle}>Últimas transações</h3>
            {loading && <p style={styles.smallText}>Carregando...</p>}
            <div style={styles.transactions}>
              {transacoesFiltradas.length === 0 && !loading && (
                <p style={styles.smallText}>Nenhuma transação encontrada.</p>
              )}
              {transacoesFiltradas.slice(0, 4).map(item => (
                <div key={item._id} style={styles.transactionRow}>
                  <div>
                    <p style={styles.transactionTitle}>{item.description}</p>
                    <p style={styles.transactionType}>
                      {item.type === "receita" ? "Receita" : "Despesa"} · {item.category}
                    </p>
                  </div>
                  <div style={styles.transactionActions}>
                    <strong style={item.type === "receita" ? styles.greenTextSmall : styles.redTextSmall}>
                      {item.type === "receita" ? "+" : "-"} {formatarMoeda(item.amount)}
                    </strong>
                    <button style={styles.editButton} onClick={() => editarTransacao(item)}>Editar</button>
                    <button style={styles.removeButton} onClick={() => removerTransacao(item._id)}>Remover</button>
                  </div>
                </div>
              ))}
            </div>
            <p style={{ ...styles.smallText, cursor: "pointer", color: "#22c55e", marginTop: "12px" }}
              onClick={() => setAbaSidebar("historico")}>
              Ver todas →
            </p>
          </div>
        </section>
      </>
    );
  };

  const menuItems = [
    { id: "dashboard", label: "🏠 Dashboard" },
    { id: "transacoes", label: "💸 Transações" },
    { id: "analises", label: "📊 Análises" },
    { id: "historico", label: "🕘 Histórico" },
  ];
  const menuGeral = [
    { id: "configuracoes", label: "⚙️ Configurações" },
    { id: "ajuda", label: "❓ Ajuda" },
  ];

  return (
    <div style={styles.page}>
      <aside style={styles.sidebar}>
        <div>
          <h1 style={styles.sidebarLogo}>ByteBank</h1>
          <p style={styles.menuTitle}>MENU</p>
          {menuItems.map(m => (
            <button key={m.id}
              style={abaSidebar === m.id ? styles.menuActive : styles.menuItem}
              onClick={() => setAbaSidebar(m.id)}>
              {m.label}
            </button>
          ))}
          <p style={styles.menuTitle}>GERAL</p>
          {menuGeral.map(m => (
            <button key={m.id}
              style={abaSidebar === m.id ? styles.menuActive : styles.menuItem}
              onClick={() => setAbaSidebar(m.id)}>
              {m.label}
            </button>
          ))}
        </div>
        <button style={styles.logoutButton} onClick={handleSair}>🚪 Sair</button>
      </aside>

      <main style={styles.main}>
        <div style={styles.header}>
          <div>
            <h2 style={styles.welcome}>Bem-vindo, {username} 👋</h2>
            <p style={styles.subtitle}>Controle suas receitas e despesas</p>
          </div>
          <input style={styles.search} placeholder="Buscar transação..."
            type="text" value={busca} onChange={e => setBusca(e.target.value)} />
        </div>
        {renderConteudo()}
      </main>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", display: "flex", background: "#0f172a", color: "#fff", fontFamily: "Arial, sans-serif" },
  sidebar: { width: "230px", background: "#020617", padding: "24px", display: "flex", flexDirection: "column", justifyContent: "space-between", flexShrink: 0 },
  sidebarLogo: { color: "#22c55e", marginBottom: "35px" },
  menuTitle: { color: "#64748b", fontSize: "12px", marginTop: "25px" },
  menuActive: { width: "100%", background: "#1e293b", color: "#fff", border: "1px solid #334155", borderRadius: "10px", padding: "12px", textAlign: "left", marginBottom: "8px", cursor: "pointer" },
  menuItem: { width: "100%", background: "transparent", color: "#94a3b8", border: "none", borderRadius: "10px", padding: "12px", textAlign: "left", marginBottom: "6px", cursor: "pointer" },
  logoutButton: { background: "#ef4444", color: "#fff", border: "none", borderRadius: "10px", padding: "12px", cursor: "pointer", fontWeight: "bold" },
  main: { flex: 1, padding: "28px", overflow: "auto" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "25px", gap: "20px" },
  welcome: { margin: 0, fontSize: "28px" },
  subtitle: { color: "#94a3b8", marginTop: "6px" },
  search: { width: "260px", background: "#1e293b", color: "#fff", border: "1px solid #334155", borderRadius: "10px", padding: "12px", outline: "none" },
  cards: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "18px", marginBottom: "22px" },
  card: { background: "#1e293b", border: "1px solid #334155", borderRadius: "18px", padding: "20px", boxShadow: "0 10px 25px rgba(0,0,0,0.25)" },
  cardLabel: { color: "#94a3b8", margin: "0 0 18px" },
  greenText: { color: "#22c55e", fontSize: "26px", margin: 0 },
  redText: { color: "#ef4444", fontSize: "26px", margin: 0 },
  whiteText: { color: "#fff", fontSize: "26px", margin: 0 },
  smallText: { color: "#94a3b8", fontSize: "13px" },
  smallGreen: { color: "#86efac", fontSize: "13px" },
  smallRed: { color: "#fca5a5", fontSize: "13px" },
  grid: { display: "grid", gridTemplateColumns: "1.4fr 0.9fr", gap: "20px" },
  panel: { background: "#1e293b", border: "1px solid #334155", borderRadius: "18px", padding: "20px", boxShadow: "0 10px 25px rgba(0,0,0,0.25)" },
  panelLarge: { background: "#1e293b", border: "1px solid #334155", borderRadius: "18px", padding: "20px", boxShadow: "0 10px 25px rgba(0,0,0,0.25)" },
  fullPanel: { background: "#1e293b", border: "1px solid #334155", borderRadius: "18px", padding: "24px", boxShadow: "0 10px 25px rgba(0,0,0,0.25)" },
  chartPanel: { background: "#0f172a", border: "1px solid #334155", borderRadius: "14px", padding: "20px" },
  panelHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" },
  panelTitle: { marginTop: 0 },
  badge: { background: "#334155", color: "#cbd5e1", padding: "8px 12px", borderRadius: "10px", fontSize: "13px" },
  creditCard: { background: "linear-gradient(135deg, #22c55e, #14b8a6)", borderRadius: "18px", padding: "22px", minHeight: "150px", display: "flex", flexDirection: "column", justifyContent: "space-between", marginBottom: "16px" },
  cardBank: { fontWeight: "bold", letterSpacing: "1px" },
  cardNumber: { fontSize: "20px", fontWeight: "bold" },
  cardBottom: { display: "flex", justifyContent: "space-between", fontSize: "13px" },
  addCardButton: { width: "100%", background: "#334155", color: "#fff", border: "none", borderRadius: "10px", padding: "12px", cursor: "pointer" },
  form: { display: "flex", flexDirection: "column", gap: "10px" },
  input: { background: "#334155", color: "#fff", border: "none", borderRadius: "10px", padding: "12px", outline: "none" },
  error: { color: "#ef4444", minHeight: "20px", fontSize: "14px" },
  primaryButton: { background: "#22c55e", color: "#fff", border: "none", borderRadius: "10px", padding: "12px", cursor: "pointer", fontWeight: "bold" },
  secondaryButton: { background: "#475569", color: "#fff", border: "none", borderRadius: "10px", padding: "12px", cursor: "pointer", fontWeight: "bold" },
  transactions: { display: "flex", flexDirection: "column", gap: "10px", marginTop: "10px" },
  transactionRow: { display: "flex", justifyContent: "space-between", alignItems: "center", background: "#334155", borderRadius: "14px", padding: "14px", gap: "12px" },
  transactionTitle: { margin: 0, fontWeight: "bold" },
  transactionType: { margin: "4px 0 0", color: "#cbd5e1", fontSize: "13px" },
  transactionActions: { display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" },
  greenTextSmall: { color: "#22c55e" },
  redTextSmall: { color: "#ef4444" },
  editButton: { background: "#3b82f6", color: "#fff", border: "none", borderRadius: "8px", padding: "8px 10px", cursor: "pointer" },
  removeButton: { background: "#475569", color: "#fff", border: "none", borderRadius: "10px", padding: "8px 10px", cursor: "pointer" },
  legend: { display: "flex", justifyContent: "center", gap: "18px" },
  legendItem: { color: "#cbd5e1", fontSize: "13px" },
};

export default Dashboard;
