import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { vi } from "vitest";

import Login from "../Login";
import Dashboard from "../Dashboard";

describe("Testes com Mock - ByteBank", () => {

  test("deve chamar irDashboard após login válido", () => {
    vi.useFakeTimers();

    const irDashboardMock = vi.fn();
    const mudarTelaMock = vi.fn();

    render(
      <Login
        mudarTela={mudarTelaMock}
        irDashboard={irDashboardMock}
      />
    );

    fireEvent.change(screen.getByPlaceholderText("Seu email"), {
      target: { value: "teste@email.com" },
    });

    fireEvent.change(screen.getByPlaceholderText("Sua senha"), {
      target: { value: "123456" },
    });

    fireEvent.click(screen.getByText("Entrar"));

    vi.runAllTimers();

    expect(irDashboardMock).toHaveBeenCalled();

    vi.useRealTimers();
  });

  test("deve chamar sair ao clicar no botão sair do dashboard", () => {
    const sairMock = vi.fn();

    render(<Dashboard sair={sairMock} />);

    fireEvent.click(screen.getByText("Sair"));

    expect(sairMock).toHaveBeenCalled();
  });

});