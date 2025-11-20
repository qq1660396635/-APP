目录
  1.   移动端竖屏适配
  2.   上方搜索栏
  3.   下方分页栏
  
  4.   背景颜色
  5.   每行三个   x
  6.   调试助手
           其他思路，随机背景颜色数组，击打特效
 
一.  零散脚本 移动端捕鱼适配
 <!-- 竖屏补丁，放在 </body> 前 -->
<script>
(function(){
    /* ========== 0. 等引擎加载完 ========== */
    function ready(fn){
        if(window.stage && stage.context && stage.context.canvas) return fn();
        setTimeout(function(){ready(fn)},30);
    }

    ready(function(){
        var canvas = stage.context.canvas,
            cStyle = canvas.style;

        /* ========== 1. 让画布“撑满”竖屏视口 ========== */
        function fit(){
            var W = window.innerWidth,          // 390 左右
                H = window.innerHeight;         // 844 左右

            /* 1.1 改绘图缓冲区（真正决定清晰度和坐标系） */
            canvas.width  = W;
            canvas.height = H;

            /* 1.2 改显示尺寸（让节点跟视口对齐） */
            cStyle.width  = W + 'px';
            cStyle.height = H + 'px';

            /* 1.3 通知引擎舞台变了（Quark 老版本没有就跳过） */
            stage.width  = W;
            stage.height = H;
            stage.resize && stage.resize(W,H);

            /* 1.4 把 FPS 定位到左上角，方便看效果 */
            var fps = document.getElementById('fps');
            if(fps) { fps.style.left = 0; fps.style.top = 0; }
        }

        /* ========== 2. 初次 + 每次转屏/地址栏收起都重新 fit ========== */
        fit();
        window.addEventListener('resize',fit);
        window.addEventListener('orientationchange',fit);

        /* ========== 3. 把老代码里写死的 980×545 全部替掉 ========== */
        /* 如果 fishjoy.js 里还有
           new Quark.Stage({width:980,height:545})
           把它改成
           new Quark.Stage({width:window.innerWidth,height:window.innerHeight})
           或者干脆把那段初始化搬到 fit() 里第一次执行。
           下面给出“搬移”示例： */
        if(stage.width===980){   // 发现老尺寸
            fit();               // 立即矫正
        }
    });
})();
</script>



二.  上方搜索栏
<!-- 搜索栏容器：start -->
<div class="search-box-wrapper">
  <input type="text" id="globalSearch" placeholder="🔍 搜索游戏名称…" autocomplete="off">
  <button id="globalSearchBtn" title="搜索"><i class="fa fa-search"></i></button>
  <button id="globalSearchClear" title="清空">×</button>
</div>

<style>
/* 搜索栏独立样式：start */
.search-box-wrapper{
  position:relative;
  max-width:480px;margin:20px auto;
  display:flex;align-items:center;
}
.search-box-wrapper input{
  flex:1;height:44px;padding:0 52px 0 18px;
  border:2px solid rgba(102,126,234,.3);border-radius:22px;
  font-size:16px;outline:none;transition:.3s;
}
.search-box-wrapper input:focus{
  border-color:#667eea;box-shadow:0 0 12px rgba(102,126,234,.35);
}
.search-box-wrapper button{
  position:absolute;border:none;background:#667eea;
  color:#fff;border-radius:50%;cursor:pointer;transition:.3s;
}
#globalSearchBtn{right:6px;width:36px;height:36px;}
#globalSearchClear{right:48px;width:24px;height:24px;background:#ff6b6b;display:none;}
.search-box-wrapper button:hover{transform:scale(1.1);}
/* 搜索栏独立样式：end */
</style>

<script>
/* 搜索栏独立逻辑：start */
(function(){
  const input  = document.getElementById('globalSearch');
  const btn    = document.getElementById('globalSearchBtn');
  const clear  = document.getElementById('globalSearchClear');

  function doSearch(){
    const kw = input.value.trim();
    clear.style.display = kw ? 'flex' : 'none';
    /* 这里把 kw 传给外部列表渲染函数即可 */
    console.log('搜索关键字：', kw);
  }
  btn.addEventListener('click', doSearch);
  input.addEventListener('keypress', e => { if(e.key==='Enter') doSearch(); });
  input.addEventListener('input', () => { clearTimeout(input.t); input.t=setTimeout(doSearch,300); });
  clear.addEventListener('click', () => { input.value=''; clear.style.display='none'; doSearch(); });
})();
/* 搜索栏独立逻辑：end */
</script>
<!-- 搜索栏容器：end -->




三  页脚分页，满xx个
<!-- 分页容器：start -->
<div id="pagerBox" class="pager-box"></div>

