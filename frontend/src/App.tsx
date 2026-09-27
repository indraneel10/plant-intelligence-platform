import {useEffect,useMemo,useState} from "react";
import {api,MonitorResult,Plant} from "./api";

type Message={role:"user"|"assistant";text:string};

function App(){
  const [plants,setPlants]=useState<Plant[]>([]);
  const [selected,setSelected]=useState("");
  const [monitor,setMonitor]=useState<MonitorResult|null>(null);
  const [messages,setMessages]=useState<Message[]>([{role:"assistant",text:"I’m your Plant Intelligence Copilot. Ask me about plant health, sensors, irrigation, decisions, or the latest monitoring cycle."}]);
  const [input,setInput]=useState("");
  const [loading,setLoading]=useState(true);
  const [running,setRunning]=useState(false);
  const [error,setError]=useState("");
  useEffect(()=>{api.listPlants().then(items=>{setPlants(items);if(items[0])setSelected(items[0].plant_id)}).catch(()=>setError("Could not connect to the Plant Intelligence API.")).finally(()=>setLoading(false))},[]);
  const plant=useMemo(()=>plants.find(p=>p.plant_id===selected),[plants,selected]);

  async function runMonitor(){
    if(!selected)return;
    setRunning(true);setError("");
    try{
      const result=await api.monitor(selected);setMonitor(result);
      setMessages(m=>[...m,{role:"assistant",text:"Monitoring completed. Health "+Math.round(result.health_score*100)+"%. Decision: "+result.decision+". "+result.reason}]);
    }catch{setError("Monitoring cycle failed. Check the backend and hardware mode.")}finally{setRunning(false)}
  }

  async function send(){
    const text=input.trim();if(!text)return;
    setMessages(m=>[...m,{role:"user",text}]);setInput("");
    try{
      const result=await api.chat(text,selected||undefined);
      setMessages(m=>[...m,{role:"assistant",text:result.message}]);
    }catch{
      setMessages(m=>[...m,{role:"assistant",text:"The AI Copilot service is unavailable. Check the backend and API configuration."}]);
    }
  }

  return <div className="shell">
    <aside className="sidebar">
      <div className="brand"><div className="mark">P</div><div><b>Plant Intelligence</b><span>AI Garden Platform</span></div></div>
      <nav>{["Overview","AI Copilot","Plants","Sensors","Irrigation","History"].map((x,i)=><button className={"nav "+(i===0?"active":"")} key={x}>{x}</button>)}</nav>
      <div className="online"><i/> Platform online</div>
    </aside>
    <main className="main">
      <header className="topbar">
        <div><p className="eyebrow">PLANT INTELLIGENCE PLATFORM</p><h1>Plant command center</h1></div>
        <div className="selector"><label>Plant</label><select value={selected} onChange={e=>setSelected(e.target.value)} disabled={loading}>{plants.length===0&&<option>No plants</option>}{plants.map(p=><option key={p.plant_id} value={p.plant_id}>{p.name} · {p.plant_id}</option>)}</select></div>
      </header>
      {error&&<div className="error">{error}</div>}
      <section className="hero">
        <div className="hero-card"><div><p className="eyebrow">CURRENT PLANT</p><h2>{plant?.name??"Select a plant"}</h2><p className="muted">{plant?.species??"Species not configured"} · {plant?.zone_id??"Zone not configured"}</p></div><button className="primary" disabled={!selected||running} onClick={runMonitor}>{running?"Running...":"Run monitoring cycle"}</button></div>
        <Metric title="Health" value={monitor?Math.round(monitor.health_score*100)+"%":"—"}/>
        <Metric title="Soil moisture" value={monitor?.soil_moisture!=null?monitor.soil_moisture+"%":"—"}/>
        <Metric title="Decision" value={monitor?.decision??"Waiting"}/>
      </section>
      <section className="grid">
        <div className="panel">
          <div className="panel-head"><div><p className="eyebrow">AI COPILOT</p><h2>Ask your plant</h2></div><span className="badge">Context aware</span></div>
          <div className="messages">{messages.map((m,i)=><div key={i} className={"message "+m.role}><small>{m.role==="assistant"?"COPILOT":"YOU"}</small><p>{m.text}</p></div>)}</div>
          <div className="composer"><input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()} placeholder="Ask: Why is my plant stressed?"/><button className="primary" onClick={send}>Send</button></div>
        </div>
        <div className="panel"><div className="panel-head"><div><p className="eyebrow">LATEST DECISION</p><h2>System reasoning</h2></div></div>{monitor?<div className="decision"><strong>{monitor.decision}</strong><p>{monitor.reason}</p><div className="chips"><span>Confidence {Math.round(monitor.confidence*100)}%</span><span>Zone {monitor.zone_id??"—"}</span><span>{monitor.duration_seconds}s irrigation</span></div></div>:<div className="empty">Run a monitoring cycle to see the platform’s current decision and evidence.</div>}</div>
      </section>
    </main>
  </div>
}

function Metric({title,value}:{title:string;value:string}){return <div className="metric"><span>{title}</span><strong>{value}</strong></div>}

function copilot(input:string,plant:Plant|undefined,result:MonitorResult){
  const q=input.toLowerCase();const name=plant?.name??"the selected plant";
  if(q.includes("water")||q.includes("irrig"))return name+" has soil moisture at "+(result.soil_moisture??"unknown")+". Latest decision: "+result.decision+". "+result.reason;
  if(q.includes("health")||q.includes("stress"))return name+"'s latest health score is "+Math.round(result.health_score*100)+"%. The monitoring engine reported: "+result.reason;
  return "The latest cycle for "+name+" reports "+result.decision+" with "+Math.round(result.confidence*100)+"% confidence. "+result.reason;
}

export default App;