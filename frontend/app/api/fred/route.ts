import { NextResponse } from 'next/server';
import axios from 'axios';

const FRED_API_BASE_URL = 'https://api.stlouisfed.org/fred';
const FRED_API_KEY = process.env.NEXT_PUBLIC_FRED_API_KEY || 'demo_key';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const seriesId = searchParams.get('series_id');
  const startDate = searchParams.get('start_date');
  const endDate = searchParams.get('end_date');

  if (!seriesId) {
    return NextResponse.json({ error: 'Series ID is required' }, { status: 400 });
  }

  try {
    // If no API key is set, return mock data
    if (FRED_API_KEY === 'demo_key' || FRED_API_KEY === 'your_api_key_here') {
      const mockData = getMockDataForSeries(seriesId);
      return NextResponse.json(mockData);
    }

    // Fetch from actual FRED API
    const params: any = {
      series_id: seriesId,
      api_key: FRED_API_KEY,
      file_type: 'json',
    };

    if (startDate) params.observation_start = startDate;
    if (endDate) params.observation_end = endDate;

    const [observationsResponse, seriesInfoResponse] = await Promise.all([
      axios.get(`${FRED_API_BASE_URL}/series/observations`, { params }),
      axios.get(`${FRED_API_BASE_URL}/series`, {
        params: {
          series_id: seriesId,
          api_key: FRED_API_KEY,
          file_type: 'json',
        },
      }),
    ]);

    const seriesInfo = seriesInfoResponse.data.seriess[0];
    const observations = observationsResponse.data.observations;

    return NextResponse.json({
      title: seriesInfo.title,
      units: seriesInfo.units,
      frequency: seriesInfo.frequency,
      data: observations.map((obs: any) => ({
        date: obs.date,
        value: obs.value === '.' ? null : parseFloat(obs.value),
      })).filter((d: any) => d.value !== null),
    });
  } catch (error) {
    console.error('Error fetching FRED data:', error);
    // Return mock data as fallback
    const mockData = getMockDataForSeries(seriesId);
    return NextResponse.json(mockData);
  }
}

function getMockDataForSeries(seriesId: string) {
  const now = new Date();
  const data = [];
  
  // Generate realistic mock data based on series type
  switch (seriesId) {
    case 'CPIAUCSL': // CPI
      for (let i = 60; i >= 0; i--) {
        const date = new Date(now);
        date.setMonth(date.getMonth() - i);
        const baseValue = 290 + i * 0.3;
        const noise = Math.sin(i / 6) * 5 + Math.random() * 2;
        data.push({
          date: date.toISOString().split('T')[0],
          value: parseFloat((baseValue + noise).toFixed(2)),
        });
      }
      return {
        title: 'Consumer Price Index for All Urban Consumers: All Items in U.S. City Average',
        units: 'Index 1982-1984=100',
        frequency: 'Monthly',
        data,
      };

    case 'UNRATE': // Unemployment
      for (let i = 24; i >= 0; i--) {
        const date = new Date(now);
        date.setMonth(date.getMonth() - i);
        const baseValue = 3.5 + Math.sin(i / 12 * Math.PI) * 0.7;
        const noise = Math.random() * 0.2 - 0.1;
        data.push({
          date: date.toISOString().split('T')[0],
          value: parseFloat((baseValue + noise).toFixed(2)),
        });
      }
      return {
        title: 'Unemployment Rate',
        units: 'Percent',
        frequency: 'Monthly',
        data,
      };

    case 'DGS10': // 10-Year Treasury
      for (let i = 24; i >= 0; i--) {
        const date = new Date(now);
        date.setMonth(date.getMonth() - i);
        const baseValue = 4.0 + Math.sin(i / 8 * Math.PI) * 0.8;
        const noise = Math.random() * 0.3 - 0.15;
        data.push({
          date: date.toISOString().split('T')[0],
          value: parseFloat((baseValue + noise).toFixed(3)),
        });
      }
      return {
        title: 'Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity',
        units: 'Percent',
        frequency: 'Daily',
        data,
      };

    case 'DGS3MO': // 3-Month Treasury
      for (let i = 24; i >= 0; i--) {
        const date = new Date(now);
        date.setMonth(date.getMonth() - i);
        const baseValue = 5.25 - i * 0.02;
        const noise = Math.random() * 0.2 - 0.1;
        data.push({
          date: date.toISOString().split('T')[0],
          value: parseFloat((baseValue + noise).toFixed(3)),
        });
      }
      return {
        title: 'Market Yield on U.S. Treasury Securities at 3-Month Constant Maturity',
        units: 'Percent',
        frequency: 'Daily',
        data,
      };

    default:
      return {
        title: 'Unknown Series',
        units: 'Units',
        frequency: 'Unknown',
        data: [],
      };
  }
}