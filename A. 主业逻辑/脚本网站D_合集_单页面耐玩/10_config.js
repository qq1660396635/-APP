// config.js
// 人生模拟器配置文件 - 充满“人味”的故事库 v4.0 (超长版)

// --- 辅助函数 ---
function createEvent(text, effects = {}, requirement = null, ageDescription = null, isDeath = false) {
    return { text, effects, requirement, ageDescription, isDeath };
}

// --- 事件生成器 (更注重细节、情感和时代感) ---
function generateRelationshipEvents(age) {
    const positives = [
        `你${age}岁时，遇到了那个让你觉得“就是TA了”的人，世界都变亮了。`,
        `你${age}岁时，和一位失联多年的挚友重新取得了联系，你们彻夜长谈。`,
        `你${age}岁时，你的孩子对你说“我爱你”，你觉得一切都值了。`,
        `你${age}岁时，你原谅了一个曾经伤害过你的人，内心获得了平静。`,
        `你${age}岁时，你领养了一只小动物，它成了你不可或缺的家人。`,
        `你${age}岁时，在一次聚会上，你进行了一次深入灵魂的交谈，感觉找到了知己。`,
        `你${age}岁时，你帮助了一个陌生人，对方真诚的感谢让你温暖了很久。`,
        `你${age}岁时，你和家人一起度过了一个完美的节日，充满了欢声笑语。`,
        `你${age}岁时，你的伴侣为你准备了一个惊喜的生日派对，你感动得热泪盈眶。`,
        `你${age}岁时，你鼓起勇气向暗恋的人表白，没想到对方也喜欢你。`,
    ];
    const negatives = [
        `你${age}岁时，经历了一场刻骨铭心的背叛，你开始怀疑人性。`,
        `你${age}岁时，你最爱的人离你而去，你的世界瞬间崩塌。`,
        `你${age}岁时，你发现最好的朋友在背后说你坏话。`,
        `你${age}岁时，你与父母大吵一架，离家出走。`,
        `你${age}岁时，你因为性格不合，与恋人痛苦地分手。`,
        `你${age}岁时，你深陷一段不健康的单恋，无法自拔。`,
        `你${age}岁时，你因为一件小事和最好的朋友决裂，从此再无联系。`,
        `你${age}岁时，你被网络暴力了，无数陌生的恶意让你窒息。`,
        `你${age}岁时，你发现伴侣一直在对你撒谎，信任的基石彻底粉碎。`,
        `你${age}岁时，你被朋友欺骗，损失了一大笔钱。`,
        `你${age}岁时，你卷入了一场激烈的家族纷争，身心俱疲。`,
    ];
    const neutrals = [
        `你${age}岁时，参加了一场同学聚会，发现大家都有了各自的生活轨迹。`,
        `你${age}岁时，你搬到了一个新的城市，不得不重新建立社交圈。`,
        `你${age}岁时，你和邻居成了点头之交，偶尔会互相帮忙收快递。`,
        `你${age}岁时，你被拉进了一个几乎不说话的微信群。`,
        `你${age}岁时，你发现，长大后能交到真心朋友的机会越来越少。`,
    ];
    const all = [...positives, ...negatives, ...neutrals];
    const chosen = all[Math.floor(Math.random() * all.length)];
    let effect = {};
    if (positives.includes(chosen)) {
        effect = { happiness: 30, social: 20 };
    } else if (negatives.includes(chosen)) {
        effect = { happiness: -30, social: -20, health: -10 };
    } else {
        effect = { social: 5 };
    }
    return [createEvent(chosen, effect)];
}

function generateHobbyEvents(age) {
    const hobbies = [
        { text: `你${age}岁时，迷上了在深夜的电台里点歌，把心事说给陌生人听。`, effects: { happiness: 10 } },
        { text: `你${age}岁时，开始学习烘焙，烤出的第一个蛋糕虽然卖相不好，但很甜。`, effects: { happiness: 15, health: 5 } },
        { text: `你${age}岁时，迷上了摇滚乐，在房间里疯狂甩头，仿佛能甩掉所有烦恼。`, effects: { happiness: 20 } },
        { text: `你${age}岁时，开始写日记，把所有不敢说出口的话都写了进去。`, effects: { happiness: 5 } },
        { text: `你${age}岁时，迷上了跑酷，在城市的屋顶间跳跃，感受风和自由。`, effects: { health: 20, happiness: 15 }, isDeath: Math.random() < 0.05 },
        { text: `你${age}岁时，成了一个植物爱好者，阳台变成了你的小花园。`, effects: { happiness: 15, health: 10 } },
        { text: `你${age}岁时，沉迷于构建模型，在微缩世界里找到了秩序和宁静。`, effects: { happiness: 10, knowledge: 5 } },
        { text: `你${age}岁时，迷上了露营，在山野间支起帐篷，与星空为伴。`, effects: { health: 10, happiness: 20 } },
        { text: `你${age}岁时，开始玩密室逃脱，享受解谜和团队合作带来的快感。`, effects: { happiness: 15, social: 10 } },
        { text: `你${age}岁时，沉迷于网络游戏，在虚拟世界里称王称霸。`, effects: { happiness: 10, health: -15, social: -5 } },
        { text: `你${age}岁时，开始学习一门乐器，虽然不成调，但乐在其中。`, effects: { happiness: 15 } },
        { text: `你${age}岁时，爱上了摄影，用镜头记录下生活中的点点滴滴。`, effects: { happiness: 15, knowledge: 5 } },
        { text: `你${age}岁时，迷上了剧本杀，在别人的故事里体验不同的人生。`, effects: { happiness: 20, social: 15 } },
        { text: `你${age}岁时，开始练习冥想，试图在喧嚣的世界中找到内心的平静。`, effects: { happiness: 10, health: 5 } },
        { text: `你${age}岁时，迷上了手冲咖啡，享受着研磨和冲泡过程中的仪式感。`, effects: { happiness: 10 } },
        { text: `你${age}岁时，开始学习木工，亲手为自己做了一把椅子。`, effects: { happiness: 20, health: 5 } },
        { text: `你${age}岁时，成了一个美食博主，探店是你的日常。`, effects: { happiness: 15, wealth: -10 } },
        { text: `你${age}岁时，迷上了天文，买了一台望远镜，在阳台上寻找星辰。`, effects: { knowledge: 15, happiness: 10 } },
    ];
    return [hobbies[Math.floor(Math.random() * hobbies.length)]];
}

