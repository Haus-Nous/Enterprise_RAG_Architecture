import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Send, Bot, User, Database, Settings,
  RefreshCcw, FileText, ChevronDown, ChevronRight, CheckCircle2, AlertCircle, Play, Loader2
} from 'lucide-react';
import DragDropUpload from './components/DragDropUpload';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isIndexing, setIsIndexing] = useState(false);
  const [indexStats, setIndexStats] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle focusing input on load
  useEffect(() => {
    inputRef.current?.focus();

    // Add initial welcome message
    setMessages([
      {
        id: 'welcome',
        role: 'bot',
        content: "Hi! I'm Ask My Docs, your specialized RAG assistant. I've been engineered with Hybrid Retrieval and strict Citation Enforcement to ensure factual accuracy.\n\nAsk me a question about your documents, and I'll find the exact sources.",
        evidence: []
      }
    ]);
  }, []);

  const handleReindex = async () => {
    setIsIndexing(true);
    try {
      const response = await fetch('http://localhost:8000/api/index', {
        method: 'POST',
      });
      if (response.ok) {
        const data = await response.json();
        setIndexStats(data.indexed_stats);
      } else {
        console.error("Index failed");
      }
    } catch (error) {
      console.error('Error reindexing:', error);
    } finally {
      setIsIndexing(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMsg.content, top_k: 5 }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMsg = {
          id: (Date.now() + 1).toString(),
          role: 'bot',
          content: data.answer,
          evidence: data.evidence,
          execTime: data.execution_time_seconds
        };
        setMessages(prev => [...prev, botMsg]);
      } else {
        throw new Error('API Request failed');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'bot',
        content: "Sorry, I encountered an error connecting to the intelligence backend. Please ensure the FastAPI server is running on port 8000.",
        isError: true
      }]);
    } finally {
      setIsLoading(false);
      setTimeout(() => inputRef.current?.focus(), 10);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Evidence Accordion Component
  const EvidenceBlock = ({ evidence }) => {
    const [isOpen, setIsOpen] = useState(false);

    if (!evidence || evidence.length === 0) return null;

    return (
      <div className="evidence-section">
        <div
          className="evidence-header"
          onClick={() => setIsOpen(!isOpen)}
          style={{ cursor: 'pointer', userSelect: 'none' }}
        >
          {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <span>{evidence.length} Sources Retrieved by Cross-Encoder</span>
        </div>

        {isOpen && (
          <div className="evidence-cards">
            {evidence.map((source, idx) => (
              <div key={idx} className="evidence-card">
                <div className="evidence-card-header">
                  <div className="evidence-source">
                    <FileText size={14} />
                    {source.source_file.split('/').pop()}
                  </div>
                  <div className="evidence-score">
                    {(source.similarity_score * 100).toFixed(1)}% Match
                  </div>
                </div>
                <div className="evidence-text">
                  "{source.content}"
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <Database className="logo-icon" size={24} />
          <h1>Ask My Docs</h1>
        </div>

        <div className="sidebar-content">
          <div className="status-card">
            <h3>Knowledge Base</h3>
            <div className="db-stats">
              <div className="stat-row">
                <span>Vector Semantic Search</span>
                <span className="stat-value"><CheckCircle2 size={14} color="var(--success-color)" /></span>
              </div>
              <div className="stat-row">
                <span>BM25 Keyword Search</span>
                <span className="stat-value"><CheckCircle2 size={14} color="var(--success-color)" /></span>
              </div>

              {indexStats && (
                <>
                  <hr style={{ borderColor: 'var(--border-color)', margin: '8px 0' }} />
                  <div className="stat-row">
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Latest Sync</span>
                  </div>
                  <div className="stat-row">
                    <span>Documents</span>
                    <span className="stat-value">{indexStats.documents_processed}</span>
                  </div>
                  <div className="stat-row">
                    <span>Embeddings</span>
                    <span className="stat-value">{indexStats.chunks_generated}</span>
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="sidebar-section">
            <h3 className="section-title">ADD DOCUMENTS</h3>
            <DragDropUpload onUploadSuccess={handleReindex} />
          </div>

          <button
            className="btn-primary"
            onClick={handleReindex}
            disabled={isIndexing}
          >
            {isIndexing ? (
              <><RefreshCcw size={16} className="typing-dot" style={{ animationDuration: '2s' }} /> Syncing...</>
            ) : (
              <><RefreshCcw size={16} /> Re-Index Database</>
            )}
          </button>

          <div style={{ marginTop: 'auto' }}>
            <div className="status-card" style={{ border: 'none', background: 'transparent', padding: '0 8px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              <p><AlertCircle size={12} style={{ display: 'inline', marginRight: '4px', position: 'relative', top: '2px' }} /> Responses are synthesized using a Local Ollama Model and constrained by retrieved factual context.</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="main-content">
        <header className="chat-header">
          <div className="header-title">Enterprise Knowledge Retrieval</div>
          <div className="header-badge">Production RAG</div>
        </header>

        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <Bot className="empty-icon" size={48} />
              <h2>How can I help you today?</h2>
              <p>Ask questions about your loaded documents. I use Hybrid Retrieval and Cross-Encoder re-ranking to provide highly accurate, cited answers.</p>
            </div>
          ) : (
            messages.map((msg) => (
              <div key={msg.id} className={`message-wrapper ${msg.role}`}>
                <div className="message">
                  <div className={`avatar ${msg.role}`}>
                    {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                  </div>
                  <div className="message-content">
                    {msg.isError ? (
                      <div style={{ color: 'var(--danger-color)' }}>{msg.content}</div>
                    ) : (
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    )}

                    {/* Render Evidence if we have it */}
                    {msg.role === 'bot' && msg.evidence && msg.evidence.length > 0 && (
                      <EvidenceBlock evidence={msg.evidence} />
                    )}

                    {/* execution time stat */}
                    {msg.execTime && (
                      <div className="exec-stats">
                        Resolved in {msg.execTime.toFixed(2)}s
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="message-wrapper bot">
              <div className="message">
                <div className="avatar bot"><Bot size={20} /></div>
                <div className="message-content" style={{ display: 'flex', alignItems: 'center' }}>
                  <div className="typing-indicator">
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                  </div>
                  <span style={{ marginLeft: '12px', fontSize: '0.85rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                    Running Hybrid Retrieval & Re-ranking...
                  </span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-container">
            <textarea
              ref={inputRef}
              className="chat-input"
              placeholder="Ask a question about your documents..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            <button
              className="send-button"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
            >
              <Send size={20} />
            </button>
          </div>
          <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
            Ask My Docs may hallucinate if evidence is not present. Always verify source citations.
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
