import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState('1'); // Fixed session ID for simplicity
  const [showConfig, setShowConfig] = useState(false);
  const [showMemoryPanel, setShowMemoryPanel] = useState(false);
  const [memoryStats, setMemoryStats] = useState(null);
  
  // Configuration state
  const [config, setConfig] = useState({
    serverUrl: 'http://localhost:8000/api/v1/query',
    memoryUrl: 'http://localhost:8000/api/v1/memory',
    responseField: 'response',
    provider: 'gemini',
    model: 'gemini-2.5-flash',
    maxSteps: 15,
    temperature: 0.1,
    userId: 'default' // User ID for memory management
  });
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const requestBody = {
        prompt: inputMessage,
        user_id: config.userId,
        provider: config.provider,
        model: config.model,
        max_steps: config.maxSteps,
        temperature: config.temperature
      };

      const response = await fetch(config.serverUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      let responseText = 'Ricevuto!';
      
      if (response.ok) {
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
          // Risposta JSON
          const data = await response.json();
          console.log('Risposta JSON ricevuta:', data);
          
          // Use configured response field
          if (config.responseField && data[config.responseField]) {
            responseText = data[config.responseField];
          } else {
            // Fallback to common response field names
            responseText = data.output || data.response || data.message || data.result || data.data || JSON.stringify(data);
          }
        } else {
          // Risposta di testo semplice
          responseText = await response.text();
          console.log('Risposta di testo ricevuta:', responseText);
        }
      } else {
        responseText = `Errore HTTP ${response.status}: ${response.statusText}`;
      }
      
      const botMessage = {
        id: Date.now() + 1,
        text: responseText,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: `Errore nella comunicazione con il server. Assicurati che il server sia attivo su ${config.serverUrl}`,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const testConnection = async () => {
    const testMessage = {
      id: Date.now(),
      text: '🔧 Test connessione al server...',
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, testMessage]);
    setIsLoading(true);

    try {
      const requestBody = {
        prompt: "Test di connessione",
        user_id: config.userId,
        provider: config.provider,
        model: config.model,
        max_steps: config.maxSteps,
        temperature: config.temperature
      };

      const response = await fetch(config.serverUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      const statusMessage = {
        id: Date.now() + 1,
        text: `✅ Connessione OK! Status: ${response.status} ${response.statusText}`,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, statusMessage]);
    } catch (error) {
      console.error('Connection test failed:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: `❌ Connessione fallita! Verifica che il server sia attivo su ${config.serverUrl}`,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Memory management functions
  const getMemoryStats = async () => {
    try {
      const response = await fetch(`${config.memoryUrl}/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        const stats = await response.json();
        setMemoryStats(stats);
        return stats;
      } else {
        console.error('Failed to get memory stats:', response.statusText);
        return null;
      }
    } catch (error) {
      console.error('Error getting memory stats:', error);
      return null;
    }
  };

  const clearUserMemory = async (userId = null) => {
    const targetUserId = userId || config.userId;
    setIsLoading(true);

    try {
      const requestBody = userId ? { user_id: targetUserId } : {};
      
      const response = await fetch(`${config.memoryUrl}/clear`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (response.ok) {
        const result = await response.json();
        
        const successMessage = {
          id: Date.now(),
          text: `🧹 ${result.message}`,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, successMessage]);

        // Refresh memory stats if panel is open
        if (showMemoryPanel) {
          await getMemoryStats();
        }
      } else {
        const errorMessage = {
          id: Date.now(),
          text: `❌ Errore nella cancellazione memoria: ${response.status} ${response.statusText}`,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString(),
          isError: true
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error clearing memory:', error);
      const errorMessage = {
        id: Date.now(),
        text: `❌ Errore nella cancellazione memoria: ${error.message}`,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearAllMemory = async () => {
    if (!window.confirm('Sei sicuro di voler cancellare TUTTA la memoria delle conversazioni? Questa operazione non può essere annullata.')) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${config.memoryUrl}/clear`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      });

      if (response.ok) {
        const result = await response.json();
        
        const successMessage = {
          id: Date.now(),
          text: `🧹 ${result.message}`,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, successMessage]);

        // Refresh memory stats if panel is open
        if (showMemoryPanel) {
          await getMemoryStats();
        }
      } else {
        const errorMessage = {
          id: Date.now(),
          text: `❌ Errore nella cancellazione memoria globale: ${response.status} ${response.statusText}`,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString(),
          isError: true
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error clearing all memory:', error);
      const errorMessage = {
        id: Date.now(),
        text: `❌ Errore nella cancellazione memoria globale: ${error.message}`,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendQuickMessage = (message) => {
    setInputMessage(message);
    // Auto-send after a short delay
    setTimeout(() => {
      const event = { target: { value: message } };
      setInputMessage(message);
      sendMessage();
    }, 100);
  };

  const updateConfig = (field, value) => {
    setConfig(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const saveConfig = () => {
    localStorage.setItem('chatbotConfig', JSON.stringify(config));
    setShowConfig(false);
  };

  const loadConfig = () => {
    const savedConfig = localStorage.getItem('chatbotConfig');
    if (savedConfig) {
      try {
        const parsedConfig = JSON.parse(savedConfig);
        setConfig(prev => ({ ...prev, ...parsedConfig }));
      } catch (error) {
        console.error('Error loading config:', error);
      }
    }
  };

  // Load config on component mount
  useEffect(() => {
    loadConfig();
  }, []);

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🤖 Chatbot MCP</h1>
          <p>Connesso a: {config.serverUrl}</p>
          <div className="header-buttons">
            <button onClick={() => setShowConfig(!showConfig)} className="config-button">
              ⚙️ Configurazione
            </button>
            <button onClick={() => setShowMemoryPanel(!showMemoryPanel)} className="memory-button">
              🧠 Memoria
            </button>
            <button onClick={clearChat} className="clear-button">
              Pulisci Chat
            </button>
          </div>
        </div>

        {showConfig && (
          <div className="config-panel">
            <h3>⚙️ Configurazione</h3>
            <div className="config-form">
              <div className="config-group">
                <label>URL Server:</label>
                <input
                  type="text"
                  value={config.serverUrl}
                  onChange={(e) => updateConfig('serverUrl', e.target.value)}
                  placeholder="http://localhost:8000/api/v1/query"
                />
              </div>
              
              <div className="config-group">
                <label>Campo Risposta:</label>
                <input
                  type="text"
                  value={config.responseField}
                  onChange={(e) => updateConfig('responseField', e.target.value)}
                  placeholder="response"
                />
              </div>
              
              <div className="config-group">
                <label>Provider:</label>
                <input
                  type="text"
                  value={config.provider}
                  onChange={(e) => updateConfig('provider', e.target.value)}
                  placeholder="gemini"
                />
              </div>
              
              <div className="config-group">
                <label>Modello:</label>
                <input
                  type="text"
                  value={config.model}
                  onChange={(e) => updateConfig('model', e.target.value)}
                  placeholder="gemini-2.5-flash"
                />
              </div>
              
              <div className="config-group">
                <label>Max Steps:</label>
                <input
                  type="number"
                  value={config.maxSteps}
                  onChange={(e) => updateConfig('maxSteps', parseInt(e.target.value))}
                  min="1"
                  max="100"
                />
              </div>
              
              <div className="config-group">
                <label>Temperature:</label>
                <input
                  type="number"
                  value={config.temperature}
                  onChange={(e) => updateConfig('temperature', parseFloat(e.target.value))}
                  min="0"
                  max="2"
                  step="0.1"
                />
              </div>
              
              <div className="config-group">
                <label>URL Memoria:</label>
                <input
                  type="text"
                  value={config.memoryUrl}
                  onChange={(e) => updateConfig('memoryUrl', e.target.value)}
                  placeholder="http://localhost:8000/api/v1/memory"
                />
              </div>
              
              <div className="config-group">
                <label>User ID:</label>
                <input
                  type="text"
                  value={config.userId}
                  onChange={(e) => updateConfig('userId', e.target.value)}
                  placeholder="default"
                />
              </div>
              
              <div className="config-buttons">
                <button onClick={saveConfig} className="save-button">
                  💾 Salva
                </button>
                <button onClick={() => setShowConfig(false)} className="cancel-button">
                  ❌ Annulla
                </button>
              </div>
            </div>
          </div>
        )}

        {showMemoryPanel && (
          <div className="memory-panel">
            <h3>🧠 Gestione Memoria Conversazioni</h3>
            <div className="memory-content">
              <div className="memory-buttons">
                <button onClick={getMemoryStats} className="stats-button">
                  📊 Mostra Statistiche
                </button>
                <button onClick={() => clearUserMemory()} className="clear-user-button">
                  🧹 Pulisci Memoria Utente ({config.userId})
                </button>
                <button onClick={clearAllMemory} className="clear-all-button">
                  🗑️ Pulisci Tutta la Memoria
                </button>
                <button onClick={() => setShowMemoryPanel(false)} className="close-button">
                  ❌ Chiudi
                </button>
              </div>
              
              {memoryStats && (
                <div className="memory-stats">
                  <h4>📈 Statistiche Memoria</h4>
                  <div className="stats-info">
                    <p><strong>Limite messaggi per utente:</strong> {memoryStats.memory_limit}</p>
                    <p><strong>User ID default:</strong> {memoryStats.default_user_id}</p>
                    <p><strong>Utenti attivi:</strong> {memoryStats.active_users}</p>
                  </div>
                  
                  {memoryStats.users && Object.keys(memoryStats.users).length > 0 && (
                    <div className="users-list">
                      <h5>👥 Dettagli Utenti:</h5>
                      {Object.entries(memoryStats.users).map(([userId, userInfo]) => (
                        <div key={userId} className="user-info">
                          <div className="user-details">
                            <strong>{userId}</strong>: {userInfo.message_count} messaggi
                            <span className="last-message">
                              (ultimo: {new Date(userInfo.last_message_time).toLocaleString()})
                            </span>
                          </div>
                          <button 
                            onClick={() => clearUserMemory(userId)} 
                            className="clear-specific-user-button"
                            title={`Pulisci memoria di ${userId}`}
                          >
                            🧹
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        <div className="quick-actions">
          <h3>Messaggi Rapidi:</h3>
          <div className="quick-buttons">
            <button 
              onClick={() => sendQuickMessage("Ciao! elenca i record sulla tabella rubrica")}
              className="quick-button"
            >
              📋 Elenca Rubrica
            </button>
            <button 
              onClick={() => sendQuickMessage("Mostrami tutti i contatti")}
              className="quick-button"
            >
              👥 Tutti i Contatti
            </button>
            <button 
              onClick={() => sendQuickMessage("Crea un nuovo contatto")}
              className="quick-button"
            >
              ➕ Nuovo Contatto
            </button>
            <button 
              onClick={testConnection}
              className="quick-button test-button"
            >
              🔧 Test Connessione
            </button>
            <button 
              onClick={getMemoryStats}
              className="quick-button memory-stats-button"
            >
              📊 Statistiche Memoria
            </button>
            <button 
              onClick={() => clearUserMemory()}
              className="quick-button clear-memory-button"
            >
              🧹 Pulisci Memoria
            </button>
          </div>
        </div>

        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>👋 Benvenuto!</h2>
              <p>Scrivi un messaggio per iniziare a chattare con il bot.</p>
              <p>Il bot è collegato al webhook MCP e può aiutarti a gestire la rubrica.</p>
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
            >
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                <div className="message-time">{message.timestamp}</div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot">
              <div className="message-content">
                <div className="message-text">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Scrivi il tuo messaggio..."
              className="message-input"
              rows="1"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="send-button"
            >
              {isLoading ? '⏳' : '📤'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
