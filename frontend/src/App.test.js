//Test file for the App component

import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  beforeEach(() => {
    window.location.hash = '';
  });

  test('renders LoginButton when no access token', () => {
    render(<App />);
    const loginButton = screen.getByText(/Log In with Spotify/i);
    expect(loginButton).toBeInTheDocument();
  });

  test('allows selecting mood and fetching tracks', async () => {
    window.location.hash = '#access_token=mock_token';
    render(<App />);

    const select = screen.getByLabelText(/What mood are you in/i);
    expect(select).toBeInTheDocument();
  });
});

