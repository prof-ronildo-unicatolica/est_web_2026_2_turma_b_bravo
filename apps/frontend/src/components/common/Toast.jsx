/**
 * Toast.jsx — Componente de notificação flutuante (Toast / Snackbar).
 *
 * Uso:
 *   import { ToastProvider, useToast } from '../common/Toast';
 *
 *   // No App.jsx, envolva com <ToastProvider>
 *   // Nos componentes, use:
 *   const { showToast } = useToast();
 *   showToast('Reserva criada com sucesso!', 'success');
 *
 * Tipos: 'success' | 'error' | 'warning' | 'info'
 */

import { createContext, useCallback, useContext, useEffect, useState } from 'react';

/* ─── Contexto ─────────────────────────────────────────────────────── */

const ToastContext = createContext(null);

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast precisa estar dentro de <ToastProvider>');
  return ctx;
}

/* ─── Provider ─────────────────────────────────────────────────────── */

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = ++toastId;
    setToasts((prev) => [...prev, { id, message, type, duration, exiting: false }]);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) =>
      prev.map((t) => (t.id === id ? { ...t, exiting: true } : t))
    );
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 300);
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="toast-container" role="status" aria-live="polite">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onClose={removeToast} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

/* ─── Toast Individual ─────────────────────────────────────────────── */

const ICONS = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ',
};

function ToastItem({ toast, onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => onClose(toast.id), toast.duration);
    return () => clearTimeout(timer);
  }, [toast.id, toast.duration, onClose]);

  return (
    <div
      className={`toast toast--${toast.type} ${toast.exiting ? 'toast--exit' : ''}`}
      onClick={() => onClose(toast.id)}
    >
      <span className="toast__icon">{ICONS[toast.type]}</span>
      <span className="toast__message">{toast.message}</span>
      <button className="toast__close" aria-label="Fechar notificação">×</button>
    </div>
  );
}

export default ToastProvider;
