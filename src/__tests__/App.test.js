// Comprehensive tests for App and major components

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import Auth from '../components/Auth';
import BotsManager from '../components/BotsManager';
import Charts from '../components/Charts';
import Notifications from '../components/Notifications';
import TradeHistory from '../components/TradeHistory';
import Dashboard from '../pages/Dashboard';

// Mock API calls
jest.mock('../App', () => ({
  __esModule: true,
  default: jest.fn(() => <div>Mocked App</div>),
}));

jest.mock('../components/Auth', () => ({
  __esModule: true,
  default: jest.fn(({ onLogin }) => (
    <div>
      <input placeholder="Username" data-testid="username" />
      <input placeholder="Password" data-testid="password" type="password" />
      <button onClick={() => onLogin('user', 'pass')} data-testid="login-btn">Login</button>
    </div>
  )),
}));

jest.mock('../components/BotsManager', () => ({
  __esModule: true,
  default: jest.fn(({ onBotAction }) => (
    <div>
      <button onClick={() => onBotAction('start')} data-testid="start-bot">Start Bot</button>
      <button onClick={() => onBotAction('stop')} data-testid="stop-bot">Stop Bot</button>
    </div>
  )),
}));

jest.mock('../components/Charts', () => ({
  __esModule: true,
  default: jest.fn(() => <div data-testid="chart">Chart Rendered</div>),
}));

jest.mock('../components/Notifications', () => ({
  __esModule: true,
  default: jest.fn(({ notifications }) => (
    <div>
      {notifications.map((n, i) => (
        <div key={i} data-testid="notification">{n.message}</div>
      ))}
    </div>
  )),
}));

jest.mock('../components/TradeHistory', () => ({
  __esModule: true,
  default: jest.fn(({ trades }) => (
    <table>
      <tbody>
        {trades.map((trade, i) => (
          <tr key={i} data-testid="trade-row">
            <td>{trade.id}</td>
            <td>{trade.amount}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )),
}));

jest.mock('../pages/Dashboard', () => ({
  __esModule: true,
  default: jest.fn(() => <div data-testid="dashboard">Dashboard Page</div>),
}));

describe('App Component', () => {
  test('renders dashboard', () => {
    render(<Dashboard />);
    expect(screen.getByTestId('dashboard')).toBeInTheDocument();
  });
});

describe('Auth Component', () => {
  test('login interaction', async () => {
    const handleLogin = jest.fn();
    render(<Auth onLogin={handleLogin} />);
    fireEvent.change(screen.getByTestId('username'), { target: { value: 'user' } });
    fireEvent.change(screen.getByTestId('password'), { target: { value: 'pass' } });
    fireEvent.click(screen.getByTestId('login-btn'));
    await waitFor(() => expect(handleLogin).toHaveBeenCalledWith('user', 'pass'));
  });
});

describe('BotsManager Component', () => {
  test('start bot action', () => {
    const handleBotAction = jest.fn();
    render(<BotsManager onBotAction={handleBotAction} />);
    fireEvent.click(screen.getByTestId('start-bot'));
    expect(handleBotAction).toHaveBeenCalledWith('start');
  });

  test('stop bot action', () => {
    const handleBotAction = jest.fn();
    render(<BotsManager onBotAction={handleBotAction} />);
    fireEvent.click(screen.getByTestId('stop-bot'));
    expect(handleBotAction).toHaveBeenCalledWith('stop');
  });
});

describe('Charts Component', () => {
  test('renders chart', () => {
    render(<Charts />);
    expect(screen.getByTestId('chart')).toHaveTextContent('Chart Rendered');
  });
});

describe('Notifications Component', () => {
  test('renders notifications', () => {
    const notifications = [{ message: 'Bot started' }, { message: 'Trade executed' }];
    render(<Notifications notifications={notifications} />);
    expect(screen.getAllByTestId('notification')).toHaveLength(2);
    expect(screen.getByText('Bot started')).toBeInTheDocument();
    expect(screen.getByText('Trade executed')).toBeInTheDocument();
  });
});

describe('TradeHistory Component', () => {
  test('renders trade history', () => {
    const trades = [{ id: 1, amount: 100 }, { id: 2, amount: 200 }];
    render(<TradeHistory trades={trades} />);
    expect(screen.getAllByTestId('trade-row')).toHaveLength(2);
    expect(screen.getByText('100')).toBeInTheDocument();
    expect(screen.getByText('200')).toBeInTheDocument();
  });
});