import { useState, useEffect, useRef } from 'react'
import './App.css'
import { AuthService } from './services/auth'

function App() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([
    { role: 'assistant', content: 'Hello! I am GitHub Copilot. How can I help you today?' }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    const handleAuth = async () => {
      const urlParams = new URLSearchParams(window.location.search)
      const code = urlParams.get('code')

      if (code) {
        window.history.replaceState({}, document.title, window.location.pathname)
        try {
          setIsLoading(true)
          const token = await AuthService.exchangeCodeForToken(code)
          AuthService.setGithubToken(token)
          setIsLoggedIn(true)
        } catch (error) {
          console.error('Auth error:', error)
          alert('Authentication failed. If you are in a local environment, you might need a proxy for GitHub OAuth.')
        } finally {
          setIsLoading(false)
        }
        return
      }

      const githubToken = AuthService.getGithubToken()
      if (githubToken) {
        setIsLoggedIn(true)
      }
      setIsLoading(false)
    }

    handleAuth()
  }, [])

  const handleLogin = () => {
    AuthService.redirectToGithub()
  }

  const handleLogout = () => {
    localStorage.removeItem('github_token')
    localStorage.removeItem('copilot_token')
    setIsLoggedIn(false)
    setMessages([{ role: 'assistant', content: 'You have been logged out. Please login again to continue.' }])
  }

  const handleSend = async () => {
    if (!inputValue.trim()) return

    const userMessage = { role: 'user', content: inputValue }
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    
    try {
      let copilotToken = AuthService.getCopilotToken()
      const githubToken = AuthService.getGithubToken()

      if (!copilotToken && githubToken) {
        try {
          const data = await AuthService.fetchCopilotToken(githubToken)
          copilotToken = data.token
        } catch (err) {
          console.error('Failed to get copilot token:', err)
          setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Your GitHub token might be expired or doesn\'t have Copilot access.' }])
          return
        }
      }

      if (!copilotToken) {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Please login with GitHub first.' }])
        return
      }

      const response = await fetch('https://api.githubcopilot.com/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${copilotToken}`,
          'Content-Type': 'application/json',
          'Editor-Version': 'vscode/1.91.0',
          'Editor-Plugin-Version': 'copilot-chat/0.17.1',
          'User-Agent': 'GitHubCopilotChat/0.17.1',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          messages: messages.concat(userMessage).map(m => ({ role: m.role, content: m.content })),
          model: 'gpt-4',
          stream: false,
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `Copilot API error: ${response.status}`)
      }

      const data = await response.json()
      const assistantMessage = data.choices[0].message
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}` }])
    }
  }

  if (isLoading) {
    return <div className="loading">Loading...</div>
  }

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <h1 className="login-title">Copilot Chat</h1>
        <p className="login-subtitle">Enterprise Web Edition</p>
        <button onClick={handleLogin} className="login-button">
          Login with GitHub
        </button>
      </div>
    )
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <span className="chat-title">Copilot Chat</span>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type a message..."
          className="chat-input"
        />
        <button onClick={handleSend} className="send-button">
          Send
        </button>
      </div>
    </div>
  )
}

export default App
