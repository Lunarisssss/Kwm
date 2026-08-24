from flask import Flask, render_template_string

app = Flask(__name__)

# โค้ดหน้าเว็บแชทสไตล์ Neon Blue / Cyber Matrix
HTML_PAGE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surprise for you 💙</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --neon-blue: #22d3ee; /* cyan-400 */
            --neon-glow: rgba(34, 211, 238, 0.5);
            --dark-bg: #0f172a; /* slate-900 */
            --panel-bg: rgba(30, 41, 59, 0.85); /* slate-800 โปร่งแสง */
        }
        
        @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slide-in { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @keyframes pulse-ring {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 211, 238, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 12px rgba(34, 211, 238, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 211, 238, 0); }
        }
        @keyframes pulse-fast { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }

        .animate-fade-in { animation: fade-in 1s ease-out; }
        .animate-slide-in { animation: slide-in 0.4s ease-out forwards; }
        .animate-pulse-fast { animation: pulse-fast 1s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        .animate-pulse-ring { animation: pulse-ring 2s infinite; }
        .animate-float { animation: float 3s ease-in-out infinite; }

        body {
            background-color: var(--dark-bg);
            margin: 0;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: #e2e8f0; /* slate-200 */
        }

        /* ดีไซน์กล่องแชทแบบกระจกนีออน */
        .chat-container {
            border: 1px solid rgba(34, 211, 238, 0.3);
            box-shadow: 0 0 25px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(34, 211, 238, 0.05);
            backdrop-filter: blur(12px);
            background-color: var(--panel-bg);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .chat-container:hover { 
            transform: scale(1.01); 
            box-shadow: 0 0 30px rgba(34, 211, 238, 0.15), inset 0 0 15px rgba(34, 211, 238, 0.1);
        }

        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

        /* ปุ่มตัวเลือกสไตล์ Hologram */
        .option-button {
            background-color: rgba(15, 23, 42, 0.6);
            color: var(--neon-blue);
            border: 1px solid rgba(34, 211, 238, 0.4);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        .option-button:hover {
            background: rgba(34, 211, 238, 0.1);
            border-color: var(--neon-blue);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(34, 211, 238, 0.2);
            text-shadow: 0 0 8px var(--neon-blue);
        }
        .option-button:active { transform: translateY(1px); }

        /* กล่องข้อความ */
        .msg-bubble-bot {
            background-color: rgba(30, 41, 59, 0.9);
            color: #f8fafc;
            border-radius: 1.25rem;
            border-bottom-left-radius: 0.25rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .msg-bubble-user {
            background: linear-gradient(135deg, #0ea5e9, #0284c7); /* sky-500 to sky-600 */
            color: #fff;
            border-radius: 1.25rem;
            border-bottom-right-radius: 0.25rem;
            box-shadow: 0 4px 10px rgba(2, 132, 199, 0.4);
        }

        .chat-header { 
            border-bottom: 1px solid rgba(34, 211, 238, 0.2); 
            background: rgba(15, 23, 42, 0.8);
        }
    </style>
</head>
<body class="animate-fade-in m-0 relative">

    <!-- แคนวาสสายฝน Neon Matrix (Blue) -->
    <canvas id="matrixCanvas" class="fixed top-0 left-0 w-full h-full z-0 pointer-events-none"></canvas>

    <!-- กล่องแชทหลัก -->
    <div class="z-10 w-full max-w-md h-full sm:h-[85vh] chat-container flex flex-col sm:rounded-2xl relative animate-slide-in overflow-hidden">
        
        <!-- ส่วนหัว (Header) -->
        <div class="chat-header p-4 rounded-t-2xl flex items-center justify-between gap-3">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-slate-800 border border-cyan-400 flex items-center justify-center text-cyan-400 font-bold text-xl shadow-[0_0_10px_rgba(34,211,238,0.3)]">💙</div>
                <div>
                    <div class="text-cyan-400 font-bold text-lg flex items-center gap-1 tracking-wide">กล่องข้อความลับ </div>
                    <div class="text-slate-400 text-xs tracking-wider uppercase">กำลังส่งข้อความ...</div>
                </div>
            </div>
            <div class="flex items-center gap-1 text-cyan-400 animate-float text-xl opacity-80">✨</div>
        </div>

        <!-- ส่วนแชท (Chat Area) -->
        <div id="chat-box" class="flex-1 overflow-y-auto space-y-4 p-5 pb-6 scrollbar-hide">
            <!-- ข้อความแชทจะมาโผล่ตรงนี้ -->
        </div>
        
        <!-- ตัวบ่งชี้การพิมพ์ (Typing Indicator) -->
        <div id="typing-indicator" class="hidden flex justify-start mb-4 mx-5">
            <div class="bg-slate-800 border border-slate-700 px-5 py-3 rounded-2xl rounded-bl-none shadow-lg text-cyan-400 flex gap-2 items-center h-12">
                <span class="w-2.5 h-2.5 bg-cyan-400 rounded-full animate-pulse-fast shadow-[0_0_5px_#22d3ee]"></span>
                <span class="w-2.5 h-2.5 bg-cyan-400 rounded-full animate-pulse-fast shadow-[0_0_5px_#22d3ee]" style="animation-delay: 0.2s"></span>
                <span class="w-2.5 h-2.5 bg-cyan-400 rounded-full animate-pulse-fast shadow-[0_0_5px_#22d3ee]" style="animation-delay: 0.4s"></span>
            </div>
        </div>

        <!-- ส่วนปุ่มตัวเลือก (Options Box) -->
        <div id="options-box" class="flex flex-col gap-3 mt-2 px-5 pb-5 animate-slide-in">
            <!-- ปุ่มตัวเลือกจะมาโผล่ตรงนี้ -->
        </div>

        <!-- ส่วนรางวัล (Reward Box) -->
        <div id="reward-box" class="hidden mt-4 text-center px-5 pb-8 animate-pulse-ring mb-4">
            <p class="text-cyan-300 font-medium mb-3 text-sm tracking-widest uppercase">System Unlocked ✨</p>
            <a href="https://youtu.be/Uoxz9St00TI?si=PlN36_nd4MOjDwXe" target="_blank" 
               class="inline-block bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-4 px-10 rounded-xl shadow-[0_0_15px_rgba(34,211,238,0.5)] text-lg flex items-center justify-center gap-2 hover:scale-105 hover:shadow-[0_0_25px_rgba(34,211,238,0.7)] transition-all duration-300">
                <span class="text-xl">🎁</span> เปิดของขวัญ 
            </a>
        </div>
    </div>

    <script>
        // ==========================================
        // ส่วนที่ 1: ระบบ Matrix Digital Rain (สีฟ้า/ไซอัน)
        // ==========================================
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // ใช้ตัวอักษรแบบ Matrix
        const chars = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        const fontSize = 16;
        let columns = 0;
        let drops = [];

        function initMatrix() {
            columns = Math.floor(canvas.width / fontSize) + 1;
            drops = [];
            for(let i = 0; i < columns; i++) {
                drops[i] = Math.random() * -100; 
            }
        }
        initMatrix();
        window.addEventListener('resize', initMatrix);

        function drawMatrix() {
            // พื้นหลังดำโปร่งแสงเพื่อสร้างหางยาวๆ (Trail effect)
            ctx.fillStyle = 'rgba(15, 23, 42, 0.15)'; // slate-900
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const char = chars[Math.floor(Math.random() * chars.length)];
                
                // สุ่มสีโทน Cyan และ Blue
                if (Math.random() > 0.9) {
                    ctx.fillStyle = '#67e8f9'; // สว่างสุด (cyan-200)
                } else if (Math.random() > 0.5) {
                    ctx.fillStyle = '#06b6d4'; // กลาง (cyan-500)
                } else {
                    ctx.fillStyle = '#0284c7'; // เข้ม (sky-600)
                }

                if (drops[i] * fontSize > 0) {
                    ctx.fillText(char, i * fontSize, drops[i] * fontSize);
                }

                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 50);

        // ==========================================
        // ส่วนที่ 2: ระบบแชท (ข้อความเดิม)
        // ==========================================
        const chatFlow = [
            {
                botMessages: ["หวัดดีไอต้าวกื่อออ" ,"วันนี้เป็นไงบ้าง 🤨", "เหนื่อยไหม 🙂"],
                options: ["เหนื่อยสุดๆเลย 😩", "ไม่เหนื่อยครับ 😊", "เหนื่อยนิดหน่อย 😔"],
                getReply: (choice) => ["มาเดี๋ยวให้จับทีนึง 🤪 หมายถึงจับมือ "]
            },
            {
                botMessages: ["คิดถึงเค้าไหม"],
                options: ["คิดถึงนิดหน่อย 😌", "คิดถึง ☺️", "คิดถึงสุดๆ 💕"],
                getReply: (choice) => {
                    if (choice === 0) return ["เชอะ! คิดถึงนิดหน่อยเองหรอ 🥺"];
                    if (choice === 1) return ["คิดถึงเหมือนกัน 💖"];
                    return ["น่ารักที่สุดเลยยยย 🥳"];
                }
            },
            {
                botMessages: ["ถ้าตอนนี้เค้าวาร์ปไปอยู่ข้างๆ ได้ อยากให้ทำอะไรให้คะ"],
                options: ["นวดให้หน่อย ปวดตัวสุดๆ 😣", "ขอกอดแน่นๆ 😗", "พาไปหาของอร่อยกิน 🍔"],
                getReply: (choice) => {
                    if (choice === 0) return ["ได้เลยยย เตรียมตัวปวดกว่าเดิม เอ้ย! สบายตัวได้เลย 💆‍♂️"];
                    if (choice === 1) return ["ไม่ให้กอดหรอกกก ล้อเล่น 😘"];
                    return ["อย่าบอกนะว่าเลือกกิน ก็ได้ๆเดี๋ยวพาไปกินของอร่อย! 🍔"];
                }
            },
            {
                botMessages: ["สารภาพมาซะดีๆ วันนี้ดื้อป่าว หรือเป็นเด็กดี 😏"],
                options: ["เป็นเด็กดีสิ 😊", "ดื้อนิดนึงงง", "ดื้อมาก! 😡"],
                getReply: (choice) => {
                    if (choice === 0) return ["น่ารักมาก เอาจุ๊บไปหนึ่งที 😘"];
                    if (choice === 1) return ["ดื้อนิดนึงหรอ แบบนี้ต้องโดนอะไรดีนะ"];
                    return ["เตรียมตัวโดนดุเลย! หึ! อ่ะล้อเล่นนน 😂"];
                }
            },
            {
                botMessages: ["เอาล่ะ! ตอบคำถามครบแล้วถึงช่วงเวลาสุดท้าย อ่ะตื่นเต้นหน่อยเด้ !!!"],
                options: ["ลุยเลยยย 🤩", "ขอทำใจแป๊บ 🫣", "มีรางวัลด้วยหรอเนี่ย 😲"],
                getReply: (choice) => {
                    return ["แท่นแท๊น! กดปุ่มข้างล่างนี้ได้เลยยยยย 🎁"];
                },
                showReward: true
            }
        ];

        let currentStep = 0;
        const chatBox = document.getElementById('chat-box');
        const optionsBox = document.getElementById('options-box');
        const typingIndicator = document.getElementById('typing-indicator');
        const rewardBox = document.getElementById('reward-box');

        const delay = (ms) => new Promise(res => setTimeout(res, ms));

        function addMessage(text, sender) {
            const div = document.createElement('div');
            div.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} animate-slide-in`;
            
            const msgDiv = document.createElement('div');
            msgDiv.className = `px-5 py-3 max-w-[75%] font-medium text-[0.95rem] ${
                sender === 'user' 
                ? 'msg-bubble-user' 
                : 'msg-bubble-bot'
            }`;
            msgDiv.textContent = text;
            
            div.appendChild(msgDiv);
            chatBox.appendChild(div);
            chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
        }

        async function playBotMessages(messages) {
            optionsBox.innerHTML = '';
            typingIndicator.classList.remove('hidden');
            chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
            
            for(let msg of messages) {
                await delay(1200); 
                addMessage(msg, 'bot');
            }
            
            typingIndicator.classList.add('hidden');
            showOptions();
        }

        function showOptions() {
            if (currentStep === -1) return;
            const stepData = chatFlow[currentStep];
            optionsBox.innerHTML = '';
            optionsBox.classList.remove('hidden');
            optionsBox.classList.add('flex');
            
            stepData.options.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.className = "option-button font-medium py-3 px-5 rounded-xl text-center cursor-pointer";
                btn.textContent = opt;
                btn.onclick = () => handleChoice(opt, idx);
                optionsBox.appendChild(btn);
            });
        }

        async function handleChoice(text, idx) {
            addMessage(text, 'user');
            optionsBox.innerHTML = '';
            optionsBox.classList.add('hidden'); 
            
            const stepData = chatFlow[currentStep];
            const botReplies = stepData.getReply(idx);
            
            typingIndicator.classList.remove('hidden');
            chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
             
            for(let msg of botReplies) {
                await delay(1200);
                addMessage(msg, 'bot');
            }
            typingIndicator.classList.add('hidden');

            if (currentStep < chatFlow.length - 1) {
                currentStep++;
                playBotMessages(chatFlow[currentStep].botMessages);
            } else {
                currentStep = -1;
                if(stepData.showReward) {
                    rewardBox.classList.remove('hidden');
                    chatBox.scrollTo({ top: chatBox.scrollHeight + 100, behavior: 'smooth' });
                }
            }
        }

        playBotMessages(chatFlow[0].botMessages);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)