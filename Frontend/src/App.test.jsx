import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "./App";


// TESTE 1 - Renderiza tela de login
test("deve mostrar a tela de login inicialmente", () => {
  render(<App />);
  expect(screen.getByText("Acesse sua conta")).toBeInTheDocument();
});


// TESTE 2 - Navega para cadastro ao clicar em "Cadastrar"
test("deve mudar para tela de cadastro ao clicar em cadastrar", () => {
  render(<App />);
  
  const botaoCadastro = screen.getByText("Cadastrar");
  fireEvent.click(botaoCadastro);

  expect(screen.getByText("Crie sua conta gratuita")).toBeInTheDocument();
});


// TESTE 3 - Navega de volta para login ao clicar em "Entrar"
test("deve voltar para login ao clicar em entrar", () => {
  render(<App />);
  
  fireEvent.click(screen.getByText("Cadastrar"));
  fireEvent.click(screen.getByText("Entrar"));

  expect(screen.getByText("Acesse sua conta")).toBeInTheDocument();
});


// TESTE 4 - Preenchimento dos inputs
test("deve permitir digitar nos campos de login", () => {
  render(<App />);
  
  const emailInput = screen.getByPlaceholderText("Seu email");
  const senhaInput = screen.getByPlaceholderText("Sua senha");

  fireEvent.change(emailInput, { target: { value: "teste@email.com" } });
  fireEvent.change(senhaInput, { target: { value: "123456" } });

  expect(emailInput.value).toBe("teste@email.com");
  expect(senhaInput.value).toBe("123456");
});