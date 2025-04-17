import { useState, useRef, useEffect } from 'react';
import {
  Container,
  TextField,
  Button,
  Paper,
  Typography,
  Box,
  CircularProgress,
  createTheme,
  ThemeProvider,
  Link,
} from '@mui/material';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1976d2' },
    background: { default: '#e0f2f1', paper: '#ffffff' },
    text: { primary: '#333333', secondary: '#666666' },
  },
});

function App() {
  const [prompt, setPrompt] = useState('');
  const [schema, setSchema] = useState('');
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem('chatHistory');
    return savedMessages ? JSON.parse(savedMessages) : [];
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(messages));
  }, [messages]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);

    const userMessage = { type: 'user', text: prompt, timestamp: new Date().toISOString() };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, schema }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }

      const botMessage = {
        type: 'bot',
        text: data.text_result,
        csv_content: data.csv_content,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: 'bot', text: `Error: ${err.message}`, timestamp: new Date().toISOString() },
      ]);
    } finally {
      setLoading(false);
      setPrompt('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleDownload = (csvContent, prompt) => {
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `results_${prompt.substring(0, 20).replace(' ', '_')}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(to bottom right, rgba(2, 43, 140, 0.85), rgb(11, 75, 70))',
          py: 4,
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h4" align="center" color="#fefefe" gutterBottom>
            Reso Researcher Chat Agent
          </Typography>

          <Paper
            elevation={4}
            sx={{
              p: 2,
              mb: 2,
              height: '60vh',
              overflowY: 'auto',
              backgroundColor: '#fefefe',
              borderRadius: '12px',
            }}
          >
            {messages.map((msg, idx) => (
              <Box
                key={idx}
                display="flex"
                justifyContent={msg.type === 'user' ? 'flex-end' : 'flex-start'}
                mb={2}
              >
                <Box
                  sx={{
                    px: 2,
                    py: 1,
                    borderRadius: 2,
                    maxWidth: '80%',
                    bgcolor: msg.type === 'user' ? '#1976d2' : '#f0f0f0',
                    color: msg.type === 'user' ? '#fff' : '#333',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    boxShadow: 1,
                  }}
                >
                  {msg.type === 'bot' && msg.csv_content ? (
                    <>
                      {msg.text}
                      <Link
                        component="button"
                        onClick={() => handleDownload(msg.csv_content, messages.find(m => m.type === 'user' && m.timestamp === msg.timestamp)?.text || 'results')}
                        sx={{ ml: 1, color: '#1976d2', textDecoration: 'underline' }}
                      >
                        Download CSV
                      </Link>
                    </>
                  ) : (
                    msg.text
                  )}
                </Box>
              </Box>
            ))}
            <div ref={chatEndRef} />
          </Paper>

          <TextField
            label="Schema (optional)"
            fullWidth
            value={schema}
            onChange={(e) => setSchema(e.target.value)}
            margin="normal"
            sx={{ backgroundColor: '#ffffff', borderRadius: 1 }}
          />

          <TextField
            label="Type your message"
            fullWidth
            multiline
            rows={2}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
            sx={{ backgroundColor: '#ffffff', borderRadius: 1 }}
          />

          <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
            <Button
              variant="contained"
              color="primary"
              onClick={handleSend}
              disabled={loading || !prompt.trim()}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Send'}
            </Button>
            {error && (
              <Typography color="error" variant="body2">
                {error}
              </Typography>
            )}
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;