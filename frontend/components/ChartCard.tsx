"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Download } from "lucide-react";

interface ChartCardProps {
  title: string;
  subtitle?: string;
  data: any[];
  dataKey: string;
  color?: string;
  showLegend?: boolean;
}

export default function ChartCard({ 
  title, 
  subtitle, 
  data, 
  dataKey, 
  color = "#2563eb",
  showLegend = false 
}: ChartCardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-sm font-semibold text-gray-900">{title}</h3>
          {subtitle && (
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs font-medium text-gray-700 bg-gray-100 px-2 py-1 rounded">FRED</span>
              <span className="text-xs text-gray-500">{subtitle}</span>
            </div>
          )}
        </div>
        <button className="text-gray-400 hover:text-gray-600 transition-colors">
          <Download size={16} />
        </button>
      </div>
      
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="0" stroke="#f3f4f6" vertical={false} />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 10, fill: '#6b7280' }}
            tickLine={false}
            axisLine={{ stroke: '#e5e7eb' }}
          />
          <YAxis 
            tick={{ fontSize: 10, fill: '#6b7280' }}
            tickLine={false}
            axisLine={false}
            domain={['dataMin', 'dataMax']}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
              fontSize: '12px'
            }}
          />
          {showLegend && <Legend wrapperStyle={{ fontSize: '12px' }} />}
          <Line 
            type="monotone" 
            dataKey={dataKey} 
            stroke={color} 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div className="flex justify-between items-center mt-4 text-xs text-gray-500">
        <span>Source: Organization for Economic Co-operation and Development via FRED</span>
        <button className="text-blue-600 hover:text-blue-700 font-medium">
          Full series (5Y)
        </button>
      </div>
    </div>
  );
}