import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/common/Card';

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Projects</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary-600">12</p>
            <p className="text-sm text-gray-500">Active Projects</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Team</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary-600">8</p>
            <p className="text-sm text-gray-500">Team Members</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Budget</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary-600">$45k</p>
            <p className="text-sm text-gray-500">Remaining</p>
          </CardContent>
        </Card>
        
        <Card variant="squad">
          <CardHeader>
            <CardTitle>Squad Mode</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-secondary-600">6</p>
            <p className="text-sm text-gray-700">Specialists Ready</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
