import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useMutation, useQueryClient } from 'react-query';
import { create } from 'zustand';

type Notification = { id: number; message: string };

interface Store {
  role: string;
  notifications: Notification[];
  setRole: (role: string) => void;
  addNotification: (message: string) => void;
}

export const useStore = create<Store>((set) => ({
  role: '',
  notifications: [],
  setRole: (role) => set({ role }),
  addNotification: (message) =>
    set((state) => ({
      notifications: [...state.notifications, { id: Date.now(), message }],
    })),
}));

const Dashboard: React.FC = () => {
  const addNotification = useStore((state) => state.addNotification);

  const mutation = useMutation(
    () =>
      fetch('http://localhost:3000/events/web.action.trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'ping' }),
      }).then((res) => {
        if (!res.ok) throw new Error('Ошибка при отправке события');
        return res.json();
      }),
    {
      onSuccess: () => addNotification('Ping успешно отправлен'),
      onError: (error: any) => addNotification(`Ошибка: ${error.message}`),
    }
  );

  return (
    <div className="dashboard">
      <h1>GG Tesla Dashboard</h1>
      <button
        onClick={() => mutation.mutate()}
        disabled={mutation.isLoading}
        className="ping-button"
      >
        {mutation.isLoading ? 'Отправка...' : 'Ping API'}
      </button>
      <Notifications />
    </div>
  );
};

const Notifications: React.FC = () => {
  const notifications = useStore((state) => state.notifications);
  return (
    <div className="notifications">
      {notifications.map((n) => (
        <div key={n.id} className="notification">
          {n.message}
        </div>
      ))}
    </div>
  );
};

const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Dashboard />} />
    </Routes>
  </BrowserRouter>
);

export default App;
