import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAppDispatch } from '@/store/hooks';
import { addProject, updateProject, deleteProject } from '@/store/slices/projectsSlice';
import { addClient, updateClient } from '@/store/slices/clientsSlice';
import {
  setSquadAnalysisProgress,
  setSquadResults,
  setSquadSynthesis,
  addSpecialistResult,
} from '@/store/slices/squadSlice';
import { addNotification } from '@/store/slices/uiSlice';
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
  const dispatch = useAppDispatch();
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
      
      dispatch(
        addNotification({
          type: 'success',
          message: 'Connected to server',
          duration: 3000,
        })
      );
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('WebSocket disconnected');
      
      dispatch(
        addNotification({
          type: 'warning',
          message: 'Connection lost. Reconnecting...',
          duration: 3000,
        })
      );
    });

    newSocket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      reconnectAttempts.current += 1;
    });

    // Project events
    newSocket.on('project:created', (project) => {
      dispatch(addProject(project));
      dispatch(
        addNotification({
          type: 'success',
          message: `Project "${project.name}" created`,
          duration: 5000,
        })
      );
    });

    newSocket.on('project:updated', (project) => {
      dispatch(updateProject(project));
    });

    newSocket.on('project:deleted', ({ id }) => {
      dispatch(deleteProject(id));
      dispatch(
        addNotification({
          type: 'info',
          message: 'Project deleted',
          duration: 3000,
        })
      );
    });

    // Client events
    newSocket.on('client:created', (client) => {
      dispatch(addClient(client));
      dispatch(
        addNotification({
          type: 'success',
          message: `Client "${client.name}" created`,
          duration: 5000,
        })
      );
    });

    newSocket.on('client:updated', (client) => {
      dispatch(updateClient(client));
    });

    // Squad events
    newSocket.on('squad:analysis:started', ({ briefId }) => {
      console.log(`Squad analysis started: ${briefId}`);
    });

    newSocket.on('squad:analysis:progress', ({ briefId, specialist, progress }) => {
      dispatch(setSquadAnalysisProgress({ briefId, specialist, progress, status: 'analyzing' }));
    });

    newSocket.on('squad:specialist:completed', (result) => {
      dispatch(addSpecialistResult(result));
    });

    newSocket.on('squad:analysis:completed', ({ briefId, results }) => {
      dispatch(setSquadResults({ briefId, results }));
      dispatch(
        addNotification({
          type: 'success',
          message: 'Squad analysis completed!',
          duration: 5000,
        })
      );
    });

    newSocket.on('squad:synthesis:completed', ({ briefId, synthesis }) => {
      dispatch(setSquadSynthesis({ briefId, synthesis }));
    });

    // General notifications
    newSocket.on('notification:new', ({ type, message }) => {
      dispatch(addNotification({ type, message, duration: 5000 }));
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [dispatch]);

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