function generatePhilosophyEvents(age) {
    const books = [
        { text: `你${age}岁时，读了《百年孤独》，你开始思考家族和宿命的意义。`, effects: { knowledge: 20, happiness: -5 } },
        { text: `你${age}岁时，读了《三体》，你对宇宙的浩瀚和人类的渺小感到敬畏。`, effects: { knowledge: 25, flags: { cyber_path: 1 } } },
        { text: `你${age}岁时，读了《活着》，你更加珍惜眼前的生活。`, effects: { happiness: 20, health: 5 } },
        { text: `你${age}岁时，读了尼采，你开始相信“上帝已死”，并试图成为自己的超人。`, effects: { knowledge: 20, happiness: -10 } },
        { text: `你${age}岁时，读了佛经，你开始理解“无常”和“放下”。`, effects: { happiness: 15 } },
        { text: `你${age}岁时，读了《局外人》，加缪的冷漠让你感到一种奇异的共鸣，你开始思考自己与世界的关系。`, effects: { knowledge: 20, happiness: -10 } },
        { text: `你${age}岁时，读了《人类简史》，你对人类文明的演进有了全新的认识。`, effects: { knowledge: 30 } },
        { text: `你${age}岁时，读了《1984》，你对监控和权力产生了深深的恐惧。`, effects: { knowledge: 20, happiness: -15 } },
        { text: `你${age}岁时，读了《小王子》，你明白了“真正重要的东西，用眼睛是看不见的”。`, effects: { happiness: 20 } },
        { text: `你${age}岁时，读了《月亮与六便士》，你开始思考理想与现实的冲突。`, effects: { knowledge: 15, happiness: -5 } },
        { text: `你${age}岁时，读了《围城》，你深刻理解了“城外的人想进去，城里的人想出来”。`, effects: { knowledge: 15, happiness: -10 } },
        { text: `你${age}岁时，读了《悉达多》，你开始了一场向内的精神之旅。`, effects: { happiness: 15, knowledge: 10 } },
        { text: `你${age}岁时，读了《禅与摩托车维修艺术》，你开始思考“良质”到底是什么。`, effects: { knowledge: 25, happiness: 5 } },
    ];
    return [books[Math.floor(Math.random() * books.length)]];
}

function generateWorkLifeEvents(age) {
    const events = [
        { text: `你${age}岁时，被一个画大饼的老板忽悠，加入了创业公司，每天激情燃烧。`, effects: { wealth: -10, health: -15, happiness: 10 } },
        { text: `你${age}岁时，在公司的酒局上，你为了签下合同，喝到不省人事。`, effects: { wealth: 20, health: -20, happiness: -15 } },
        { text: `你${age}岁时，你的一个项目大获成功，你在庆功宴上被众人簇拥。`, effects: { wealth: 30, happiness: 25, social: 20 } },
        { text: `你${age}岁时，你厌倦了内卷，辞职去大理开了个小客栈。`, effects: { wealth: -30, happiness: 20 } },
        { text: `你${age}岁时，你成了“螺丝钉”，每天重复着同样的工作，感觉生命在流逝。`, effects: { happiness: -20, health: -10 } },
        { text: `你${age}岁时，你因为办公室政治，被同事排挤。`, effects: { happiness: -25, social: -30 } },
        { text: `你${age}岁时，你被裁员了，看着空荡荡的工位，你感到了前所未有的迷茫。`, effects: { wealth: -40, happiness: -30 } },
        { text: `你${age}岁时，你开始做自由职业，虽然收入不稳定，但拥有了自由。`, effects: { wealth: 10, happiness: 15 } },
        { text: `你${age}岁时，你被提拔为经理，但巨大的压力让你夜不能寐。`, effects: { wealth: 25, health: -15, happiness: -5 } },
        { text: `你${age}岁时，你和同事办公室恋情曝光，被迫一人离职。`, effects: { happiness: -20, wealth: -10 } },
        { text: `你${age}岁时，你遇到了一个好导师，在你的职业生涯上给了很多帮助。`, effects: { happiness: 20, knowledge: 15, wealth: 10 } },
        { text: `你${age}岁时，你创业失败了，欠了一屁股债。`, effects: { wealth: -50, happiness: -40, health: -20 } },
        { text: `你${age}岁时，你跳槽到了一家更有前景的公司，薪水翻倍。`, effects: { wealth: 40, happiness: 20 } },
        { text: `你${age}岁时，你因为工作失误，给公司造成了巨大损失，被开除了。`, effects: { wealth: -20, happiness: -35 } },
        { text: `你${age}岁时，你考上了公务员，虽然工资不高，但生活稳定。`, effects: { wealth: 10, happiness: 15, health: 5 } },
    ];
    return [events[Math.floor(Math.random() * events.length)]];
}

