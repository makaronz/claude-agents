import React from 'react';
import { Button } from '@/components/common/Button';

const Projects: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
        <Button>+ New Project</Button>
      </div>
      
      <div className="bg-white p-8 rounded-lg border border-gray-200">
        <p className="text-gray-500 text-center">
          Project management interface will be implemented here.
        </p>
      </div>
    </div>
  );
};

export default Projects;
