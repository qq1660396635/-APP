/* 一、外层：一行一个卡片 */
.cards-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* 二、内层：卡片内一行两个脚本 */
.script-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

/* 三、最窄宽度参考 */
.games-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}

/* 四、手机强制双列 */
@media (max-width: 768px) {
    .script-list {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 五、细节微调 */
.script-item {
    padding: 10px;
}

.script-name {
    white-space: normal;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}


# 网页 3D / 漫画 / 粒子背景 CDN 速查（思维导图版）

## 一 3D 引擎类
### 1.1 Three.js 官方生态
- 1 r134 核心 https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js
- 2 控制器 OrbitControls https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/controls/OrbitControls.js
- 3 后处理库 EffectComposer https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/postprocessing/EffectComposer.js
- 4 3D 字体加载器 https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/loaders/FontLoader.js

### 1.2 Babylon.js 微软系
- 1 核心引擎 https://cdn.babylonjs.com/babylon.js
- 2 加载器扩展 https://cdn.babylonjs.com/loaders/babylonjs.loaders.min.js
- 3 GUI 系统 https://cdn.babylonjs.com/gui/babylon.gui.min.js
- 4 材质库 https://cdn.babylonjs.com/materialsLibrary/babylonjs.materials.min.js

### 1.3 PlayCanvas 轻量备选
- 1 引擎 https://code.playcanvas.com/playcanvas-stable.min.js

## 二 Vanta 现成着色器（3D 背景一键用）
### 2.1 自然流体
- 1 waves https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js
- 2 cloud https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.cloud.min.js
- 3 fog https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.fog.min.js

### 2.2 粒子宇宙
- 1 net https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js
- 2 dots https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.dots.min.js
- 3 rings https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js

### 2.3 几何科技
- 1 cells https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.cells.min.js
- 2 halo https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.halo.min.js
- 3 tron https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.tron.min.js

## 三 漫画 / 像素风
### 3.1 cmx.js 漫画滤镜
- 1 核心 https://unpkg.com/cmx.js@latest/dist/cmx.min.js

### 3.2 PixiJS 2D 卡通
- 1 核心 https://cdn.jsdelivr.net/npm/pixi.js@6.x/dist/browser/pixi.min.js
- 2 滤镜包 https://cdn.jsdelivr.net/npm/pixi-filters@4.x/dist/browser/pixi-filters.js

### 3.3 Aseprite-WASM 像素
- 1 运行时 https://cdn.jsdelivr.net/npm/aseprite-wasm@latest/dist/aseprite-wasm.js

## 四 粒子专项
### 4.1 tsParticles 通用
- 1 核心 https://cdn.jsdelivr.net/npm/tsparticles@2.x/tsparticles.bundle.min.js
- 2 预设气泡 https://cdn.jsdelivr.net/npm/tsparticles-preset-bubbles@2.x/dist/tsparticles.preset.bubbles.min.js
- 3 预设雪花 https://cdn.jsdelivr.net/npm/tsparticles-preset-snow@2.x/dist/tsparticles.preset.snow.min.js

### 4.2 particles.js 经典
- 1 核心 https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js

### 4.3 three-particles 3D 粒子
- 1 扩展 https://cdn.jsdelivr.net/npm/three-particles@1.0.0/dist/three-particles.min.js

## 五 音频可视化
### 5.1 wavesurfer.js
- 1 核心 https://cdn.jsdelivr.net/npm/wavesurfer.js@6.x/dist/wavesurfer.min.js
- 2 时间轴插件 https://cdn.jsdelivr.net/npm/wavesurfer.js@6.x/dist/plugin/wavesurfer.timeline.min.js

### 5.2 p5.sound 创意可视化
- 1 p5 核心 https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js
- 2 声音库 https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/addons/p5.sound.min.js

## 六 其他特效补充
### 6.1 鼠标跟随星轨
- 1 mouse-constellation https://cdn.jsdelivr.net/npm/mouse-constellation@1.0.0/dist/mc.min.js

### 6.2 动态线条 mesh
- 1 meshline https://cdn.jsdelivr.net/npm/three.meshline@1.3.0/THREE.MeshLine.js

### 6.3 随机可爱动物图
- 1 place-puppy https://place-puppy.com/300/200
- 2 placekitten https://placekitten.com/300/200
