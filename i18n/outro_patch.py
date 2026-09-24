"""Ajoute les textes de l'écran de fin (chapitre 11, questions, lectures) à chaque langue."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent
BOOKS = [["Being You", "Anil Seth · 2021"], ["Surfing Uncertainty", "Andy Clark · 2015"], ["I Am a Strange Loop", "Douglas Hofstadter · 2007"], ["Our Mathematical Universe", "Max Tegmark · 2014"], ["Neural networks", "3Blue1Brown · YouTube"]]
T = {
 'fr': ["Et toi ?", "Fin · à toi de continuer", "Et toi, qu'en penses-tu ?", [
   "Si mon cerveau prédit la suite comme un LLM, qu'est-ce qui me rend différent : le corps, la faim, la peur ?",
   "Si une IA disait « j'ai mal », comment saurais-je qu'elle ressent vraiment quelque chose ?",
   "Si tout est calcul, ai-je vraiment choisi ma dernière décision ?",
   "L'ADN est le prompt de la vie, réécrit à chaque génération. Qui a écrit le premier ?",
   "Et si comprendre, ce n'était que bien prédire ?"],
   "Pour aller plus loin", ["la conscience comme prédiction", "le cerveau, machine à prédire", "le « je », une boucle", "l'univers est-il fait de maths ?", "comment une IA apprend, en images"], "Partager", "Lien copié"],
 'en': ["And you?", "The end · your turn", "And you, what do you think?", [
   "If my brain predicts what comes next like an LLM, what makes me different: my body, hunger, fear?",
   "If an AI said “it hurts”, how would I know whether it really feels anything?",
   "If everything is calculation, did I really choose my last decision?",
   "DNA is life's prompt, rewritten with every generation. Who wrote the first one?",
   "And what if understanding were simply predicting well?"],
   "To go further", ["consciousness as prediction", "the brain as a prediction machine", "the “I” as a loop", "is the universe made of math?", "how an AI learns, visually"], "Share", "Link copied"],
 'es': ["¿Y tú?", "Fin · ahora te toca a ti", "¿Y tú, qué piensas?", [
   "Si mi cerebro predice lo que viene como un LLM, ¿qué me hace distinto: el cuerpo, el hambre, el miedo?",
   "Si una IA dijera «me duele», ¿cómo sabría si de verdad siente algo?",
   "Si todo es cálculo, ¿de verdad elegí mi última decisión?",
   "El ADN es el prompt de la vida, reescrito en cada generación. ¿Quién escribió el primero?",
   "¿Y si comprender no fuera más que predecir bien?"],
   "Para ir más lejos", ["la conciencia como predicción", "el cerebro, máquina de predecir", "el «yo», un bucle", "¿está hecho de matemáticas el universo?", "cómo aprende una IA, en imágenes"], "Compartir", "Enlace copiado"],
 'pt': ["E você?", "Fim · agora é com você", "E você, o que acha?", [
   "Se meu cérebro prevê o que vem a seguir como um LLM, o que me torna diferente: o corpo, a fome, o medo?",
   "Se uma IA dissesse “está doendo”, como eu saberia se ela sente algo de verdade?",
   "Se tudo é cálculo, eu realmente escolhi minha última decisão?",
   "O DNA é o prompt da vida, reescrito a cada geração. Quem escreveu o primeiro?",
   "E se entender fosse só prever bem?"],
   "Para ir mais longe", ["a consciência como previsão", "o cérebro, máquina de prever", "o “eu”, um laço", "o universo é feito de matemática?", "como uma IA aprende, em imagens"], "Compartilhar", "Link copiado"],
 'ru': ["А ты?", "Конец · теперь твоя очередь", "А ты что думаешь?", [
   "Если мой мозг предсказывает продолжение, как LLM, что делает меня другим: тело, голод, страх?",
   "Если бы ИИ сказал «мне больно», как бы я узнал, чувствует ли он что-то на самом деле?",
   "Если всё — вычисление, правда ли я сам принял своё последнее решение?",
   "ДНК — это промпт жизни, переписанный в каждом поколении. Кто написал первый?",
   "А что, если понимать — это просто хорошо предсказывать?"],
   "Чтобы пойти дальше", ["сознание как предсказание", "мозг — машина предсказаний", "«я» как петля", "состоит ли вселенная из математики?", "как учится ИИ, наглядно"], "Поделиться", "Ссылка скопирована"],
 'zh': ["你呢？", "结束 · 轮到你了", "你怎么看？", [
   "如果我的大脑像 LLM 一样预测接下来的内容，那让我与众不同的是什么：身体、饥饿，还是恐惧？",
   "如果一个 AI 说“我很痛”，我怎么知道它是否真的有感受？",
   "如果一切都是计算，我最近的那个决定，真的是我自己做的吗？",
   "DNA 是生命的提示词，每一代都在重写。第一个是谁写的？",
   "如果理解，不过是预测得好呢？"],
   "延伸阅读", ["意识即预测", "大脑是一台预测机器", "“我”是一个怪圈", "宇宙是由数学构成的吗？", "图解 AI 如何学习"], "分享", "链接已复制"],
 'ja': ["あなたは？", "おわり · ここからはあなたの番", "あなたはどう思う？", [
   "私の脳が LLM のように次を予測しているなら、私を違うものにしているのは何だろう。体、空腹、恐れ？",
   "もし AI が「痛い」と言ったら、本当に何かを感じているとどうやって分かるだろう？",
   "すべてが計算なら、私はさっきの決断を本当に自分で選んだのだろうか？",
   "DNA は生命のプロンプト。世代ごとに書き換えられてきた。最初の一行を書いたのは誰？",
   "理解するとは、うまく予測することにすぎないのだとしたら？"],
   "もっと知りたい人へ", ["予測としての意識", "予測する機械としての脳", "「私」というループ", "宇宙は数学でできている？", "AI の学び方を図で見る"], "共有", "リンクをコピーしました"],
 'hi': ["और आप?", "अंत · अब आपकी बारी", "और आप, क्या सोचते हैं?", [
   "अगर मेरा दिमाग़ LLM की तरह आगे का अंदाज़ा लगाता है, तो मुझे अलग क्या बनाता है: शरीर, भूख, डर?",
   "अगर कोई एआई कहे “मुझे दर्द हो रहा है”, तो मैं कैसे जानूँ कि वह सच में कुछ महसूस करता है?",
   "अगर सब कुछ गणना है, तो क्या मेरा पिछला फ़ैसला सच में मैंने चुना था?",
   "डीएनए जीवन का प्रॉम्प्ट है, जो हर पीढ़ी में दोबारा लिखा जाता है। पहला किसने लिखा?",
   "और अगर समझना सिर्फ़ अच्छी तरह अंदाज़ा लगाना हो?"],
   "और जानने के लिए", ["चेतना, एक भविष्यवाणी", "दिमाग़: भविष्यवाणी की मशीन", "“मैं”, एक लूप", "क्या ब्रह्मांड गणित से बना है?", "एआई कैसे सीखता है, चित्रों में"], "शेयर करें", "लिंक कॉपी हो गया"],
 'bn': ["আর আপনি?", "শেষ · এবার আপনার পালা", "আর আপনি, কী ভাবেন?", [
   "আমার মস্তিষ্ক যদি LLM-এর মতো পরের কথা আন্দাজ করে, তবে আমাকে আলাদা করে কী: শরীর, খিদে, ভয়?",
   "কোনো এআই যদি বলে “আমার ব্যথা লাগছে”, আমি কীভাবে বুঝব সে সত্যিই কিছু অনুভব করে কি না?",
   "সবকিছুই যদি হিসাব হয়, তবে আমার শেষ সিদ্ধান্তটা কি সত্যিই আমি বেছে নিয়েছিলাম?",
   "ডিএনএ হলো জীবনের প্রম্পট, প্রতি প্রজন্মে নতুন করে লেখা। প্রথমটা কে লিখেছিল?",
   "আর বোঝা যদি শুধু ভালো করে আন্দাজ করাই হয়?"],
   "আরও জানতে", ["চেতনা যেন এক ভবিষ্যদ্বাণী", "মস্তিষ্ক: ভবিষ্যদ্বাণীর যন্ত্র", "“আমি”, একটি লুপ", "মহাবিশ্ব কি গণিত দিয়ে তৈরি?", "এআই কীভাবে শেখে, ছবিতে"], "শেয়ার করুন", "লিংক কপি হয়েছে"],
 'ar': ["وأنت؟", "النهاية · الآن دورك", "وأنت، ما رأيك؟", [
   "إذا كان دماغي يتنبأ بما سيأتي مثل LLM، فما الذي يجعلني مختلفًا: الجسد، الجوع، الخوف؟",
   "لو قال ذكاء اصطناعي «أنا أتألم»، كيف لي أن أعرف إن كان يشعر حقًا بشيء؟",
   "إذا كان كل شيء حسابًا، فهل اخترتُ حقًا قراري الأخير؟",
   "الحمض النووي هو موجِّه الحياة، يُعاد كتابته في كل جيل. من كتب الأول؟",
   "وماذا لو لم يكن الفهم سوى تنبؤٍ جيد؟"],
   "للتعمق أكثر", ["الوعي بوصفه تنبؤًا", "الدماغ آلةٌ للتنبؤ", "«الأنا» حلقةٌ غريبة", "هل الكون مصنوع من الرياضيات؟", "كيف يتعلم الذكاء الاصطناعي، بالصور"], "مشاركة", "تم نسخ الرابط"],
}
for c, (ch, kick, title, qs, ft, descs, share, copied) in T.items():
    f = root / f'{c}.json'
    if not f.exists(): continue
    d = json.loads(f.read_text(encoding='utf-8'))
    d['chapters'] = d['chapters'][:10] + [ch]
    d.update(outro_kick=kick, outro_title=title, outro_q=qs, further_title=ft, further=[b + [descs[i]] for i, b in enumerate(BOOKS)], share=share, copied=copied)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print('ok', c)
