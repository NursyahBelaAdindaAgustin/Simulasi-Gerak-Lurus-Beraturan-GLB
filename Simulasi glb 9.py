import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.markdown("""
<h1 style="text-align:center;">Simulasi Gerak Lurus Beraturan (GLB) dengan Gedung</h1>
<p style="text-align:center; margin-top: -10px;">
Deskripsi: Simulasi ini menampilkan mobil bergerak lurus dengan kecepatan tetap di depan deretan gedung.<br>
Limit simulasi: 90 meter (mobil berhenti otomatis ketika mencapai batas).
</p>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Simulasi GLB</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: "Poppins", sans-serif; margin:0; padding:0; }
#simulasi { position: relative; width: 900px; height: 300px; margin: 30px auto; 
background: linear-gradient(to top, #a8d5e2 70%, #e0f7fa 30%); border: 2px solid #333; border-radius: 10px; overflow: hidden; }
.gedung { position: absolute; bottom: 80px; width: 50px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; }
.gedung.dekat { background: linear-gradient(to bottom, #cce5f6, #99c2e6); border: 1px solid #5c90c0; }
.gedung.sedang { background: linear-gradient(to bottom, #b0cce0, #84a9c6); border: 1px solid #5c80a0; }
.gedung.jauh { background: linear-gradient(to bottom, #9bb0c4, #6e8aa0); border: 1px solid #556a80; }
.jendela { width: 10px; height: 10px; background: linear-gradient(to bottom right, #ffffff, #8fc3f7); margin: 1px 0; border-radius: 1px; border: 1px solid #b0d3f0; }
#jalan { position: absolute; bottom: 0; width: 100%; height: 80px; background: #222; }
#garis { position: absolute; bottom: 35px; width: 100%; height: 8px; background: repeating-linear-gradient(to right, white 0, white 60px, transparent 60px, transparent 120px); opacity: 0.9; }
#mobil { position: absolute; bottom: 50px; left: 0; font-size: 50px; transform: scaleX(-1); }
#koordinat { position: absolute; bottom: 15px; left: 10px; background: rgba(255,255,255,0.85); padding: 5px 10px; border-radius: 8px; font-size: 14px; font-weight: 600; }
.grafik-row { display: flex; justify-content: center; gap: 20px; margin-top: 25px; flex-wrap: wrap; }
.grafik-box { width: 45%; min-width: 300px; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.15); }
canvas { width: 100% !important; height: 300px !important; }
button { margin: 5px; padding: 8px 16px; background: #0288d1; color: white; border-radius: 8px; border: none; cursor: pointer; }
button:hover { background: #01579b; }
</style>
</head>
<body>
<div style="text-align:center; margin-bottom:15px;">
  Posisi awal (m): <input id="posisiAwal" type="number" value="0">
  Kecepatan (m/s): <input id="kecepatan" type="number" step="0.5" value="3">
  <button onclick="mulai()">Mulai</button>
  <button onclick="berhenti()">Berhenti</button>
  <button onclick="resetSimulasi()">Reset</button>
</div>

<div id="simulasi">
  <div class="gedung dekat" style="left:0px; height:150px;"></div>
  <script>
    const simulasi=document.currentScript.parentElement;
    const totalGedung=28; // disesuaikan agar muat di 900px
    for(let i=0;i<totalGedung;i++){
      const g=simulasi.children[0].cloneNode(true);
      let tipe=(i%3===0)?'jauh':((i%3===1)?'sedang':'dekat');
      g.className='gedung '+tipe;
      let tinggi=100+Math.random()*100;
      g.style.height=tinggi+'px';
      g.style.left=(i*32)+"px";
      g.innerHTML='';
      const numJendela=Math.floor(tinggi/12);
      for(let j=0;j<numJendela;j++){
        const win=document.createElement('div');
        win.className='jendela';
        g.appendChild(win);
      }
      simulasi.appendChild(g);
    }
    simulasi.removeChild(simulasi.children[0]);
  </script>
  <div id="jalan"></div>
  <div id="garis"></div>
  <div id="mobil">🏎️</div>
  <div id="koordinat">(0 m, 0 s)</div>
</div>

<div class="grafik-row">
  <div class="grafik-box"><h3>Grafik Posisi - Waktu</h3><canvas id="grafikPosisi"></canvas></div>
  <div class="grafik-box"><h3>Grafik Kecepatan - Waktu</h3><canvas id="grafikKecepatan"></canvas></div>
</div>

<script>
let waktu=0,posisi=0,kecepatan=0,interval=null,jalan=false;
const mobil=document.getElementById("mobil");
const koordinat=document.getElementById("koordinat");

const chartPosisi=new Chart(document.getElementById("grafikPosisi"),{
    type:"line",
    data:{labels:[],datasets:[{label:"Posisi (m)",borderColor:"blue",data:[],fill:false}]},
    options:{scales:{x:{title:{display:true,text:"Waktu (s)"}},y:{title:{display:true,text:"Posisi (m)"}}}}
});
const chartKecepatan=new Chart(document.getElementById("grafikKecepatan"),{
    type:"line",
    data:{labels:[],datasets:[{label:"Kecepatan (m/s)",borderColor:"red",data:[],fill:false}]},
    options:{scales:{x:{title:{display:true,text:"Waktu (s)"}},y:{title:{display:true,text:"Kecepatan (m/s)"}}}}
});

function mulai(){
    if(jalan) return;
    posisi=parseFloat(document.getElementById("posisiAwal").value);
    kecepatan=parseFloat(document.getElementById("kecepatan").value);
    waktu=0;
    chartPosisi.data.labels=[];
    chartPosisi.data.datasets[0].data=[];
    chartPosisi.update();
    chartKecepatan.data.labels=[];
    chartKecepatan.data.datasets[0].data=[];
    chartKecepatan.update();
    jalan=true;
    interval=setInterval(updateSimulasi,100);
}

function updateSimulasi(){
    waktu+=0.1;
    posisi+=kecepatan*0.1;
    const xPixel=posisi*10;
    mobil.style.left=xPixel+"px";
    koordinat.innerHTML=`(${posisi.toFixed(2)} m, ${waktu.toFixed(1)} s)`;
    koordinat.style.left=(xPixel+10)+"px";
    chartPosisi.data.labels.push(waktu.toFixed(1));
    chartPosisi.data.datasets[0].data.push(posisi);
    chartPosisi.update();
    chartKecepatan.data.labels.push(waktu.toFixed(1));
    chartKecepatan.data.datasets[0].data.push(kecepatan);
    chartKecepatan.update();
    if(posisi>=90) berhenti();
}

function berhenti(){jalan=false; clearInterval(interval);}
function resetSimulasi(){berhenti(); waktu=posisi=0; mobil.style.left="0px"; koordinat.innerHTML="(0 m, 0 s)";}
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
