import * as THREE from "three";
import { FontLoader } from "three/examples/jsm/loaders/FontLoader.js";
import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry.js";
import getCurrentUserGameStatus from "../Controller/Game/GetCurrentUserGameStatus.js";
import createElement from "../Utils/createElement.js";

const WAIT_GAME = 1;
const START_GAME = 2;
const END_GAME = 3;

class ImpactEffect {
  constructor(scene) {
    this.scene = scene;
    this.impacts = [];
    this.settings = {
      rings: 5,
      particlesPerRing: 30,
      startRadius: 2,
      maxRadius: 5,
      expandSpeed: 0.5,
      duration: 100,
      colors: [0xfd0140, 0xff140, 0xfb9b2e, 0xf78180],
      particleSize: 0.5,
      fadeSpeed: 0.02,
      rotationSpeed: 1,
      verticalSpeed: 0.1,
      thickness: 0.5,
    };
  }

  createImpact(position) {
    const rings = [];
    for (let r = 0; r < this.settings.rings; r++) {
      const geometry = new THREE.BufferGeometry();
      const positions = [];
      const baseRadius = this.settings.startRadius + r * this.settings.thickness;
      const particleCount = this.settings.particlesPerRing * (r + 1);

      for (let i = 0; i < particleCount; i++) {
        const angle = (i / particleCount) * Math.PI * 2;
        const x = Math.cos(angle) * baseRadius;
        const z = Math.sin(angle) * baseRadius;
        positions.push(x + position.x, position.y, z + position.z);
      }

      geometry.setAttribute(
        "position",
        new THREE.Float32BufferAttribute(positions, 3)
      );

      const material = new THREE.PointsMaterial({
        size: this.settings.particleSize,
        color: this.settings.colors[r % this.settings.colors.length],
        transparent: true,
        opacity: 1,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });

      const ring = new THREE.Points(geometry, material);
      rings.push({
        object: ring,
        radius: baseRadius,
        particleCount: particleCount,
        rotationOffset: Math.random() * Math.PI * 2,
        verticalOffset: 0,
      });

      this.scene.add(ring);
    }

    const impact = {
      rings,
      position,
      startTime: Date.now(),
      life: 1.0,
    };

    this.impacts.push(impact);

    // 일정 시간 후 제거
    setTimeout(() => {
      impact.rings.forEach((ring) => {
        this.scene.remove(ring.object);
        ring.object.geometry.dispose();
        ring.object.material.dispose();
      });
      this.impacts = this.impacts.filter((imp) => imp !== impact);
    }, this.settings.duration);
  }

  update() {
    const currentTime = Date.now();

    for (const impact of this.impacts) {
      const elapsed = (currentTime - impact.startTime) / this.settings.duration;
      const expandFactor = Math.min(elapsed * this.settings.expandSpeed, 1);

      impact.rings.forEach((ring, ringIndex) => {
        const positions = ring.object.geometry.attributes.position.array;
        const baseRadius =
          ring.radius + (this.settings.maxRadius - ring.radius) * expandFactor;

        // 각 파티클 업데이트
        for (let i = 0; i < positions.length; i += 3) {
          const particleIndex = i / 3;
          const angle =
            (particleIndex / ring.particleCount) * Math.PI * 2 +
            (ring.rotationOffset + this.settings.rotationSpeed * elapsed);

          const radiusVariation =
            Math.sin(angle * (ringIndex + 1) + elapsed * 5) * 0.2;
          const currentRadius = baseRadius * (1 + radiusVariation);

          positions[i] = impact.position.x + Math.cos(angle) * currentRadius;
          positions[i + 1] = impact.position.y + ring.verticalOffset;
          positions[i + 2] =
            impact.position.z + Math.sin(angle) * currentRadius;
        }

        ring.verticalOffset += this.settings.verticalSpeed;
        ring.rotationOffset += this.settings.rotationSpeed * (ringIndex + 1);
        ring.object.geometry.attributes.position.needsUpdate = true;
        ring.object.material.opacity = Math.max(0, 1 - elapsed);
      });
    }
  }
}

class AudioManager {
  constructor(camera) {
    this.camera = camera;
    this.audioContext = null;
    this.listener = null;
    this.sounds = new Map();
    this.audioLoader = null;
    this.initialized = false;
    this.initializationPromise = null;
  }

