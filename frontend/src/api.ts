export type Plant = {
  plant_id:string; name:string; species?:string|null; zone_id?:string|null; location_label?:string|null;
};
export type MonitorResult = {
  frame_id:string; decision:string; health_score:number; soil_moisture:number|null;
  reason:string; confidence:number; action:string|null; zone_id:string|null; duration_seconds:number;
};
const BASE=(import.meta.env.VITE_API_BASE_URL??"").replace(/\/$/,"");
async function request<T>(path:string, options?:RequestInit):Promise<T>{
  const response=await fetch(BASE+path,{headers:{"Content-Type":"application/json"},...options});
  if(!response.ok) throw new Error("API request failed: "+response.status);
  return response.json() as Promise<T>;
}
export const api={
  listPlants:()=>request<Plant[]>("/plants"),
  monitor:(id:string)=>request<MonitorResult>("/monitor/"+encodeURIComponent(id)+"/run",{method:"POST"}),
  observations:(id:string)=>request<unknown[]>("/plants/"+encodeURIComponent(id)+"/observations"),
  sensorHistory:(id:string)=>request<unknown[]>("/plants/"+encodeURIComponent(id)+"/sensor-history"),
  decisions:(id:string)=>request<unknown[]>("/plants/"+encodeURIComponent(id)+"/decisions"),
  irrigationHistory:(id:string)=>request<unknown[]>("/plants/"+encodeURIComponent(id)+"/irrigation-history"),
  chat:(message:string,plantId?:string)=>request<{message:string;mode:string;tools_used:string[]}>("/ai/chat",{
    method:"POST",
    body:JSON.stringify({message,plant_id:plantId??null})
  })
};