function generateHealthEvents(age) {
    const events = [
        { text: `你${age}岁时，你坚持锻炼，身体状态前所未有地好。`, effects: { health: 25, happiness: 10 } },
        { text: `你${age}岁时，你得了重感冒，在床上躺了一周。`, effects: { health: -15, happiness: -10, wealth: -5 } },
        { text: `你${age}岁时，你开始失眠，每晚都在数羊中度过。`, effects: { health: -20, happiness: -15 } },
        { text: `你${age}岁时，你在体检时查出了脂肪肝，医生让你多运动。`, effects: { health: -10, happiness: -5 } },
        { text: `你${age}岁时，你因为一场意外骨折了，打了好几个月的石膏。`, effects: { health: -30, happiness: -15, wealth: -10 } },
        { text: `你${age}岁时，你开始脱发，每次洗头都心惊胆战。`, effects: { health: -5, happiness: -20 } },
        { text: `你${age}岁时，你尝试了禁果，事后却陷入了无尽的恐惧和懊悔，你偷偷去检查身体。`, effects: { health: -10, happiness: -40, wealth: -10 } },
        { text: `你${age}岁时，你被诊断出患有慢性病，需要长期服药。`, effects: { health: -25, wealth: -15, happiness: -20 } },
        { text: `你${age}岁时，你成功减肥20斤，整个人都自信了起来。`, effects: { health: 20, happiness: 30 } },
        { text: `你${age}岁时，你得了阑尾炎，做了一场小手术。`, effects: { health: -15, wealth: -20, happiness: -10 } },
        { text: `你${age}岁时，你因为长期熬夜，心脏开始出现问题。`, effects: { health: -30, happiness: -20 } },
        { text: `你${age}岁时，你染上了烟瘾，肺活量越来越差。`, effects: { health: -25, wealth: -10 } },
        { text: `你${age}岁时，你因为一次不洁的性行为，感染了梅毒，开始了漫长而羞耻的治疗过程。`, effects: { health: -40, wealth: -50, happiness: -50, social: -20 } },
        { text: `你${age}岁时，你开始注重养生，每天早睡早起，喝枸杞泡水。`, effects: { health: 15, happiness: 5 } },
        { text: `你${age}岁时，你拔掉了四颗智齿，脸肿得像猪头。`, effects: { health: -10, happiness: -15, wealth: -10 } },
    ];
    return [events[Math.floor(Math.random() * events.length)]];
}