  async init() {
    if (this.initializationPromise) {
      return this.initializationPromise;
    }

    this.initializationPromise = new Promise((resolve) => {
      const handleInteraction = async () => {
        if (this.initialized) return;
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.audioContext = new AudioContext();

        this.listener = new THREE.AudioListener();
        this.audioLoader = new THREE.AudioLoader();
        this.camera.add(this.listener);

        if (this.audioContext.state === "suspended") {
          await this.audioContext.resume();
        }
        this.initialized = true;

        // 예시로 4개 사운드 로드
        await this.loadSound("ball",
          "https://raw.githubusercontent.com/alsksssass/ft_pingpong/master/public/localdata/sound/ball.mp3",
          { loop: false, volume: 0.9 }
        );
        await this.loadSound("bgm",
          "https://raw.githubusercontent.com/alsksssass/ft_pingpong/master/public/localdata/sound/bgm.mp3",
          { loop: true, volume: 0.9 }
        );
        await this.loadSound("power_ball",
          "https://raw.githubusercontent.com/alsksssass/ft_pingpong/master/public/localdata/sound/power_ball.mp3",
          { loop: false, volume: 0.9 }
        );
        await this.loadSound("nomal_ball",
          "https://raw.githubusercontent.com/alsksssass/ft_pingpong/master/public/localdata/sound/nomal_ball.mp3",
          { loop: false, volume: 0.9 }
        );

        this.play("bgm");

        // 등록했던 이벤트 제거
        ["click", "touchstart", "keydown"].forEach((event) => {
          document.removeEventListener(event, handleInteraction);
        });

        resolve();
      };

      ["click", "touchstart", "keydown"].forEach((event) => {
        document.addEventListener(event, handleInteraction);
      });
    });

    return this.initializationPromise;
  }

  async loadSound(name, path, options = {}) {
    if (!this.initialized) {
      throw new Error("AudioManager not initialized.");
    }
    return new Promise((resolve, reject) => {
      this.audioLoader.load(
        path,
        (buffer) => {
          const sound = new THREE.Audio(this.listener);
          sound.setBuffer(buffer);
          sound.setVolume(options.volume ?? 0.5);
          sound.setLoop(options.loop ?? false);
          sound.autoplay = name === "bgm";
          this.sounds.set(name, { sound, options: { ...options } });
          resolve(sound);
        },
        undefined,
        reject
      );
    });
  }

  play(name) {
    const soundData = this.sounds.get(name);
    if (!soundData) {
      console.warn(`Sound "${name}" not found`);
      return;
    }
    const { sound } = soundData;
    if (!sound.isPlaying) {
      sound.play();
    }
  }

  stop(name) {
    const soundData = this.sounds.get(name);
    console.log("stop sound 1");
    if (!soundData) {
      console.warn(`Sound "${name}" not found`);
      return;
    }
    console.log("stop sound 2");
    const { sound } = soundData;
    if (sound.isPlaying) {
    console.log("stop sound 3");
      sound.stop();
      sound.disconnect();
    }
  }

  setVolume(name, volume) {
    const soundData = this.sounds.get(name);
    if (!soundData) {
      console.warn(`Sound "${name}" not found`);
      return;
    }
    soundData.sound.setVolume(Math.max(0, Math.min(1, volume)));
  }

  cleanup() {
    this.sounds.forEach(({ sound }, soundKey) => {
      console.log("sound delete", soundKey, sound);
      if (sound.isPlaying) {
        sound.stop(soundKey);
      }
      sound.disconnect();
      sound.buffer = null;
    });
    this.sounds.clear();
  
    if (this.camera && this.listener) {
      this.camera.remove(this.listener);
    }
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }
    this.initialized = false;
  }
  
}

export default class PingPongClient {
  constructor(socket, gameId) {
    this.gameId = gameId;
    this.socket = socket;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );

    // 오디오 매니저
    this.audio = new AudioManager(this.camera);
    this.audio.init();

    // THREE 렌더러
    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize(window.innerWidth, window.innerHeight);

    // 게임 기본 속성
    this.gameWidth = 100;
    this.gameLenth = 250;
    this.initColor = [0xffffff, 0xff0000, 0x000000, 0x0000cc];
    this.gameStart = WAIT_GAME;
    this.secondPlayer = false;
    this.balls = [];
    this.textdata = null;
    this.effect = new ImpactEffect(this.scene);

    // 카메라 관련
    this.cameraRadius = 200;
    this.cameraTheta = 1.56;
    this.cameraPhi = 1.03;
    this.cameraTarget = new THREE.Vector3(0, 0, 0);

    // 마우스 드래그 관련
    this.isDragging = false;
    this.previousMousePosition = { x: 0, y: 0 };

