import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { SquadModeToggle } from '@/components/squad/SquadModeToggle';
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { useGetProjectsQuery } from '@/store/api/projectsApi';
import { useGetClientsQuery } from '@/store/api/clientsApi';
import { toggleSquadMode } from '@/store/slices/squadSlice';
import { useNavigate } from 'react-router-dom';
import { formatCurrency } from '@/utils/helpers';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { data: projects = [] } = useGetProjectsQuery();
  const { data: clients = [] } = useGetClientsQuery();
  const { isSquadMode } = useAppSelector((state) => state.squad);

  // Calculate stats
  const activeProjects = projects.filter((p) => p.status === 'In Progress').length;
  const totalBudget = projects.reduce((sum, p) => sum + p.budget, 0);
  const allTeamMembers = new Set(
    projects.flatMap((p) => p.teamMembers.map((m) => m.id))
  );

  const handleToggleSquadMode = () => {
    dispatch(toggleSquadMode());
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-sm text-gray-600 mt-1">
            Overview of your projects and team
          </p>
        </div>
        <SquadModeToggle
          isSquadMode={isSquadMode}
          onToggle={handleToggleSquadMode}
        />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => navigate('/projects')}>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <span>📋</span>
              <span>Projects</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary-600">{projects.length}</p>
            <p className="text-sm text-gray-500">{activeProjects} active</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => navigate('/clients')}>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <span>👥</span>
              <span>Clients</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary-600">{clients.length}</p>
            <p className="text-sm text-gray-500">active clients</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <span>💰</span>
              <span>Budget</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary-600">
              {formatCurrency(totalBudget)}
            </p>
            <p className="text-sm text-gray-500">total allocated</p>
          </CardContent>
        </Card>

        <Card variant="squad" className="hover:shadow-xl transition-shadow cursor-pointer" onClick={() => navigate('/squad')}>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <span>🎭</span>
              <span>Squad Mode</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-secondary-600">6</p>
            <p className="text-sm text-gray-700">
              {isSquadMode ? 'Specialists Active' : 'Specialists Ready'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>🚀 Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Button onClick={() => navigate('/projects')}>
              📋 Create Project
            </Button>
            <Button variant="outline" onClick={() => navigate('/clients')}>
              👥 Add Client
            </Button>
            {isSquadMode && (
              <Button variant="squad" onClick={() => navigate('/squad')}>
                🎭 Run Squad Analysis
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Recent Projects */}
      {projects.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>📅 Recent Projects</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {projects.slice(0, 5).map((project) => (
                <div
                  key={project.id}
                  className="flex items-center justify-between p-3 rounded-md hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => navigate('/projects')}
                >
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{project.name}</p>
                    <p className="text-sm text-gray-600">{project.clientName}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{project.progress}%</p>
                    <p className="text-xs text-gray-500">{project.status}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Dashboard;