// --- 按年龄分组的事件池 ---
const allLifeEvents = {
    "0": [
        createEvent("你在一声啼哭中来到这个世界，父母为你取了一个充满希望的名字。", { happiness: 10 }),
        createEvent("你是个意外，你的到来并没有给这个家庭带来太多喜悦。", { happiness: -20, social: -10 }),
        createEvent("你出生在风暴之夜，接生婆说这孩子命不凡。", { happiness: 5, flags: { special_birth: 1 } }),
        createEvent("你是个双胞胎之一，从出生起就从未真正孤单过。", { social: 30, happiness: 10 }),
        createEvent("你出生时，家里一贫如洗，你的第一件衣服是用旧衣服改的。", { wealth: -30, health: -10 }),
        createEvent("你是剖腹产出生的，妈妈肚子上留下了一道永恒的印记。", { health: -5 }),
        createEvent("你出生时很健康，护士夸你是个漂亮宝宝。", { health: 10, happiness: 10 }),
    ],
    "1": [
        createEvent("你学会了走路，摇摇晃晃地扑向妈妈的怀抱。", { health: 10, happiness: 20 }),
        createEvent("你长出了第一颗牙，喜欢咬一切能咬的东西。", { health: 5 }),
        createEvent("你得了幼儿急疹，发了几天高烧，把父母吓坏了。", { health: -15, happiness: -10 }),
        createEvent("你第一次清晰地喊出“妈妈”，让家人欣喜若狂。", { happiness: 25 }),
    ],
    "3": [
        createEvent("你被送进了幼儿园，你抱着妈妈的腿不肯松手，哭得撕心裂肺。", { happiness: -20, social: -10 }),
        createEvent("你在幼儿园里抢了别的小朋友的玩具，被老师批评了。", { happiness: -10, social: -15 }),
        createEvent("你在幼儿园交到了第一个朋友，你们分享了一块饼干。", { happiness: 15, social: 20 }),
        createEvent("你开始对世界充满好奇，问出了第一个“为什么”。", { knowledge: 10 }),
    ],
    "5": [
        createEvent("你第一次看到雪，兴奋地在院子里打滚，结果感冒了。", { health: -10, happiness: 20 }),
        createEvent("你在幼儿园被孤立，因为你不爱说话，只是喜欢看蚂蚁搬家。", { social: -20, happiness: -10 }),
        createEvent("你得到了第一辆玩具车，你睡觉都抱着它。", { happiness: 25 }),
        createEvent("你目睹了一次邻里间的激烈争吵，让你第一次感到了恐惧。", { happiness: -15, health: -5 }),
        createEvent("你相信了童话，一直在等待骑着白马的王子。", { happiness: 15 }),
        createEvent("你开始学钢琴，但每天枯燥的练习让你很痛苦。", { happiness: -10, knowledge: 10 }),
        ...generateRelationshipEvents(5), ...generateHobbyEvents(5)
    ],
    "7": [
        createEvent("你上小学了，对新环境既紧张又兴奋。", { happiness: 10, social: 10 }),
        createEvent("你因为考试没考好，被父母狠狠地训了一顿。", { happiness: -20, social: -5 }),
        createEvent("你在学校文艺汇演上表演了节目，赢得了满堂彩。", { happiness: 30, social: 25 }),
        createEvent("你开始意识到自己家境普通，有些羡慕别的同学。", { happiness: -10, wealth: -10 }),
        ...generateRelationshipEvents(7), ...generateHobbyEvents(7)
    ],
    "10": [
        createEvent("你开始意识到自己长得不好看，变得有些自卑。", { happiness: -20 }),
        createEvent("你偷偷拿了家里的钱去买游戏卡，被发现后挨了一顿毒打。", { happiness: -30, wealth: -10 }),
        createEvent("你在作文本上写下了你的梦想：成为一名宇航员。", { happiness: 20, knowledge: 10 }),
        createEvent("你最好的朋友因为搬家转学了，你哭了一整天。", { happiness: -25, social: -15 }),
        createEvent("你看了《终结者2》，从此对人工智能又爱又怕。", { knowledge: 15, flags: { cyber_path: 1 } }),
        createEvent("你在自然课上解剖了青蛙，你并没有感到不适，反而很着迷。", { knowledge: 15, flags: { bio_path: 1 } }),
        createEvent("你迷上了日本动漫，开始学起了蹩脚的日语。", { happiness: 15, knowledge: 5 }),
        createEvent("你参加了学校的奥数班，发现自己在这方面很有天赋。", { knowledge: 20, happiness: 10 }),
        ...generateRelationshipEvents(10), ...generateHobbyEvents(10), ...generatePhilosophyEvents(10)
    ],
    "12": [
        createEvent("你进入了青春期，脸上开始长痘痘，声音也变了。", { health: -5, happiness: -10 }),
        createEvent("你有了自己的小秘密，开始写上锁的日记。", { happiness: 5 }),
        createEvent("你和父母因为“早恋”问题爆发了激烈的争吵。", { happiness: -30, social: -20 }),
        createEvent("你迷上了某个明星，房间里贴满了TA的海报。", { happiness: 15 }),
        ...generateRelationshipEvents(12), ...generateHealthEvents(12)
    ],
    "15": [
        createEvent("你开始写诗，诗句里充满了无人能懂的忧郁。", { happiness: 5, knowledge: 10 }),
        createEvent("你为了融入集体，学会了抽烟，但呛得你直流眼泪。", { happiness: -10, health: -15, social: 5 }),
        createEvent("你第一次有了喜欢的人，连看一眼都会心跳加速。", { happiness: 30 }),
        createEvent("你因为顶撞老师，被请了家长，回家后又被混合双打。", { happiness: -20, health: -10 }),
        createEvent("你迷上了赛博朋克文化，开始幻想改造自己的身体。", { knowledge: 20, flags: { cyber_path: 2 } }),
        createEvent("你参加了生物夏令营，第一次在显微镜下看到了细胞的世界。", { knowledge: 25, flags: { bio_path: 2 } }),
        createEvent("你因为身材被同学嘲笑，你开始节食，得了厌食症。", { health: -30, happiness: -30 }),
        createEvent("你经历了中考，压力大到脱发。", { health: -10, happiness: -15, knowledge: 10 }),
        ...generateRelationshipEvents(15), ...generateWorkLifeEvents(15), ...generateHobbyEvents(15)
    ],
    "18": [
        createEvent("你参加了高考，考完感觉身体被掏空。", { health: -20, happiness: -10, knowledge: 15 }),
        createEvent("你考上了一所理想的大学，全家为你摆了庆功宴。", { happiness: 40, social: 20 }),
        createEvent("你高考失利，只能去一所不喜欢的学校，你感到很失落。", { happiness: -30, social: -10 }),
        createEvent("你第一次离开家去外地读大学，对自由充满了向往。", { happiness: 25, social: 15 }),
        createEvent("你在大学军训时晒得黢黑，但和同学建立了革命友谊。", { health: -5, social: 20, happiness: 10 }),
        ...generateRelationshipEvents(18), ...generateHobbyEvents(18)
    ],
    "20": [
        createEvent("你第一次独自旅行，在陌生的城市里，你感到了自由。", { happiness: 25, wealth: -20 }),
        createEvent("你在大学里加入了话剧社，在舞台上，你成了另一个人。", { happiness: 20, social: 25 }),
        createEvent("你经历了一场网恋，奔现后发现对方和照片差距很大。", { happiness: -20, wealth: -10 }),
        createEvent("你为了考研，在图书馆里度过了无数个日夜，头发大把大把地掉。", { health: -20, knowledge: 30, happiness: -10 }),
        createEvent("你进入了一家顶级科技公司实习，接触到了最前沿的AI技术。", { knowledge: 35, wealth: 10, flags: { cyber_path: 2 } }),
        createEvent("你成为了实验室的助手，每天与小白鼠和细胞培养皿为伴。", { knowledge: 30, flags: { bio_path: 2 } }),
        createEvent("你染上了赌瘾，把父母给的生活费都输光了。", { wealth: -40, happiness: -40 }),
        createEvent("你在大学里谈了一场轰轰烈烈的恋爱，最后却无疾而终。", { happiness: -25, social: -15 }),
        ...generateRelationshipEvents(20), ...generateWorkLifeEvents(20), ...generateHobbyEvents(20), ...generateHealthEvents(20)
    ],
    "22": [
        createEvent("你大学毕业，穿着学士服拍下了毕业照，对未来充满憧憬。", { happiness: 30 }),
        createEvent("你投了无数份简历，却石沉大海，你感到了就业的压力。", { happiness: -25, wealth: -10 }),
        createEvent("你找到了第一份工作，虽然薪水不高，但你干劲十足。", { wealth: 20, happiness: 20 }),
        createEvent("你和大学恋人因为异地而分手，在火车站哭成了泪人。", { happiness: -35, social: -20 }),
        createEvent("你决定考研“二战”，搬到了学校附近租了个小房子。", { wealth: -15, happiness: -10 }),
        ...generateRelationshipEvents(22), ...generateWorkLifeEvents(22)
    ],
    "25": [
        createEvent("你参加了一场说走就走的旅行，在西藏，你看到了最纯净的星空。", { happiness: 30, wealth: -15 }),
        createEvent("你被诊断出有抑郁症，世界在你眼中失去了色彩。", { happiness: -40, health: -20 }),
        createEvent("你结婚了，婚礼上，你看着对方的眼睛，觉得拥有了全世界。", { happiness: 50, social: 30 }),
        createEvent("你为了凑首付，向所有亲戚朋友借遍了钱。", { wealth: -20, social: -10, happiness: -15 }),
        createEvent("你参与了一个秘密项目，试图将人类记忆数字化。", { knowledge: 40, flags: { cyber_path: 2 } }),
        createEvent("你开始进行基因剪辑实验，试图创造出完美的生物。", { knowledge: 40, flags: { bio_path: 2 } }),
        createEvent("你在一次派对上，尝试了违禁药品，从此堕入深渊。", { health: -50, happiness: -30, wealth: -20 }),
        createEvent("你买了属于自己的第一套房，虽然背负着沉重的房贷。", { wealth: -40, happiness: 25 }),
        ...generateRelationshipEvents(25), ...generateWorkLifeEvents(25), ...generatePhilosophyEvents(25), ...generateHealthEvents(25)
    ],
    "28": [
        createEvent("你被催婚催到烦躁，开始怀疑婚姻的意义。", { happiness: -20, social: -15 }),
        createEvent("你工作几年后，决定辞职出国留学，给自己充充电。", { wealth: -30, happiness: 15, knowledge: 20 }),
        createEvent("你在行业里小有名气，开始有猎头挖你。", { wealth: 20, happiness: 25 }),
        createEvent("你看着同龄人结婚生子，感到了一丝焦虑。", { happiness: -15 }),
        ...generateRelationshipEvents(28), ...generateWorkLifeEvents(28)
    ],
    "30": [
        createEvent("你的孩子出生了，你抱着小小的TA，感到了沉甸甸的责任。", { happiness: 35, wealth: -25 }),
        createEvent("你中年危机提前到来，你买了一辆摩托车，想去追寻风。", { happiness: 15, wealth: -30 }),
        createEvent("你发现伴侣出轨了，你的世界天翻地覆。", { happiness: -45, social: -20 }),
        createEvent("你升职了，但头发也越来越少了。", { wealth: 30, health: -15, happiness: 10 }),
        createEvent("你成功将一段动物记忆上传到了计算机，虽然只有几秒钟。", { knowledge: 50, flags: { cyber_path: 2 } }),
        createEvent("你研发出了一种可以修复受损细胞的技术，但副作用未知。", { knowledge: 45, flags: { bio_path: 2 } }),
        createEvent("你开始健身，看着镜子里日益清晰的肌肉，你找回了自信。", { health: 25, happiness: 20 }),
        createEvent("你参加了朋友的婚礼，在宴桌上感慨万千。", { happiness: 10, social: 15 }),
        ...generateRelationshipEvents(30), ...generateWorkLifeEvents(30), ...generateHobbyEvents(30), ...generateHealthEvents(30)
    ],
    "32": [
        createEvent("你为了孩子的学区房，愁白了头。", { wealth: -30, happiness: -20 }),
        createEvent("你发现养一个孩子，成本远超想象。", { wealth: -25, happiness: -10 }),
        createEvent("你和伴侣因为育儿观念不同，频繁吵架。", { happiness: -25, social: -15 }),
        createEvent("你看着孩子学会走路，第一次叫你“爸爸/妈妈”，你激动得哭了。", { happiness: 40 }),
    ],
    "35": [
        createEvent("你送孩子去上幼儿园，看着TA小小的背影，你眼眶湿润了。", { happiness: 20 }),
        createEvent("你和多年未见的老同学重逢，发现大家都变了。", { happiness: 10, social: 15 }),
        createEvent("你为了一个项目，连续一个月没回家，成功后却感到一阵空虚。", { happiness: -10, health: -30, wealth: 40 }),
        createEvent("你开始相信玄学，找人算命，对方说你中年有劫。", { happiness: -10 }),
        createEvent("你给自己植入了第一个脑机接口，可以直接用思维上网。", { knowledge: 60, health: -10, flags: { cyber_path: 2 } }),
        createEvent("你冒险在自己身上进行了第一次人体基因优化实验。", { health: -25, knowledge: 50, flags: { bio_path: 2 } }),
        createEvent("你学会了喝酒，但每次都喝醉，然后说着胡话哭。", { happiness: -15, health: -20 }),
        createEvent("你的职位被更年轻、更有冲劲的人取代了。", { wealth: -20, happiness: -30 }),
        ...generateRelationshipEvents(35), ...generateWorkLifeEvents(35), ...generatePhilosophyEvents(35), ...generateHealthEvents(35)
    ],
    "38": [
        createEvent("你开始有意识地抗衰老，用上了最贵的眼霜。", { wealth: -15, happiness: 5 }),
        createEvent("你的婚姻进入了平淡期，激情似乎被柴米油盐磨光了。", { happiness: -20 }),
        createEvent("你开始辅导孩子写作业，血压因此飙升。", { health: -10, happiness: -15 }),
        createEvent("你意外地得到了一笔遗产，生活宽裕了不少。", { wealth: 50, happiness: 30 }),
    ],
    "40": [
        createEvent("你看着镜子里自己的白发，第一次感到了衰老。", { happiness: -15, health: -10 }),
        createEvent("你的公司上市了，你一夜之间实现了财富自由。", { wealth: 80, happiness: 40 }),
        createEvent("你父母中的一位生病了，你奔波在医院和公司之间。", { health: -20, happiness: -25, wealth: -15 }),
        createEvent("你迷上了钓鱼，在水库边一坐就是一天，享受着宁静。", { happiness: 20, health: 10 }),
        createEvent("你的机械义肢出现了排异反应，让你痛苦不堪。", { health: -30, flags: { cyber_path: 1 } }),
        createEvent("你的长寿药物出现了可怕的副作用，你的皮肤开始变得像树皮一样。", { health: -40, flags: { bio_path: 1 } }),
        createEvent("你参加了同学会，发现混得最好的不是当年学习最好的那个。", { happiness: -5 }),
        createEvent("你开始注重体检，每年都做一次全面的身体检查。", { health: 10, wealth: -5 }),
        ...generateRelationshipEvents(40), ...generateWorkLifeEvents(40), ...generateHobbyEvents(40), ...generateHealthEvents(40)
    ],
    "42": [
        createEvent("你进入了“上有老下有小”的阶段，感觉自己是家庭的顶梁柱。", { health: -10, happiness: -5 }),
        createEvent("你的孩子进入了叛逆期，处处和你对着干。", { happiness: -25, social: -20 }),
        createEvent("你和伴侣的关系因为各种压力而变得紧张。", { happiness: -20 }),
        createEvent("你开始怀念起年轻时的自由和无忧无虑。", { happiness: -15 }),
    ],
    "45": [
        createEvent("你进入了空巢期，家里突然变得好安静。", { happiness: -20 }),
        createEvent("你和伴侣重燃爱火，来了一场说走就走的二次蜜月。", { happiness: 30 }),
        createEvent("你被诊断出高血压，医生让你戒烟戒酒。", { health: -25 }),
        createEvent("你开始学习书法，试图在笔墨中寻找内心的平和。", { happiness: 15 }),
        createEvent("你开始用机械替换更多器官，感觉自己越来越不像人类。", { health: 20, knowledge: 40, happiness: -30, flags: { cyber_path: 2 } }),
        createEvent("你成功逆转了生物衰老，但你的精神状态却越来越不稳定。", { health: 30, happiness: -40, flags: { bio_path: 2 } }),
        createEvent("你开始信命，觉得一切都是安排好的。", { happiness: -10 }),
        createEvent("你的孩子考上了大学，你既骄傲又不舍。", { happiness: 30, wealth: -20 }),
        ...generateRelationshipEvents(45), ...generateWorkLifeEvents(45), ...generatePhilosophyEvents(45), ...generateHealthEvents(45)
    ],
    "48": [
        createEvent("你开始面临职场天花板，晋升变得遥遥无期。", { happiness: -15, wealth: -10 }),
        createEvent("你开始为退休生活做规划，研究起了理财产品。", { wealth: 10, knowledge: 10 }),
        createEvent("你发现自己越来越容易疲劳，精力大不如前。", { health: -15 }),
        createEvent("你迷上了逛公园，看大爷大妈下棋跳舞。", { happiness: 10, social: 10 }),
    ],
    "50": [
        createEvent("你参加了孩子的婚礼，看着TA穿上了婚纱/西装，你百感交集。", { happiness: 35 }),
        createEvent("你退休了，每天的生活就是散步、看报、逗鸟。", { happiness: 5 }),
        createEvent("你开始怀念起年轻时的自己，那个无所畏惧的少年/少女。", { happiness: -10 }),
        createEvent("你学会了用智能手机，开始刷短视频，乐此不疲。", { happiness: 15, knowledge: 10 }),
        createEvent("你上传了你的完整人格副本，网络上的“你”比真实的你更活跃。", { knowledge: 70, flags: { cyber_path: 1 } }),
        createEvent("你的生物公司被查封，你的研究成果被视为非法。", { wealth: -60, happiness: -50, flags: { bio_path: 1 } }),
        createEvent("你迷上了养花，看着它们从种子到开花，你感受到了生命的力量。", { happiness: 20, health: 10 }),
        createEvent("你加入了社区的广场舞队伍，成了领舞。", { health: 15, happiness: 20, social: 25 }),
        ...generateRelationshipEvents(50), ...generateHobbyEvents(50), ...generateHealthEvents(50)
    ],
    "52": [
        createEvent("你开始吃各种保健品，希望能延年益寿。", { health: 5, wealth: -10 }),
        createEvent("你和老伴一起报了个旅游团，周游世界。", { happiness: 30, wealth: -25, health: 10 }),
        createEvent("你的老伙计们开始讨论谁谁谁走了，你感到了生命的脆弱。", { happiness: -20 }),
    ],
    "55": [
        createEvent("你的老伴去世了，你对着TA的遗像说了一下午的话。", { happiness: -50, social: -40 }),
        createEvent("你加入了老年合唱团，在歌声中，你仿佛又回到了年轻时代。", { happiness: 25, social: 30, health: 10 }),
        createEvent("你身体大不如前，上下楼梯都变得困难。", { health: -30 }),
        createEvent("你开始整理旧物，翻出了一箱情书，读着读着就笑了，笑着笑着就哭了。", { happiness: -5 }),
        createEvent("你的机械身体开始出现各种小故障，维修费用高昂。", { wealth: -30, health: -20 }),
        createEvent("你成了一个隐士，在深山里研究生命的终极奥秘。", { happiness: 10, knowledge: 30 }),
        createEvent("你有了第一个孙辈，你抱着TA，仿佛看到了生命的延续。", { happiness: 40 }),
        ...generateRelationshipEvents(55), ...generateHobbyEvents(55), ...generateHealthEvents(55)
    ],
    "58": [
        createEvent("你开始依赖拐杖走路。", { health: -20 }),
        createEvent("你的听力开始下降，和人交流变得有些困难。", { health: -15, happiness: -10 }),
        createEvent("你开始写回忆录，想把这一生的故事都记录下来。", { happiness: 20, knowledge: 10 }),
    ],
    "60": [
        createEvent("你有了第一个孙辈，你抱着TA，仿佛看到了生命的延续。", { happiness: 40 }),
        createEvent("你的记性越来越差，有时候会忘记刚刚发生过的事。", { health: -40, happiness: -20 }),
        createEvent("你搬进了养老院，这里有很多和你一样的老人。", { social: 10, happiness: -5 }),
        createEvent("你开始写回忆录，想把这一生的故事都记录下来。", { happiness: 20 }),
        createEvent("你的纯机械身体已经无法支持复杂活动，你大部分时间都连接在维生系统上。", { health: -40, knowledge: 20 }),
        createEvent("你看着镜子里依然年轻的容颜，感到了与世界的格格不入。", { happiness: -35 }),
        createEvent("你正式退休，把工作交给了年轻人。", { happiness: 10, wealth: -10 }),
        ...generateRelationshipEvents(60), ...generatePhilosophyEvents(60), ...generateHealthEvents(60)
    ],
    "62": [
        createEvent("你开始对食物越来越挑剔，只吃得下软烂的东西。", { health: -10 }),
        createEvent("你每天最大的乐趣就是看电视里的养生节目。", { happiness: 5, knowledge: 5 }),
        createEvent("你因为一次小摔倒，住进了医院，子女们都赶了回来。", { health: -25, happiness: -10 }),
    ],
    "65": [
        createEvent("你每天最大的乐趣，就是推着轮椅在公园里晒太阳。", { happiness: 10, health: -5 }),
        createEvent("你老友的葬礼一个接一个，你开始思考死亡。", { happiness: -30 }),
        createEvent("你学会了用智能手机和孙辈视频，这是你最大的快乐来源。", { happiness: 25, social: 15 }),
        createEvent("你开始研究家谱，想知道自己从哪里来。", { knowledge: 20, happiness: 10 }),
        createEvent("你决定放弃物理身体，将意识完全数字化。", { health: -100, knowledge: 100, flags: { cyber_path: 3 } }),
        createEvent("你注射了第一代稳定型长寿血清，身体的衰老进程明显减缓。", { health: 30, wealth: -50, flags: { bio_path: 3 } }),
        ...generateRelationshipEvents(65), ...generateHobbyEvents(65), ...generateHealthEvents(65)
    ],
    "68": [
        createEvent("你开始频繁地做梦，梦里全是年轻时的往事。", { happiness: 5, health: -5 }),
        createEvent("你的老房子被拆迁，你分到了一套新房子和一笔钱。", { wealth: 60, happiness: 20 }),
        createEvent("你感觉自己的时间不多了，开始和子女交代后事。", { happiness: -15 }),
    ],
    "70": [
        createEvent("你已经看淡了生死，每天只是平静地活着。", { happiness: 5 }),
        createEvent("你摔了一跤，之后身体就每况愈下。", { health: -35 }),
        createEvent("你成了一位慈祥的老人，孩子们都喜欢听你讲过去的故事。", { happiness: 25, social: 20 }),
        createEvent("你开始信仰宗教，从中获得了慰藉。", { happiness: 15 }),
        createEvent("你的基因优化出现了排异反应，身体机能开始紊乱。", { health: -50, happiness: -30, flags: { bio_path: 1 } }),
        ...generateRelationshipEvents(70), ...generatePhilosophyEvents(70), ...generateHealthEvents(70)
    ],
    "72": [
        createEvent("你大部分时间都在打盹，醒着的时候也有些迷糊。", { health: -20 }),
        createEvent("你住进了ICU，身上插满了管子。", { health: -40, wealth: -50, happiness: -30 }),
        createEvent("你看着窗外四季更迭，感慨万千。", { happiness: 10 }),
    ],
    "75": [
        createEvent("你大部分时间都在睡觉，梦里全是年轻时的往事。", { health: -20 }),
        createEvent("你立下了遗嘱，把一切都安排得明明白白。", { happiness: -5 }),
        createEvent("你觉得自己活不了多久了，但内心很平静。", { happiness: 10 }),
        createEvent("你的身体机能全面衰退，进入了临终关怀阶段。", { health: -50 }),
        ...generateRelationshipEvents(75)
    ],
    "78": [
        createEvent("你在一个平静的午后，在睡梦中离开了人世。", { isDeath: true, text: "你在一个平静的午后，在睡梦中离开了人世。" }),
        createEvent("你因为器官衰竭，在医院安详离世。", { isDeath: true, text: "你因为器官衰竭，在医院安详离世。" }),
        createEvent("你吃了一块最喜欢的蛋糕，噎住了，没能抢救过来。", { isDeath: true, text: "你吃了一块最喜欢的蛋糕，噎住了，没能抢救过来。" }),
        createEvent("你看着家人围绕在床边，微笑着闭上了眼睛。", { isDeath: true, text: "你看着家人围绕在床边，微笑着闭上了眼睛。" }),
    ],
    "80": [ createEvent("你已经不在乎外界的纷纷扰扰，只求内心安宁。") ],
    "82": [
        createEvent("你的记忆出现了混乱，有时会认不出自己的孩子。", { health: -30, happiness: -20 }),
        createEvent("你成了一位百岁老人，记者来采访你的长寿秘诀。", { happiness: 20, social: 15 }),
    ],
    "85": [ createEvent("你像一个老灵魂，静静地观察着这个熟悉又陌生的世界。") ],
    "90": [ createEvent("你觉得自己的一生，就像一部漫长的电影，终于要落幕了。") ],
    "95": [ createEvent("你已经活成了一个传奇，家族里的每一个人都听过你的故事。") ],
    "100": [
        createEvent("你迎来了你的100岁生日，五代同堂为你庆祝。", { happiness: 50, social: 40 }),
        createEvent("你的身体已经极度衰弱，但意识依然清醒。", { health: -40 }),
    ],
    // --- 超长寿路径事件 ---
    "110": [
        createEvent("作为数字生命，你见证了人类文明的又一次技术爆炸。", { knowledge: 100, flags: { cyber_path: 3 } }),
        createEvent("作为生物超人，你看着曾曾曾孙结婚，感慨万千。", { happiness: 10, flags: { bio_path: 3 } }),
    ],
    "120": [
        createEvent("你在数据之海中漂流，偶然发现了一个外星文明的信号。", { knowledge: 200, flags: { cyber_path: 3 } }),
        createEvent("你的肉体虽然不朽，但精神上的孤独感几乎将你吞噬。", { happiness: -50, flags: { bio_path: 3 } }),
    ],
    "150": [
        createEvent("你选择将你的数字意识广播到整个宇宙，寻找同类。", { knowledge: 300, flags: { cyber_path: 3 } }),
        createEvent("在无尽的时光中，你选择了自我终结，将最后的遗产留给世界。", { isDeath: true, text: "在无尽的时光中，你选择了自我终结，将最后的遗产留给世界。", flags: { bio_path: 3 } }),
    ],
    "200": [
        createEvent("你的意识与宇宙本身融为一体，你成为了永恒。", { isDeath: true, text: "你的意识与宇宙本身融为一体，你成为了永恒。", flags: { cyber_path: 3 } }),
    ],
};

