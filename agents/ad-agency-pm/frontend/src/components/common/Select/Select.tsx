import React from 'react';
import { cn } from '@/utils/helpers';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'squad';
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, helperText, variant = 'default', className, children, ...props }, ref) => {
    const baseClasses = "block w-full rounded-md border-0 py-2 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6";
    
    const variantClasses = {
      default: "bg-white",
      squad: "bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200 focus:ring-purple-600",
    };

    const errorClasses = error 
      ? "ring-red-300 focus:ring-red-600" 
      : "ring-gray-300 focus:ring-primary-600";

    return (
      <div className="space-y-1">
        {label && (
          <label className="block text-sm font-medium text-gray-700">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        
        <select
          ref={ref}
          className={cn(
            baseClasses,
            variantClasses[variant],
            errorClasses,
            className
          )}
          {...props}
        >
          {children}
        </select>
        
        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}
        
        {helperText && !error && (
          <p className="text-gray-500 text-sm">{helperText}</p>
        )}
      </div>
    );
  }
);

Select.displayName = 'Select';

export default Select;
