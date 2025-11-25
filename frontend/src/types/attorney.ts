// src/types/attorney.ts
export interface AttorneyDetail {
  id: number;
  attorney_id: number;
  detail_type: string;
  detail: string;
}

export interface Attorney {
  id: number;
  jurisdiction: string;
  source: string;
  name: string;
  bar?: number;
  phone?: string;
  address?: string;
  date_admitted?: string;
  law_school?: string;
  license_status?: string;
  rating?: string;
  details?: AttorneyDetail[];
}