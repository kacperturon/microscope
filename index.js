const server = "https://c020-89-64-127-213.ngrok-free.app";
// const server = "http://192.168.1.154:5000";

const version = `0.01.00`;

const formURLProd = "https://docs.google.com/forms/d/e/1FAIpQLSf6OgAjepwCfIi9LPhtTNG9m4CtFEp_cUaB6Z8LdYBi_DktUA/formResponse";
const formURLDev = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfK8NX00r2Y89e2eWiJiwGpJrPwvQ4ZMTlZSZvFjwYuaX23uQ/formResponse";

const imgContainer = document.getElementById("picImg");
const takePicBtnContainer = document.getElementById("takePicBtn");
const picIdInput = document.getElementById("2020640437");
const form = document.getElementById("bootstrapForm"); 
const szkodnikiCheckboxes = document.getElementById('szkodniki');
const chorobyCheckboxes = document.getElementById('choroby');
const checkboxQuerySelector = "input[type=checkbox]";

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if(!validForm()) return;
  var data = new FormData(e.target);
  try{
    const resp = await fetch(
      `${e.target.action}?${new URLSearchParams(data).toString()}`,
      {
          method: e.target.method,
          mode: 'no-cors',
          headers: {
              'Accept': 'application/json',
          }
      });
    await movePicture(picIdInput.value);
    form.reset();
    imgContainer.setAttribute('src', '#');
    imgContainer.classList = 'hidden';
    alert('Pomyślnie wysłano');
  } catch (e) {
    console.log(e);
  }
});

const validForm = () => {
  let message = "";
  let msg1 =`Zrob zdjecie przed wyslaniem formy`;
  let msg2 = `Przynajmniej jedno pole musi byc zaznaczone w chorobach lub szkodnikach`;
  let valid = true;
  let checkboxes = Array.from(szkodnikiCheckboxes.querySelectorAll(checkboxQuerySelector)).concat(
    Array.from(chorobyCheckboxes.querySelectorAll(checkboxQuerySelector))
  );

  if(picIdInput.value == "" && !checkboxes.some(
    checkbox => checkbox.checked
  )) {
    message = `• ${msg1}\n• ${msg2}`;
    valid = false;
  }
  else if(picIdInput.value == "") {
    message = msg1;
    valid = false;
  } else if(!checkboxes.some(
    checkbox => checkbox.checked
  )) {
    message = msg2;
    valid = false;
  }
  if(!valid) alert(message);
  return valid;
}

const serverOk = async () => {
  try{
    const resp = await fetch(`${server}/ping`, {
      method: "GET", 
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      headers: {
        'ngrok-skip-browser-warning': 'noop',
      }
    }
      );
    const ok = await resp.text();
    return ok === "pong";
  }catch(e){
    return false;
  }
}

async function takePicture(){
  const resp = await fetch(`${server}/pic`, {
    headers: {
      'ngrok-skip-browser-warning': 'noop',
    }
  });
  const {id, url} = await resp.json();
  imgContainer.setAttribute('src', url);
  imgContainer.classList = 'pb-2';
  picIdInput.value = id;
}

async function movePicture(picId){
  const resp = await fetch(`${server}/pic/${picId}/move`, {
    headers: {
      'ngrok-skip-browser-warning': 'noop',
    }
  });
}

async function init() {
  const resp = await fetch(`${server}/env`, {
    headers: {
      'ngrok-skip-browser-warning': 'noop',
    }
  });
  const env = await resp.text();
  const resp2 = await fetch(`${server}/camconnected`, {
    headers: {
      'ngrok-skip-browser-warning': 'noop',
    }
  });
  const cameraWorking = await resp.text();
  const serverRunning = await serverOk(); 

  form.setAttribute('action', env === 'prod' ? formURLProd : formURLDev);

  console.info(`Server is running: ${serverRunning}`);
  console.info(`Camera is working: ${cameraWorking}`);
  console.info(`Environment: ${env}\nVersion: ${version}`);
}

init();