// src/api/attorneys.ts
import { useQuery } from "@tanstack/react-query";
import { api } from "./client";
import type { Attorney } from "../types/attorney";

export async function fetchAttorneys(jurisdiction: string) {
  const res = await api.get<Attorney[]>(`/attorneys/${jurisdiction}`);
  return res.data;
}

export function useAttorneys(jurisdiction: string) {
  return useQuery({
    queryKey: ["attorneys", jurisdiction],
    queryFn: () => fetchAttorneys(jurisdiction),
    enabled: jurisdiction.length === 2, // only fetch when valid code
  });
}
