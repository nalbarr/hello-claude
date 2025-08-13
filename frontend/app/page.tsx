"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import ChartCard from "@/components/ChartCard";
import { fetchMultipleSeries, FRED_SERIES, FredSeriesData, calculateYoYChange } from "@/lib/fredApi";

export default function Home() {
  const [data, setData] = useState<{ [key: string]: FredSeriesData }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Calculate date range (last 5 years for CPI, last 2 years for others)
        const endDate = new Date();
        const startDateCPI = new Date();
        startDateCPI.setFullYear(endDate.getFullYear() - 5);
        const startDateOthers = new Date();
        startDateOthers.setFullYear(endDate.getFullYear() - 2);
        
        // Fetch all series data
        const seriesData = await fetchMultipleSeries([
          FRED_SERIES.CPI,
          FRED_SERIES.UNEMPLOYMENT,
          FRED_SERIES.BOND_10Y,
          FRED_SERIES.TREASURY_3M,
        ]);
        
        setData(seriesData);
      } catch (err) {
        console.error("Error loading FRED data:", err);
        setError("Failed to load economic data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Calculate CPI year-over-year change for display
  const cpiYoYData = data[FRED_SERIES.CPI] 
    ? calculateYoYChange(data[FRED_SERIES.CPI].data)
    : [];

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Economic Indicators Dashboard</h1>
            <p className="text-gray-600 mt-2">Real-time economic data from the Federal Reserve Economic Data (FRED) system</p>
          </div>
          
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-gray-600">Loading economic data...</p>
              </div>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-700">{error}</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-6">
              <ChartCard
                title="CPI - last five years"
                subtitle={data[FRED_SERIES.CPI]?.title || "Consumer Price Index: All Items: Total for United States"}
                data={cpiYoYData.length > 0 ? cpiYoYData : data[FRED_SERIES.CPI]?.data || []}
                dataKey="value"
                color="#2563eb"
              />
              
              <ChartCard
                title="Infra-Annual Labor Statistics: Unemployment Rate Total"
                subtitle={data[FRED_SERIES.UNEMPLOYMENT]?.title}
                data={data[FRED_SERIES.UNEMPLOYMENT]?.data || []}
                dataKey="value"
                color="#2563eb"
              />
              
              <ChartCard
                title="Interest Rates: Long-Term Government Bond Yields: 10-Year"
                subtitle={data[FRED_SERIES.BOND_10Y]?.title || "10-Year Treasury Constant Maturity Rate"}
                data={data[FRED_SERIES.BOND_10Y]?.data || []}
                dataKey="value"
                color="#2563eb"
              />
              
              <ChartCard
                title="Interest Rates: 3-Month or 90-Day Rates and Yields"
                subtitle={data[FRED_SERIES.TREASURY_3M]?.title || "3-Month Treasury Constant Maturity Rate"}
                data={data[FRED_SERIES.TREASURY_3M]?.data || []}
                dataKey="value"
                color="#2563eb"
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}