// --- 死亡事件库 (更具文学性和“人味”) ---
const deathEvents = [
    { id: 'cancer', text: "你被癌症折磨了很久，最后在睡梦中解脱了。" },
    { id: 'heart_attack', text: "你心口一阵剧痛，想起了还有很多事没做，眼前一黑。" },
    { id: 'stroke', text: "你倒下了，半边身体不能动弹，在床上躺了几年后，安详离去。" },
    { id: 'accident', text: "一场突如其来的意外，为你的人生画上了句号。" },
    { id: 'suicide', text: "你选择了在一个雨夜结束自己的生命，你觉得这世界没什么可留恋的。" },
    { id: 'pneumonia', text: "一场普通的感冒，却因为身体虚弱，发展成了要命的肺炎。" },
    { id: 'natural_causes', text: "你寿终正寝，在一个温暖的午后，躺在摇椅上睡着了，再也没有醒来。" },
    { id: 'lonely_death', text: "你在等红绿灯时，安详地倒下。人们匆匆走过，没人知道一个灵魂刚刚离开了这个世界。" },
    { id: 'dementia', text: "你在遗忘的迷雾中走了很久，最后连自己都忘记了，安静地离去。" },
    { id: 'overwork', text: "你倒在了你奋斗一生的岗位上，电脑屏幕还亮着。" },
    { id: 'car_crash', text: "刺眼的远光灯和刺耳的刹车声，是你最后的记忆。" },
    { id: 'fall', text: "你在浴室滑倒，冰冷的地板是你最后的触感。" },
    { id: 'fire', text: "你在睡梦中被浓烟呛醒，没能逃出来。" },
    { id: 'drowning', text: "失足落水，你挣扎了几下，水灌进了你的肺里，世界归于寂静。" },
    { id: 'murder', text: "你走在黑暗的小巷，一把刀抵住了你的腰。" },
    { id: 'sudden_illness', text: "昨天还好好的，今天却突然发起高烧，很快就失去了意识。" },
    { id: 'drug_overdose', text: "在迷幻的烟雾中，你感觉身体飘了起来，然后就再也没落下。" },
    { id: 'electrocution', text: "你想自己修一下电器，一阵麻酥感过后，一切都结束了。" },
    { id: 'hypothermia', text: "在一个寒冷的冬夜，你蜷缩在角落里，渐渐失去了知觉。" },
    { id: 'cholesterol', text: "血管里的垃圾，最终堵死了生命的通道。" },
    { id: 'liver_cirrhosis', text: "你的肝脏硬如石头，再也无法支撑你的生命。" },
    { id: 'sepsis', text: "一个小小的伤口，却引发了全身的感染，你最终死于败血症。" },
    { id: 'meteorite', text: "你正悠闲地散步，一颗陨石从天而降，精准地砸中了你。这概率比中彩票还低。" },
    { id: 'laugh_death', text: "你听到了一个天大的笑话，笑得喘不过气，就这么笑死了。" },
    { id: 'sad_death', text: "你因为一件伤心事，流了一夜的泪，第二天早上，身体已经冰凉。" },
    { id: 'happiness_death', text: "你中了巨额彩票，兴奋过度，心脏病突发而死。" },
    { id: 'simulation_end', text: "你所感知到的一切，都只是一个模拟程序。现在，程序结束了。" },
    { id: 'alzheimer_fade', text: "你在阿尔茨海默症的侵蚀下，记忆一点点被抹去，最终像一张白纸一样离开了世界。" },
    { id: 'diabetes_complication', text: "长期的糖尿病引发了多种并发症，你的身体机能逐渐衰竭。" },
    { id: 'kidney_failure', text: "你的肾脏衰竭了，每周几次的透析最终还是没能挽回你的生命。" },
    { id: 'suicide_by_starvation', text: "你患上了严重的厌食症，最终在饥饿中走向了死亡。" },
    { id: 'plane_crash', text: "你乘坐的飞机失事了，在最后的时刻，你给家人发了最后一条信息：“我爱你”。" },
    { id: 'food_choking', text: "你在一次家庭聚餐上，被一块肉噎住，在众人的惊呼声中窒息而死。" },
    { id: 'cyber_rejection', text: "你的机械身体产生了剧烈的排异反应，系统崩溃，意识随之消散。", flags: { cyber_path: 1 } },
    { id: 'bio_mutation', text: "基因编辑的最终后果显现，你的身体发生了不可控的恐怖突变，在痛苦中死去。", flags: { bio_path: 1 } },
];

// --- 特殊结局 ---
const specialEndings = {
    cyber_ending: {
        text: "你抛弃了脆弱的肉身，将意识上传至庞大的机械网络。你成为了永生的数字幽灵，在数据之海中观察着人类文明的演化，直到宇宙的尽头。你，已经不再是“你”了。",
        age: 220,
    },
    bio_ending: {
        text: "你成功研发并使用了终极长寿血清。你的细胞停止了衰老，疾病与你绝缘。你看着身边的人一代代老去、死亡，成为了孤独的神。最终，在无尽的时光中，你选择了自我终结。",
        age: 150,
    },
};
