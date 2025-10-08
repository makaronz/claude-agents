import React, { ReactNode } from 'react';
import { ProjectProvider } from './ProjectContext';
import { ClientProvider } from './ClientContext';
import { SquadProvider } from './SquadContext';
import { UIProvider } from './UIContext';

interface AppProvidersProps {
  children: ReactNode;
}

export const AppProviders: React.FC<AppProvidersProps> = ({ children }) => {
  return (
    <UIProvider>
      <ProjectProvider>
        <ClientProvider>
          <SquadProvider>
            {children}
          </SquadProvider>
        </ClientProvider>
      </ProjectProvider>
    </UIProvider>
  );
};

// Re-export all hooks for convenience
export {
  useProjectContext,
  useProjects,
  useSelectedProject,
  useProjectFilters,
  useFilteredProjects,
} from './ProjectContext';

export {
  useClientContext,
  useClients,
} from './ClientContext';

export {
  useSquadContext,
  useSquadMode,
  useSquadAnalysis,
} from './SquadContext';

export {
  useUIContext,
  useSidebar,
  useNotifications,
} from './UIContext';
