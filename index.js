const server = "https://398f-165-120-47-15.ngrok-free.app";
// const server = "http://192.168.1.154:5000";

const imgContainer = document.getElementById("picImg");
const takePicBtnContainer = document.getElementById("takePicBtn");
const picIdInput = document.getElementById("2020640437");
const form = document.getElementById("bootstrapForm"); 
const szkodnikiCheckboxes = document.getElementById('szkodniki');
const chorobyCheckboxes = document.getElementById('choroby');


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
  let valid = true;
  if(picIdInput.value == "") {
    message += `Zrob zdjecie przed wyslaniem formy`;
    valid = false;
  }
  if(Array.from(szkodnikiCheckboxes.querySelectorAll("input[type=checkbox]")).some(
    checkbox => checkbox.checked
  )) {
    message += `Przynajmniej jedno pole musi byc zaznaczone w szkodnikach`
    valid = false;
  }
  if(Array.from(szkodnikiCheckboxes.querySelectorAll("input[type=checkbox]")).some(
    checkbox => checkbox.checked
  )) {
    message += `Przynajmniej jedno pole musi byc zaznaczone w szkodnikach`
    valid = false;
  }
  alert(message);
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

serverOk();