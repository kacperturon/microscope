const server = "http://127.0.0.1:5000";
// let server = "http://192.168.1.171:5000";

const imgContainer = document.getElementById("picImg");
const takePicBtnContainer = document.getElementById("takePicBtn");
const picIdInput = document.getElementById("2020640437");
const form = document.getElementById("bootstrapForm"); 


const getConfigS3 = async() => {
  const resp = await fetch(
    `https://microscope-grain.s3.eu-central-1.amazonaws.com/config.json`);
  data = await resp.json();
  server = `http://${data['server_local_ip']}:5000`;

}
getConfigS3();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  var data = new FormData(e.target);
  try{
    const resp = await fetch(
      `${e.target.action}?${new URLSearchParams(data).toString()}`,
      {
          method: e.target.method,
          mode: 'no-cors',
          headers: {
              'Accept': 'application/json'
          }
      });
    console.log(resp);
    form.reset();
    // movePicture(picIdInput.value);
    alert('Pomyślnie wysłano');
  } catch (e) {
    console.log(e);
  }

});

const serverOk = async () => {
  try{
    const resp = await fetch(`${server}/ping`, {
      method: "GET", 
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    }
      );
    const ok = await resp.text();
    return ok === "pong";
  }catch(e){
    return false;
  }
}

async function takePicture(){
  const resp = await fetch(`${server}/pic`);
  const {id, url} = await resp.json();
  imgContainer.setAttribute('src', url);
  imgContainer.classList = 'pb-2';
  picIdInput.value = id;
}

async function movePicture(picId){
  const resp = await fetch(`${server}/pic/${picId}/move`);
}

// (async()=>{
//   let serverChecker = setInterval(async()=>{
//     if(await serverOk()){
//       console.log('server ok');
//       clearInterval(serverChecker);
//       takePicBtnContainer.disabled = false;
//     }
//   }, 1000);
// })();