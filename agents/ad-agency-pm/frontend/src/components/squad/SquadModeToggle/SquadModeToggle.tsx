import React from 'react';
import { cn } from '@/utils/helpers';

export interface SquadModeToggleProps {
  isSquadMode: boolean;
  onToggle: (enabled: boolean) => void;
  specialistCount?: number;
  className?: string;
}

const SquadModeToggle: React.FC<SquadModeToggleProps> = ({
  isSquadMode,
  onToggle,
  specialistCount = 6,
  className,
}) => {
  return (
    <div className={cn('flex items-center space-x-4', className)}>
      <div className="flex items-center space-x-2">
        <span className="text-sm font-medium text-gray-700">Solo Mode</span>
        <button
          onClick={() => onToggle(!isSquadMode)}
          className={cn(
            'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
            isSquadMode
              ? 'bg-gradient-to-r from-secondary-600 to-primary-600'
              : 'bg-gray-200'
          )}
          role="switch"
          aria-checked={isSquadMode}
          aria-label="Toggle Squad Mode"
        >
          <span
            className={cn(
              'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
              isSquadMode ? 'translate-x-6' : 'translate-x-1'
            )}
          />
        </button>
        <span className="text-sm font-medium text-gray-700">Squad Mode</span>
      </div>

      {isSquadMode && (
        <div className="flex items-center space-x-2 text-sm text-secondary-600 animate-fade-in">
          <div className="flex -space-x-1">
            {Array.from({ length: specialistCount }).map((_, index) => (
              <div
                key={index}
                className="w-6 h-6 rounded-full bg-gradient-to-r from-secondary-500 to-primary-500 border-2 border-white flex items-center justify-center text-xs font-bold text-white"
                title={`Specialist ${index + 1}`}
              >
                {index + 1}
              </div>
            ))}
          </div>
          <span className="font-medium">{specialistCount} Specialists Ready</span>
        </div>
      )}
    </div>
  );
};

SquadModeToggle.displayName = 'SquadModeToggle';

export default SquadModeToggle;