    // **bind 함수**를 클래스 필드에 저장
    this.onKeyDownBound = this.onKeyDown.bind(this);
    this.onKeyUpBound = this.onKeyUp.bind(this);
    this.onMouseDownBound = this.onMouseDown.bind(this);
    this.onMouseMoveBound = this.onMouseMove.bind(this);
    this.onMouseUpBound = this.onMouseUp.bind(this);
    this.onWindowResizeBound = this.onWindowResize.bind(this);
    this.animate = this.animate.bind(this);

    this.updateCameraPosition();
    this.makeWindow();
    this.setupLights();
    this.setupEventListeners();

    // 오브젝트들
    this.playerOne = this.makeGameBar(0, 6, 100, 1);
    this.playerTwo = this.makeGameBar(0, 6, -100, 0);
    this.ball = this.createBall();
    this.makeTable();
    this.makeLine();
    this.makeGuideLines();

    // 애니메이션 시작
    this.animate();

    // 소켓 리스너 등록
    this.setupSocketListeners();
  }

  // 페이지 떠날 때 정리할 메서드
  dispose() {
    // 1) 오디오 정리
    this.audio.cleanup();

    // 2) 이벤트 리스너 해제
    window.removeEventListener("keydown", this.onKeyDownBound, false);
    window.removeEventListener("keyup", this.onKeyUpBound, false);
    this.renderer.domElement.removeEventListener(
      "mousedown",
      this.onMouseDownBound,
      false
    );
    this.renderer.domElement.removeEventListener(
      "mousemove",
      this.onMouseMoveBound,
      false
    );
    this.renderer.domElement.removeEventListener(
      "mouseup",
      this.onMouseUpBound,
      false
    );
    window.removeEventListener("resize", this.onWindowResizeBound, false);
    window.removeEventListener("load", this.onWindowResizeBound, false);

    // 3) Three.js renderer dispose
    this.renderer.dispose();

    // (추가) 필요하다면 scene 내 geometry/material dispose (체크 후 필요 시)
    // this.scene.traverse((obj) => {
    //   if (obj.isMesh) {
    //     obj.geometry.dispose();
    //     obj.material.dispose();
    //   }
    // });

    console.log("PingPongClient dispose() done.");
  }

  makeWindow() {
    return createElement("div", { class: "gameWindow" }, this.renderer.domElement);
  }

  makeFont(msg) {
    const loader = new FontLoader();
    loader.load(
      "https://threejs.org/examples/fonts/helvetiker_regular.typeface.json",
      (font) => {
        const textGeo = new TextGeometry(msg, {
          font,
          size: 10,
          height: 1,
          curveSegments: 1,
          bevelEnabled: true,
          bevelThickness: 1,
          bevelSize: 0.1,
          bevelOffset: 0.1,
          bevelSegments: 1,
        });
        textGeo.computeBoundingBox();
        textGeo.center();
        const material = new THREE.MeshPhongMaterial({ color: 0xffffff });
        const textMesh = new THREE.Mesh(textGeo, material);
        textMesh.position.set(0, 50, 0);

        if (this.textdata) {
          this.scene.remove(this.textdata);
          this.textdata.geometry.dispose();
          this.textdata.material.dispose();
          this.textdata = null;
        }
        this.scene.add(textMesh);
        this.textdata = textMesh;
      }
    );
  }

  setupLights() {
    const ambientLight = new THREE.AmbientLight(0xffffff, 1);
    this.scene.add(ambientLight);
  }

  setupEventListeners() {
    window.addEventListener("keydown", this.onKeyDownBound, false);
    window.addEventListener("keyup", this.onKeyUpBound, false);

    this.renderer.domElement.addEventListener(
      "mousedown",
      this.onMouseDownBound,
      false
    );
    this.renderer.domElement.addEventListener(
      "mousemove",
      this.onMouseMoveBound,
      false
    );
    this.renderer.domElement.addEventListener("mouseup", this.onMouseUpBound, false);

    window.addEventListener("resize", this.onWindowResizeBound, false);
    window.addEventListener("load", this.onWindowResizeBound, false);
  }

  onKeyDown(event) {
    let key = event.key.toUpperCase();
    key = key === "ARROWRIGHT" ? "D" : key === "ARROWLEFT" ? "A" : key;

    if (!this.secondPlayer && (key === "A" || key === "D")) {
      this.socket.emit("keypress", { key, pressed: true, who: this.secondPlayer });
    } else if (this.secondPlayer && (key === "A" || key === "D")) {
      this.socket.emit("keypress", {
        key: key === "A" ? "D" : "A",
        pressed: true,
        who: this.secondPlayer,
      });
    } else if (key === " ") {
      this.socket.emit("keypress", {
        key: " ",
        pressed: true,
        who: this.secondPlayer,
      });
    } else if (key === "M") {
      const bgmData = this.audio.sounds.get("bgm");
      if (bgmData?.sound) {
        bgmData.sound.isPlaying ? this.audio.stop("bgm") : this.audio.play("bgm");
      }
    } else if (key === "C") {
      const player = !this.secondPlayer ? this.playerOne : this.playerTwo;
      const nowIndexColor = this.initColor.indexOf(player.material.color.getHex());
      const nextColor =
        nowIndexColor >= this.initColor.length - 1 ? 0 : nowIndexColor + 1;
      player.material.color.set(this.initColor[nextColor]);
    }
  }

  onKeyUp(event) {
    let key = event.key.toUpperCase();
    key = key === "ARROWRIGHT" ? "D" : key === "ARROWLEFT" ? "A" : key;

    if (!this.secondPlayer && (key === "A" || key === "D")) {
      this.socket.emit("keypress", { key, pressed: false });
    } else if (this.secondPlayer && (key === "A" || key === "D")) {
      this.socket.emit("keypress", {
        key: key === "A" ? "D" : "A",
        pressed: false,
      });
    }
  }

  onMouseDown(event) {
    this.isDragging = true;
    this.previousMousePosition.x = event.clientX;
    this.previousMousePosition.y = event.clientY;
  }

  onMouseMove(event) {
    if (!this.isDragging) return;
    const deltaMove = {
      x: event.clientX - this.previousMousePosition.x,
      y: event.clientY - this.previousMousePosition.y,
    };
    this.previousMousePosition.x = event.clientX;
    this.previousMousePosition.y = event.clientY;
    this.rotateCamera(deltaMove);
  }

  onMouseUp(event) {
    this.isDragging = false;
  }

  rotateCamera(deltaMove) {
    this.cameraTheta -= deltaMove.x * 0.01;
    this.cameraPhi -= deltaMove.y * 0.01;
    this.cameraPhi = Math.max(0.1, Math.min(Math.PI - 0.1, this.cameraPhi));
    this.updateCameraPosition();
  }

  updateCameraPosition() {
    this.camera.position.x =
      this.cameraRadius * Math.sin(this.cameraPhi) * Math.cos(this.cameraTheta);
    this.camera.position.y = this.cameraRadius * Math.cos(this.cameraPhi);
    this.camera.position.z =
      this.cameraRadius * Math.sin(this.cameraPhi) * Math.sin(this.cameraTheta);
    this.camera.lookAt(this.cameraTarget);
  }

  onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  createBall() {
    const ballGeometry = new THREE.SphereGeometry(2, 32, 32);
    const ballMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
    const ballMesh = new THREE.Mesh(ballGeometry, ballMaterial);
    this.scene.add(ballMesh);
    return ballMesh;
  }

  createBalls(count) {
    // 기존 공 제거
    this.balls.forEach((ball) => {
      this.scene.remove(ball);
      ball.geometry.dispose();
      ball.material.dispose();
    });
    this.balls = [];
    // 새 공 생성
    for (let i = 0; i < count; i++) {
      this.balls.push(this.createBall());
    }
  }

  updateGameState(gameState) {
    this.playerOne.position.set(
      gameState.playerOne.x,
      gameState.playerOne.y,
      gameState.playerOne.z
    );
    this.playerTwo.position.set(
      gameState.playerTwo.x,
      gameState.playerTwo.y,
      gameState.playerTwo.z
    );
    if (this.balls.length !== gameState.balls.length) {
      this.createBalls(gameState.balls.length);
    }
    gameState.balls.forEach((ballData, index) => {
      this.balls[index].position.set(
        ballData.position.x,
        ballData.position.y,
        ballData.position.z
      );
      this.balls[index].material.color.setHex(
        this.initColor[gameState.balls[index].powerCounter]
      );
    });
  }

  makeGameBar(x, y, z, check) {
    const paddleGeometry = new THREE.BoxGeometry(20, 5, 5);
    const paddleMaterial = new THREE.MeshPhongMaterial({
      color: this.initColor[check],
    });
    const paddleMesh = new THREE.Mesh(paddleGeometry, paddleMaterial);
    paddleMesh.position.set(x, y, z);
    this.scene.add(paddleMesh);
    return paddleMesh;
  }

  makeTable() {
    const tableGeometry = new THREE.BoxGeometry(
      this.gameWidth,
      5,
      this.gameLenth
    );
    const tableMaterial = new THREE.MeshPhongMaterial({ color: 0x1a5c1a });
    const tableMesh = new THREE.Mesh(tableGeometry, tableMaterial);
    this.scene.add(tableMesh);
  }

  makeLine() {
    const lineGeometry = new THREE.BoxGeometry(this.gameWidth, 6, 1);
    const lineMaterial = new THREE.MeshPhongMaterial({ color: 0x0000ff });
    this.scene.add(new THREE.Mesh(lineGeometry, lineMaterial));
  }

  makeGuideLines() {
    const guideGeometry = new THREE.BoxGeometry(1, 10, this.gameLenth);
    const guideMaterial = new THREE.MeshPhongMaterial({ color: 0x0000ff });
    this.leftGuide = new THREE.Mesh(guideGeometry, guideMaterial);
    this.leftGuide.position.set(-this.gameWidth / 2, 5, 0);
    this.scene.add(this.leftGuide);

    this.rightGuide = new THREE.Mesh(guideGeometry, guideMaterial);
    this.rightGuide.position.set(this.gameWidth / 2, 5, 0);
    this.scene.add(this.rightGuide);
  }

  setupSocketListeners() {
    this.socket.on("connect", () => {
      console.log("Socket connected");
    });
    this.socket.on("data", async (gameState) => {
      if (gameState.type === "gameState") {
        this.gameStart = START_GAME;
        this.updateGameState(gameState);
      } else if (gameState.type === "score") {
        this.makeFont(
          !this.secondPlayer
            ? `${gameState.oneName} ${gameState.score.playerOne} : ${gameState.score.playerTwo} ${gameState.twoName}`
            : `${gameState.twoName} ${gameState.score.playerTwo} : ${gameState.score.playerOne} ${gameState.oneName}`
        );
      } else if (gameState.type === "gameStart") {
        this.gameStart = START_GAME;
        this.makeFont(
          !this.secondPlayer
            ? `${gameState.oneName} ${gameState.score.playerOne} : ${gameState.score.playerTwo} ${gameState.twoName}`
            : `${gameState.twoName} ${gameState.score.playerTwo} : ${gameState.score.playerOne} ${gameState.oneName}`
        );
      } else if (gameState.type === "gameEnd") {
        this.gameStart = END_GAME;
        this.makeFont(gameState.txt);
        // await this.dispose();
        if (this.textdata) {
          this.textdata.lookAt(this.camera.position);
        }
        window.removeEventListener("keydown", this.onKeyDownBound, false);
        window.removeEventListener("keyup", this.onKeyUpBound, false);
        // 간단 예시
        if (localStorage.getItem("matchType") !== "tournament") {
          if (localStorage.getItem("matchType") === "Pve") {
            await window.router.navigate(`/home`, false);
          } else {
            await window.router.navigate(`/result/${this.gameId}`, false);
          }
        } else {
          // Tournament 경우
          let count = 0;
          const id = setInterval(async () => {
            if (count > 10) {
              clearInterval(id);
              await window.router.navigate(`/home`, false);
              return;
            }
            try {
              clearInterval(id);
              const result = await getCurrentUserGameStatus();
              if (!result) {
                  const tournament_id = localStorage.getItem("tid");
                await window.router.navigate(`/result/${tournament_id}`, false);
            } else {
                await window.router.navigate(`/playing/${result.game_id}`, false);
              }
            } catch (err) {
              console.error("Error fetching game status:", err);
            }
            count++;
          }, 2000);
        }
      } else if (gameState.type === "secondPlayer") {
        this.secondPlayer = true;
        this.cameraTheta = -this.cameraTheta;
        this.updateCameraPosition();
        this.playerOne.material.color.setHex(this.initColor[0]);
        this.playerTwo.material.color.setHex(this.initColor[1]);
      } else if (gameState.type === "gameWait") {
        this.gameStart = WAIT_GAME;
        console.log("gameWait", gameState);
      } else if (gameState.type === "sound") {
        if (gameState.sound === "ballToWall" && this.audio.sounds.has("ball")) {
          this.audio.play("nomal_ball");
        }
      } else if (gameState.type === "effect") {
        this.effect.createImpact(gameState.op);
        this.audio.play("power_ball");
      }
    });
  }

  animate() {
    requestAnimationFrame(this.animate);
    if (this.gameStart === START_GAME) {
      if (this.textdata) {
        this.textdata.lookAt(this.camera.position);
      }
    } else if (this.gameStart === WAIT_GAME) {
      this.makeFont("waiting for player!");
    } else if (this.gameStart === END_GAME) {
      if (this.textdata) {
        this.textdata.rotation.y += 0.05;
      }
    }
    this.renderer.render(this.scene, this.camera);
  }
}

