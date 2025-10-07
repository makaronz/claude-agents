import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import type { SpecialistResult } from '@/types/squad';
import { SPECIALISTS, getSpecialistById } from '@/constants/specialists';
import { cn } from '@/utils/helpers';

export interface SpecialistCardsProps {
  analysisProgress?: Record<string, number>;
  results?: SpecialistResult[];
  isAnalyzing?: boolean;
  className?: string;
}

const SpecialistCards: React.FC<SpecialistCardsProps> = ({
  analysisProgress = {},
  results = [],
  isAnalyzing = false,
  className,
}) => {
  const getProgressColor = (progress: number) => {
    if (progress < 30) return 'bg-red-500';
    if (progress < 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getResult = (specialistId: string) => {
    return results.find((r) => r.specialist === specialistId);
  };

  return (
    <div
      className={cn(
        'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4',
        className
      )}
    >
      {SPECIALISTS.map((specialist) => {
        const progress = analysisProgress[specialist.id] || 0;
        const result = getResult(specialist.id);
        const isComplete = progress === 100 || !!result;

        return (
          <Card key={specialist.id} variant="squad">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <span className="text-2xl">{specialist.icon}</span>
                <div className="flex-1">
                  <div className="text-sm font-medium">{specialist.name}</div>
                  <div className="text-xs text-gray-600">{specialist.role}</div>
                </div>
                {isComplete && (
                  <span className="text-green-500 text-xl" title="Analysis Complete">
                    ✅
                  </span>
                )}
              </CardTitle>
            </CardHeader>

            <CardContent>
              {isAnalyzing && !isComplete && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Progress</span>
                    <span className="font-medium">{progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={cn(
                        'h-2 rounded-full transition-all duration-500',
                        getProgressColor(progress)
                      )}
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                  <p className="text-xs text-gray-600 italic">
                    Analyzing {specialist.role.toLowerCase()}...
                  </p>
                </div>
              )}

              {result && (
                <div className="space-y-3">
                  <div>
                    <h4 className="text-sm font-semibold text-green-600 mb-1">
                      ✅ Analysis Complete
                    </h4>
                    <p className="text-xs text-gray-700 bg-white p-2 rounded border line-clamp-3">
                      {result.analysis}
                    </p>
                  </div>

                  {result.recommendations && result.recommendations.length > 0 && (
                    <div>
                      <h5 className="text-xs font-semibold text-gray-700 mb-1">
                        Key Recommendations:
                      </h5>
                      <ul className="text-xs text-gray-600 space-y-1">
                        {result.recommendations.slice(0, 3).map((rec, index) => (
                          <li key={index} className="flex items-start">
                            <span className="mr-1">•</span>
                            <span className="line-clamp-2">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {!isAnalyzing && !result && (
                <div className="text-center py-4">
                  <p className="text-sm text-gray-500 italic">Waiting to start...</p>
                </div>
              )}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};

SpecialistCards.displayName = 'SpecialistCards';

export default SpecialistCards;

