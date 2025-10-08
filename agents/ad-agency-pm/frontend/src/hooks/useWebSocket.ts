import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useProjectContext, useClientContext, useSquadContext, useUIContext } from '@/context';
import config from '@/config/environment';

interface WebSocketEvents {
  // Project events
  'project:created': any;
  'project:updated': any;
  'project:deleted': { id: string };

  // Client events
  'client:created': any;
  'client:updated': any;

  // Squad events
  'squad:analysis:started': { briefId: string };
  'squad:analysis:progress': {
    briefId: string;
    specialist: string;
    progress: number;
  };
  'squad:specialist:completed': any;
  'squad:analysis:completed': { briefId: string; results: any[] };
  'squad:synthesis:completed': { briefId: string; synthesis: any };

  // Notifications
  'notification:new': {
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
  };
}

export const useWebSocket = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const { addProject, updateProject, deleteProject } = useProjectContext();
  const { addClient, updateClient } = useClientContext();
  const { updateProgress, addResult, setSynthesis } = useSquadContext();
  const { addNotification } = useUIContext();
  const reconnectAttempts = useRef(0);

  useEffect(() => {
    const newSocket = io(config.WS_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    newSocket.on('connect', () => {
      setConnected(true);
      reconnectAttempts.current = 0;
      console.log('WebSocket connected');
      
      addNotification({
        type: 'success',
        message: 'Connected to server',
      });
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('WebSocket disconnected');
      
      addNotification({
        type: 'warning',
        message: 'Connection lost. Reconnecting...',
      });
    });

    newSocket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      reconnectAttempts.current += 1;
    });

    // Project events
    newSocket.on('project:created', (project) => {
      addProject(project);
      addNotification({
        type: 'success',
        message: `Project "${project.name}" created`,
      });
    });

    newSocket.on('project:updated', (project) => {
      updateProject(project);
    });

    newSocket.on('project:deleted', ({ id }) => {
      deleteProject(id);
      addNotification({
        type: 'info',
        message: 'Project deleted',
      });
    });

    // Client events
    newSocket.on('client:created', (client) => {
      addClient(client);
      addNotification({
        type: 'success',
        message: `Client "${client.name}" created`,
      });
    });

    newSocket.on('client:updated', (client) => {
      updateClient(client);
    });

    // Squad events
    newSocket.on('squad:analysis:started', ({ briefId }) => {
      console.log(`Squad analysis started: ${briefId}`);
    });

    newSocket.on('squad:analysis:progress', ({ briefId, specialist, progress }) => {
      updateProgress({ briefId, specialist, progress, status: 'analyzing' });
    });

    newSocket.on('squad:specialist:completed', (result) => {
      addResult(result);
    });

    newSocket.on('squad:analysis:completed', ({ briefId, results }) => {
      // Handle completed analysis
      addNotification({
        type: 'success',
        message: 'Squad analysis completed!',
      });
    });

    newSocket.on('squad:synthesis:completed', ({ briefId, synthesis }) => {
      setSynthesis(synthesis);
    });

    // General notifications
    newSocket.on('notification:new', ({ type, message }) => {
      addNotification({ type, message });
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [addProject, updateProject, deleteProject, addClient, updateClient, updateProgress, addResult, setSynthesis, addNotification]);

  const emit = <K extends keyof WebSocketEvents>(
    event: K,
    data: WebSocketEvents[K]
  ) => {
    if (socket && connected) {
      socket.emit(event, data);
    } else {
      console.warn('Socket not connected, cannot emit event:', event);
    }
  };

  return { socket, connected, emit };
};

