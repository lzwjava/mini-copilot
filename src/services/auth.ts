const GITHUB_CLIENT_ID = 'Iv1.b507a08c87ecfe98'; // Standard GitHub Copilot Client ID
const GITHUB_REDIRECT_URI = window.location.origin;

export interface CopilotTokenResponse {
  token: string;
  expires_at: number;
  refresh_in: number;
}

export const AuthService = {
  getGithubToken(): string | null {
    return localStorage.getItem('github_token');
  },

  setGithubToken(token: string) {
    localStorage.setItem('github_token', token);
  },

  getCopilotToken(): string | null {
    const tokenData = localStorage.getItem('copilot_token');
    if (!tokenData) return null;
    
    const { token, expires_at } = JSON.parse(tokenData);
    // Add 5 minute buffer
    if (Date.now() / 1000 > (expires_at - 300)) {
      localStorage.removeItem('copilot_token');
      return null;
    }
    return token;
  },

  async fetchCopilotToken(githubToken: string): Promise<CopilotTokenResponse> {
    const response = await fetch('https://api.github.com/copilot_internal/v2/token', {
      headers: {
        'Authorization': `token ${githubToken}`,
        'Accept': 'application/json',
        'Editor-Version': 'vscode/1.91.0',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch Copilot token. Make sure you have Copilot access.');
    }

    const data = await response.json();
    localStorage.setItem('copilot_token', JSON.stringify({
      token: data.token,
      expires_at: data.expires_at,
    }));
    
    return data;
  },

  redirectToGithub() {
    const scopes = 'read:user'; 
    const url = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&scope=${scopes}&redirect_uri=${GITHUB_REDIRECT_URI}`;
    window.location.href = url;
  },

  async exchangeCodeForToken(code: string): Promise<string> {
    // NOTE: GitHub's access_token endpoint does not support CORS.
    // In an enterprise environment, you should use a backend proxy.
    // Example: const PROXY_URL = 'https://your-api.com/auth/github';
    
    const PROXY_URL = 'https://github.com/login/oauth/access_token'; 
    
    try {
      const response = await fetch(PROXY_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          client_id: GITHUB_CLIENT_ID,
          code: code,
          redirect_uri: GITHUB_REDIRECT_URI,
        }),
      });

      if (!response.ok) throw new Error('Failed to exchange code');
      
      const data = await response.json();
      if (data.access_token) return data.access_token;
      throw new Error(data.error_description || 'No access token received');
    } catch (error) {
      console.error('Direct token exchange failed:', error);
      throw new Error('Token exchange failed. A backend proxy might be required for Web OAuth.');
    }
  }
};
