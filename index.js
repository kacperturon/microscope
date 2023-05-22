const server = "http://127.0.0.1:5000";
const imgContainer = document.getElementById("picImg");
const takePicBtnContainer = document.getElementById("takePicBtn");
const picIdInput = document.getElementById("2020640437");
const form = document.getElementById("bootstrapForm"); 

console.log(imgContainer);
console.log(takePicBtnContainer);

const serverOk = async () => {
  try{
    const resp = await fetch(`${server}/ping`, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
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
  console.log(id, url);
  imgContainer.setAttribute('src', url);
  imgContainer.classList = 'pb-2';
  picIdInput.value = id;
}

async function movePicture(picId){
  const resp = await fetch(`${server}/pic/${picId}/move`);
  console.log('moved pic' , resp.status);

}

(async()=>{
  
  let serverChecker = setInterval(async()=>{
    if(await serverOk()){
      console.log('server ok');
      clearInterval(serverChecker);
      takePicBtnContainer.disabled = false;

    }
  }, 1000);
})();