import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import { projectsApi } from './api/projectsApi';
import { clientsApi } from './api/clientsApi';
import { squadApi } from './api/squadApi';
import projectsReducer from './slices/projectsSlice';
import clientsReducer from './slices/clientsSlice';
import squadReducer from './slices/squadSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    projects: projectsReducer,
    clients: clientsReducer,
    squad: squadReducer,
    ui: uiReducer,
    [projectsApi.reducerPath]: projectsApi.reducer,
    [clientsApi.reducerPath]: clientsApi.reducer,
    [squadApi.reducerPath]: squadApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(projectsApi.middleware)
      .concat(clientsApi.middleware)
      .concat(squadApi.middleware),
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Export hooks
export { useAppDispatch, useAppSelector } from './hooks';

