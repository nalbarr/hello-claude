"use client";

import { useState } from "react";
import { 
  TrendingUp, 
  DollarSign, 
  Briefcase, 
  Percent, 
  BarChart3, 
  ArrowRightLeft,
  Home,
  ShoppingCart,
  ChevronRight
} from "lucide-react";

const menuItems = [
  { id: "key-indicators", label: "Key Indicators", icon: TrendingUp, active: true },
  { id: "inflation", label: "Inflation", icon: DollarSign },
  { id: "employment", label: "Employment", icon: Briefcase },
  { id: "interest-rates", label: "Interest Rates", icon: Percent },
  { id: "economic-growth", label: "Economic Growth", icon: BarChart3 },
  { id: "exchange-rates", label: "Exchange Rates", icon: ArrowRightLeft },
  { id: "housing", label: "Housing", icon: Home },
  { id: "consumer-spending", label: "Consumer Spending", icon: ShoppingCart },
];

export default function Sidebar() {
  const [activeItem, setActiveItem] = useState("key-indicators");

  return (
    <div className="w-[280px] bg-white border-r border-gray-200 h-screen flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900">FRED Indicators</h1>
        <p className="text-sm text-gray-500 mt-1">Economic Data Dashboard</p>
      </div>
      
      <nav className="flex-1 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeItem === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveItem(item.id)}
              className={`w-full flex items-center justify-between px-4 py-3 mb-1 rounded-lg transition-all ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </div>
              <ChevronRight size={16} className={isActive ? "opacity-100" : "opacity-0"} />
            </button>
          );
        })}
      </nav>
      
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Data provided by Federal Reserve Economic Data (FRED)
        </p>
      </div>
    </div>
  );
}