<style>
/* 分页独立样式：start */
.pager-box{display:flex;justify-content:center;gap:8px;margin:20px 0;}
.pager-box button{
  padding:6px 14px;border:1px solid #ccc;background:#fff;border-radius:4px;cursor:pointer;transition:.3s;
}
.pager-box button:hover{background:#667eea;color:#fff;}
.pager-box button.active{background:#ff6b6b;color:#fff;border-color:#ff6b6b;}
.pager-box button:disabled{opacity:.5;cursor:not-allowed;}
/* 分页独立样式：end */
</style>

<script>
/* 分页独立逻辑：start */
/**
 * 渲染分页按钮
 * @param {number} totalItems  总条数
 * @param {number} perPage     每页条数（如 30）
 * @param {number} current     当前页码（从 1 起）
 * @param {function} onChange  切换页码的回调，参数为新页码
 */
function renderPager(totalItems, perPage, current, onChange){
  const totalPages = Math.ceil(totalItems / perPage);
  const box = document.getElementById('pagerBox');
  box.innerHTML = '';

  if(totalPages <= 1) return;               // 不足 1 页不分页

  const createBtn = (txt, pg, dis) => {
    const b = document.createElement('button');
    b.innerHTML = txt; b.disabled = dis;
    if(pg === current) b.classList.add('active');
    if(!dis) b.addEventListener('click', () => onChange(pg));
    return b;
  };
  box.appendChild(createBtn('上一页', current - 1, current === 1));
  for(let i = 1; i <= totalPages; i++) box.appendChild(createBtn(i, i, false));
  box.appendChild(createBtn('下一页', current + 1, current === totalPages));
}
/* 分页独立逻辑：end */

/* 使用示例：start */
// 假设总数据 80 条，每页 30 条，当前第 2 页
renderPager(80, 30, 2, newPage => {
  console.log('用户切换到第', newPage, '页');
  // 这里重新请求数据并刷新列表
});
/* 使用示例：end */
</script>
<!-- 分页容器：end -->




四  随机切换背景颜色
<script>
/* ===== 随机炫酷背景切换：start ===== */
(function(){
  // 1. 15 组渐变配色，按喜好继续追加即可
  const gradients = [
    'linear-gradient(135deg,#667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg,#f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg,#4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg,#43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg,#fa709a 0%, #fee140 100%)',
    'linear-gradient(135deg,#30cfd0 0%, #330867 100%)',
    'linear-gradient(135deg,#a8edea 0%, #fed6e3 100%)',
    'linear-gradient(135deg,#ff9a9e 0%, #fecfef 50%, #fecfef 100%)',
    'linear-gradient(135deg,#ff5858 0%, #f09819 100%)',
    'linear-gradient(135deg,#fc466b 0%, #3f5efb 100%)',
    'linear-gradient(135deg,#e0c3fc 0%, #8ec5fc 100%)',
    'linear-gradient(135deg,#f6d365 0%, #fda085 100%)',
    'linear-gradient(135deg,#84fab0 0%, #8fd3f4 100%)',
    'linear-gradient(135deg,#a1c4fd 0%, #c2e9fb 100%)',
    'linear-gradient(135deg,#d4fc79 0%, #96e6a1 100%)'
  ];

  let idx = 0;                                    // 当前下标
  const body = document.body;
  body.style.transition = 'background 0.6s ease'; // 平滑过渡
  body.style.background = gradients[0];           // 初始背景

  // 2. 点击页面任意位置切换
  document.addEventListener('click', () => {
    idx = (idx + 1) % gradients.length;
    body.style.background = gradients[idx];
  });
})();
/* ===== 随机炫酷背景切换：end ===== */
</script>


五  每行3个
.game-grid {
    display: grid;               /* 启用网格 */
    grid-template-columns: repeat(3, 1fr);  /* 每行 3 列，等宽 */
    gap: 10px;                   /* 格子间距 */
    padding: 10px;
}

六. 调试助手
<!-- ✅ 调试面板：随时可删 -->
<div id="debugPanel" style="
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 120px;
    background: rgba(0,0,0,0.85);
    color: #0f0;
    font: 12px/1.4 monospace;
    overflow-y: auto;
    padding: 6px 8px;
    box-sizing: border-box;
    z-index: 9999;
    white-space: pre-wrap;
"></div>

<script>
/* ================ 调试钩子：随时可删 ================ */
(function(){
    const panel = document.getElementById('debugPanel');
    function log(...args) {
        panel.textContent = [...args].join(' ') + '\n' + panel.textContent;
        panel.scrollTop = 0;
    }

    // 保存原函数
    const oldMakeMove = GomokuGame.prototype.makeMove;
    const oldFindThreeThreat = GomokuGame.prototype.findThreeThreat;
    const oldCheckThreeInDirection = GomokuGame.prototype.checkThreeInDirection;

    // 落子钩子：打印下了哪、当前棋盘
    GomokuGame.prototype.makeMove = function(index, player) {
        const row = Math.floor(index / this.boardSize);
        const col = index % this.boardSize;
        log(`[落子] ${player} → (${row},${col})`);
        // 调用原版
        return oldMakeMove.call(this, index, player);
    };

    // 检测三连钩子：打印检测过程
    GomokuGame.prototype.findThreeThreat = function(player) {
        log(`[findThreeThreat] 开始检测 player=${player}`);
        const res = oldFindThreeThreat.call(this, player);
        log(`[findThreeThreat] 返回威胁索引：${res}`);
        return res;
    };

    // 方向检测钩子：打印详细参数
    GomokuGame.prototype.checkThreeInDirection = function(row, col, player, [dx, dy]) {
        const res = oldCheckThreeInDirection.call(this, row, col, player, [dx, dy]);
        log(`[checkThreeInDirection] (${row},${col}) dir(${dx},${dy}) → ${res ? '✅活三' : '❌不是活三'}`);
        return res;
    };
})();
</script>
<!-- ✅ 调试面板结束 -->