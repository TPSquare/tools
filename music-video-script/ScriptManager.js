/**
 * @typedef {Object} Scene
 * @property {string} [description]
 * @property {[HTMLVideoElement, string]} [sampleVideo]
 * @property {[HTMLAudioElement, string]} [audio]
 * @property {[string]} [actors]
 */

let onEsc = () => {};
window.onkeydown = ({ key }) => {
  if (key === "Escape") onEsc();
};

export default class ScriptManager {
  #scenesTable = document.body.querySelector("#scenes");
  #sampleVideosBlock = document.getElementById("sample-videos-block");
  #loadingLog = document.getElementById("loading-log");
  #actorsStatistics = document.getElementById("actors-statistics");
  #actorSearchSelect = document.body.querySelector("#filter .actor-search");
  #locationSearchSelect = document.body.querySelector("#filter .location-search");

  #actorsStatisticsData = {};
  #locationObjList = {};
  #actorsStatisticsAll = 0;
  #filter = { currentActor: "Tất cả", currentLocation: "Tất cả" };

  sampleVideos = {};
  audios = {};

  /**
   *
   * @param {HTMLElement} container
   * @param {string[]} audioNames
   * @param {string[]} sampleVideoNames
   */
  constructor(audioNames = [], sampleVideoNames = []) {
    sampleVideoNames.forEach((name) => (this.sampleVideos[name] = this.#createSampleVideo(name)));
    audioNames.forEach((name) => (this.audios[name] = this.#createAudio(name)));
  }

  /**
   *
   * @param {Scene[]} scenes
   */
  scenes(scenes) {
    this.#scenesTable.appendChild(this.#getScenesTableHeader());
    scenes.forEach((scene, index) => {
      const order = index + 1;

      const musicButton = (() => {
        if (scene.audio) return this.#createAudioButton(scene.audio);
        return null;
      })();

      const description = (() => {
        if (scene.sampleVideo) return this.#createOpenSampleVideoButton(scene.sampleVideo);
        return scene.description;
      })();

      const actors = scene.actors
        .map((actor) => {
          if (actor.includes("người")) return `<span class="red">${actor}</span>`;
          if (actor.toLowerCase() === "tất cả") ++this.#actorsStatisticsAll;
          else if (actor !== "") this.#actorsStatisticsData[actor] = this.#actorsStatisticsData[actor] + 1 || 1;
          return actor;
        })
        .join(", ");

      const preparation = scene.preparation || "";

      const location = scene.location;
      this.#locationObjList[location] = true;

      const cells = [order, musicButton, description, actors, preparation, location];
      this.#scenesTable.appendChild(this.#createTableRow(cells));
    });
  }

  done() {
    this.#sortActorsStatisticsData();
    this.#addActorsStatistics();
    this.#createActorSearchSelect();
    this.#createLocationSearchSelect();
  }

  #sortActorsStatisticsData() {
    const data = structuredClone(this.#actorsStatisticsData);
    const list = Object.keys(data).sort((actor1, actor2) => data[actor2] - data[actor1]);
    this.#actorsStatisticsData = {};
    for (const name of list) this.#actorsStatisticsData[name] = data[name];
  }

  #addActorsStatistics() {
    const maper = (name, i) => `<tr><td>${i + 1}</td><td>${name}</td><td>${this.#actorsStatisticsData[name]}</td></tr>`;
    const rows = Object.keys(this.#actorsStatisticsData).map(maper);
    const table = `<table><tr><th>STT</th><th>Tên</th><th>Số vai đã có</th></tr>${rows.join("")}</table>`;
    this.#actorsStatistics.innerHTML += table;
    this.#actorsStatistics.innerHTML += `<div>Có ${this.#actorsStatisticsAll} cảnh cần tất cả mọi người!</div>`;
  }

  #createActorSearchSelect() {
    const actors = ["Tất cả"].concat(Object.keys(this.#actorsStatisticsData));
    const options = actors.map((actor) => `<option value="${actor}">${actor}</option>`).join("");
    this.#actorSearchSelect.innerHTML = options;

    this.#actorSearchSelect.onchange = () => this.#updateFilter({ actor: this.#actorSearchSelect.value });
  }

  #createLocationSearchSelect() {
    const locations = ["Tất cả"].concat(Object.keys(this.#locationObjList));
    const options = locations.map((location) => `<option value="${location}">${location}</option>`).join("");
    this.#locationSearchSelect.innerHTML = options;

    this.#locationSearchSelect.onchange = () => this.#updateFilter({ location: this.#locationSearchSelect.value });
  }

  #updateFilter({ actor, location }) {
    if (actor !== undefined) this.#filter.currentActor = actor;
    if (location !== undefined) this.#filter.currentLocation = location;
    location = this.#filter.currentLocation;

    this.#scenesTable.querySelectorAll(".hidden").forEach((e) => e.classList.remove("hidden"));
    if (this.#filter.currentActor === "Tất cả" && this.#filter.currentLocation === "Tất cả") return;

    const hiddenChildList = Array.from(this.#scenesTable.childNodes).filter((elm, index) => {
      if (index === 0) return false;

      const condition = { actor: true, location: true };
      if (this.#filter.currentActor === "Tất cả") condition.actor = false;
      else {
        const actors = elm.querySelector("td:nth-child(4)").textContent;
        if (actors.toLowerCase().includes("tất cả") || actors.includes(this.#filter.currentActor)) condition.actor = false;
      }
      if (this.#filter.currentLocation === "Tất cả") condition.location = false;
      else if (elm.querySelector("td:nth-child(6)").textContent === this.#filter.currentLocation) condition.location = false;
      return !(!condition.actor && !condition.location);
    });

    hiddenChildList.forEach((elm) => elm.classList.add("hidden"));
  }

  #createSampleVideo(name) {
    const video = document.createElement("video");
    video.src = `./assets/${name}.mp4`;
    video.className = name;
    video.playsInline = true;
    video.controls = true;

    const loadElement = document.createElement("div");
    loadElement.textContent = `Đang tải ${name}.mp4`;
    this.#loadingLog.appendChild(loadElement);
    video.onloadeddata = () => this.#loadingLog.removeChild(loadElement);

    video.load();

    this.#sampleVideosBlock.appendChild(video);
    return video;
  }

  #createAudio(name) {
    const audio = new Audio(`./assets/${name}.mp3`);

    const loadElement = document.createElement("div");
    loadElement.textContent = `Đang tải ${name}.mp3`;
    this.#loadingLog.appendChild(loadElement);
    audio.onloadeddata = () => this.#loadingLog.removeChild(loadElement);
    audio.load();

    return audio;
  }

  #getScenesTableHeader() {
    const cells = ["Cảnh", "Đoạn nhạc", "Mô tả", "Người diễn", "Chuẩn bị / Đạo cụ", "Địa điểm"];
    const tr = document.createElement("tr");
    tr.innerHTML = cells.map((c) => `<th>${c}</th>`).join("");
    return tr;
  }

  #createTableRow(cellNodes = []) {
    const tr = document.createElement("tr");
    cellNodes.forEach((cell) => {
      const td = document.createElement("td");
      if (cell instanceof Node) td.appendChild(cell);
      else td.innerHTML = cell;
      tr.appendChild(td);
    });
    return tr;
  }

  #sampleVideosWrapper = {
    element: document.getElementById("sample-videos-wrapper"),
    show: () => this.#sampleVideosWrapper.element.classList.add("show"),
    hide: () => this.#sampleVideosWrapper.element.classList.remove("show"),
  };

  #createOpenSampleVideoButton([video, time]) {
    const [startTime, endTime] = this.#splitTime(time);
    const button = document.createElement("button");
    button.className = "open-sample-video-button";
    button.textContent = "Bấm để xem video";
    button.onclick = () => {
      this.#sampleVideosWrapper.show();
      video.currentTime = startTime;
      video.ontimeupdate = () => {
        if (video.currentTime > endTime) {
          video.pause();
          setTimeout(this.#sampleVideosWrapper.hide, 200);
        }
      };
      video.play();
      onEsc = () => {
        video.pause();
        this.#sampleVideosWrapper.hide();
      };
    };
    return button;
  }

  #createAudioButton([audio, time]) {
    const [startTime, endTime] = this.#splitTime(time);
    const button = document.createElement("button");
    button.className = "audio-button";
    button.textContent = "Phát";
    button.onclick = () => {
      audio.currentTime = startTime;
      audio.ontimeupdate = () => {
        if (audio.currentTime > endTime) audio.pause();
      };
      audio.play();
    };
    return button;
  }

  #splitTime(time) {
    const timePart = time.replaceAll(" ", "").split("-");
    const startTime = this.#readableTimeToSeconds(timePart[0]);
    const endTime = this.#readableTimeToSeconds(timePart[1]);
    return [startTime, endTime];
  }

  #readableTimeToSeconds(time) {
    const parts = time.split(":");
    const minutes = parseInt(parts[0], 10);
    const seconds = parseFloat(parts[1], 10);
    return minutes * 60 + seconds;
  }
}
