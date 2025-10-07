import React, { useState, useEffect } from 'react';
import { Button } from '@/components/common/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import { Textarea } from '@/components/common/Textarea';
import { SquadModeToggle } from '@/components/squad/SquadModeToggle';
import { SpecialistCards } from '@/components/squad/SpecialistCards';
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { toggleSquadMode, startAnalysis, resetCurrentAnalysis } from '@/store/slices/squadSlice';
import { useStartAnalysisMutation } from '@/store/api/squadApi';
import { useWebSocket } from '@/hooks/useWebSocket';

const Squad: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isSquadMode, currentAnalysis } = useAppSelector((state) => state.squad);
  const [brief, setBrief] = useState('');
  const [startSquadAnalysis, { isLoading }] = useStartAnalysisMutation();
  const { connected } = useWebSocket();

  const handleToggleSquadMode = (enabled: boolean) => {
    dispatch(toggleSquadMode());
  };

  const handleStartAnalysis = async () => {
    if (!brief.trim()) return;

    try {
      const response = await startSquadAnalysis({ brief }).unwrap();
      dispatch(startAnalysis({ briefId: response.briefId, brief }));
    } catch (error) {
      console.error('Failed to start analysis:', error);
    }
  };

  const handleReset = () => {
    dispatch(resetCurrentAnalysis());
    setBrief('');
  };

  const isAnalyzing = currentAnalysis.status === 'analyzing';
  const isComplete = currentAnalysis.status === 'completed';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🎭 Squad Mode</h1>
        <p className="text-gray-600 mb-4">Multi-agent creative collaboration</p>
        
        <div className="flex justify-center">
          <SquadModeToggle
            isSquadMode={isSquadMode}
            onToggle={handleToggleSquadMode}
            specialistCount={6}
          />
        </div>
      </div>

      {isSquadMode && (
        <>
          {/* Brief Input */}
          <Card variant="squad">
            <CardHeader>
              <CardTitle>📝 Creative Brief</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Textarea
                  value={brief}
                  onChange={(e) => setBrief(e.target.value)}
                  placeholder="Describe your creative project, target audience, objectives..."
                  disabled={isAnalyzing}
                  rows={6}
                  helperText="Provide as much detail as possible for better analysis"
                />
                
                <div className="flex space-x-3 justify-center">
                  <Button
                    onClick={handleStartAnalysis}
                    disabled={!brief.trim() || isAnalyzing}
                    variant="squad"
                    size="lg"
                    loading={isAnalyzing}
                  >
                    {isAnalyzing ? 'Analyzing...' : '🎯 Start Squad Analysis'}
                  </Button>
                  
                  {(isAnalyzing || isComplete) && (
                    <Button
                      onClick={handleReset}
                      variant="outline"
                      size="lg"
                    >
                      Reset
                    </Button>
                  )}
                </div>

                {!connected && (
                  <p className="text-sm text-warning text-center">
                    ⚠️ WebSocket disconnected - Real-time updates unavailable
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Specialist Analysis */}
          {(isAnalyzing || currentAnalysis.results.length > 0) && (
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                🎭 Specialist Analysis {isAnalyzing && '(In Progress)'}
              </h2>
              <SpecialistCards
                analysisProgress={currentAnalysis.progress}
                results={currentAnalysis.results}
                isAnalyzing={isAnalyzing}
              />
            </div>
          )}

          {/* Synthesis */}
          {currentAnalysis.synthesis && (
            <Card variant="elevated">
              <CardHeader>
                <CardTitle className="text-xl">
                  🎯 Creative Director Synthesis
                  <span className="ml-2 text-sm font-normal text-gray-600">
                    Score: {currentAnalysis.synthesis.score}/10
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Summary</h3>
                    <p className="text-gray-700">{currentAnalysis.synthesis.synthesis}</p>
                  </div>

                  {currentAnalysis.synthesis.actionPlan && currentAnalysis.synthesis.actionPlan.length > 0 && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">Action Plan</h3>
                      <ul className="space-y-2">
                        {currentAnalysis.synthesis.actionPlan.map((action, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-primary-600 mr-2">→</span>
                            <span className="text-gray-700">{action}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="flex space-x-4">
                    <Button variant="squad">
                      📋 Create Project from Analysis
                    </Button>
                    <Button variant="outline">
                      💾 Save Strategy
                    </Button>
                    <Button variant="ghost">
                      📤 Export Report
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}

      {!isSquadMode && (
        <Card className="p-8">
          <div className="text-center space-y-4">
            <p className="text-lg text-gray-700">
              Enable Squad Mode to access multi-agent creative collaboration.
            </p>
            <p className="text-sm text-gray-600">
              6 specialist agents will analyze your creative brief in parallel and provide comprehensive strategy.
            </p>
          </div>
        </Card>
      )}
    </div>
  );
};

export default Squad;
