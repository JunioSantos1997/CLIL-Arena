import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update JS
js_old = """    /* ----- FASE 1: Sorteador ----- */
    function onDeckClick() {
      if (els.deckWrapper.classList.contains('disabled') || els.deckWrapper.classList.contains('shuffling')) return;

      els.deckWrapper.classList.add('shuffling');
      
      // Criar cartas falsas para o shuffle
      const numCards = 8;
      for (let i = 0; i < numCards; i++) {
        const c = document.createElement('img');
        c.src = 'imagens/verso.png';
        c.className = 'shuffle-card';
        
        c.style.setProperty('--dx1', (Math.random() * 100 - 50) + 'px');
        c.style.setProperty('--dy1', (Math.random() * 80 - 40) + 'px');
        c.style.setProperty('--rot1', (Math.random() * 16 - 8) + 'deg');
        
        c.style.setProperty('--dx2', (Math.random() * 140 - 70) + 'px');
        c.style.setProperty('--dy2', (Math.random() * 60 - 30) + 'px');
        c.style.setProperty('--rot2', (Math.random() * 16 - 8) + 'deg');
        
        c.style.setProperty('--dx3', (Math.random() * 80 - 40) + 'px');
        c.style.setProperty('--dy3', (Math.random() * 120 - 60) + 'px');
        c.style.setProperty('--rot3', (Math.random() * 16 - 8) + 'deg');
        
        c.style.setProperty('--dx4', (Math.random() * 50 - 25) + 'px');
        c.style.setProperty('--dy4', (Math.random() * 80 - 40) + 'px');
        c.style.setProperty('--rot4', (Math.random() * 16 - 8) + 'deg');
        
        c.style.animationDelay = (i * 0.05) + 's';
        
        els.deckWrapper.appendChild(c);
      }

      setTimeout(() => {
        els.deckWrapper.querySelectorAll('.shuffle-card').forEach(el => el.remove());
        els.deckWrapper.classList.remove('shuffling');
        
        els.deckWrapper.classList.add('glow-pulse');
        
        setTimeout(() => {
          els.deckWrapper.classList.remove('glow-pulse');
          proceedWithReveal();
        }, 600);
      }, 2100);
    }"""

js_new = """    /* ----- FASE 1: Sorteador ----- */
    function onDeckClick() {
      if (els.deckWrapper.classList.contains('disabled') || els.deckWrapper.classList.contains('shuffling')) return;

      els.deckWrapper.classList.add('shuffling');
      
      // Criar cartas falsas para o shuffle 3D
      const numCards = 12; // Mais cartas para volume
      for (let i = 0; i < numCards; i++) {
        const c = document.createElement('img');
        c.src = 'imagens/verso.png';
        c.className = 'shuffle-card';
        
        // Direção alternada (esq/dir) para o shuffle
        const dir = i % 2 === 0 ? 1 : -1;
        
        // Posições extremas com grande variação em Z (frente e fundo)
        c.style.setProperty('--tx1', (Math.random() * 180 * dir) + 'px');
        c.style.setProperty('--ty1', (Math.random() * 80 - 40) + 'px');
        c.style.setProperty('--tz1', (Math.random() * 150 + 50) + 'px'); // Frente
        c.style.setProperty('--r1', (Math.random() * 30 * dir) + 'deg');
        
        c.style.setProperty('--tx2', (Math.random() * 180 * -dir) + 'px');
        c.style.setProperty('--ty2', (Math.random() * 80 - 40) + 'px');
        c.style.setProperty('--tz2', (Math.random() * -150 - 50) + 'px'); // Fundo
        c.style.setProperty('--r2', (Math.random() * 30 * -dir) + 'deg');
        
        c.style.setProperty('--tx3', (Math.random() * 120 * dir) + 'px');
        c.style.setProperty('--ty3', (Math.random() * 60 - 30) + 'px');
        c.style.setProperty('--tz3', (Math.random() * 100 + 20) + 'px'); // Frente
        c.style.setProperty('--r3', (Math.random() * 15 * dir) + 'deg');
        
        c.style.setProperty('--tx4', (Math.random() * 60 * -dir) + 'px');
        c.style.setProperty('--ty4', (Math.random() * 40 - 20) + 'px');
        c.style.setProperty('--tz4', (Math.random() * -100 - 20) + 'px'); // Fundo
        c.style.setProperty('--r4', (Math.random() * 10 * -dir) + 'deg');
        
        c.style.animationDelay = (i * 0.04) + 's';
        
        els.deckWrapper.appendChild(c);
      }

      setTimeout(() => {
        els.deckWrapper.querySelectorAll('.shuffle-card').forEach(el => el.remove());
        els.deckWrapper.classList.remove('shuffling');
        
        els.deckWrapper.classList.add('glow-pulse');
        
        setTimeout(() => {
          els.deckWrapper.classList.remove('glow-pulse');
          proceedWithReveal();
        }, 600);
      }, 2100);
    }"""

content = content.replace(js_old, js_new)


# Remove the old .deck-wrapper, .deck-aura, .deck-card block at the top
content = re.sub(r'\.deck-wrapper\s*\{[^}]*\}', '', content, count=1)
content = re.sub(r'\.deck-aura\s*\{[^}]*\}', '', content, count=1)
content = re.sub(r'\.deck-card\s*\{[^}]*\}', '', content, count=1)


# Replace the old shuffle css block with the new one
css_pattern = re.compile(r'/\* Animação Shuffle do Deck \*/.*?</style>', re.DOTALL)

css_new = """/* Animação Shuffle do Deck 3D */
    .deck-wrapper {
      position: relative;
      cursor: pointer;
      transition: transform 0.2s;
      perspective: 1500px;
      transform-style: preserve-3d;
    }

    .deck-aura {
      position: absolute;
      inset: -20px;
      background: radial-gradient(circle, rgba(212, 175, 55, 0.4) 0%, transparent 70%);
      animation: auraPulse 1.5s ease-in-out infinite;
      pointer-events: none;
      transform: translateZ(-200px);
    }

    .deck-card {
      width: var(--card-w);
      aspect-ratio: 3/4;
      border: 3px solid var(--gold);
      box-shadow:
        0 0 15px rgba(212, 175, 55, 0.4),
        inset 0 0 15px rgba(0, 180, 216, 0.2);
      object-fit: cover;
      display: block;
      position: relative;
      clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
      z-index: 5;
    }

    .shuffling .deck-card {
      animation: mainCardShake3D 0.4s ease-in-out infinite alternate;
    }

    @keyframes mainCardShake3D {
      0% { transform: translate3d(0, 0, 0) rotate(0deg); }
      50% { transform: translate3d(5px, -5px, -10px) rotate(2deg); }
      100% { transform: translate3d(-5px, 5px, 10px) rotate(-2deg); }
    }

    .shuffle-card {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      border-radius: inherit;
      border: 3px solid var(--gold);
      box-shadow: 0 5px 25px rgba(0,0,0,0.4);
      object-fit: cover;
      clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
      opacity: 0;
    }

    .shuffling .shuffle-card {
      opacity: 1;
      animation: shuffleAnim3D 2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }

    .deck-wrapper.shuffling { pointer-events: none; }
    .deck-wrapper.glow-pulse .deck-card {
      animation: mainCardGlow 0.6s ease-out forwards;
    }

    @keyframes shuffleAnim3D {
      0% { transform: translate3d(0, 0, 0) rotate(0deg); opacity: 0; }
      10% { opacity: 1; }
      25% { transform: translate3d(var(--tx1), var(--ty1), var(--tz1)) rotate(var(--r1)); }
      50% { transform: translate3d(var(--tx2), var(--ty2), var(--tz2)) rotate(var(--r2)); }
      75% { transform: translate3d(var(--tx3), var(--ty3), var(--tz3)) rotate(var(--r3)); }
      90% { transform: translate3d(var(--tx4), var(--ty4), var(--tz4)) rotate(var(--r4)); opacity: 1; }
      100% { transform: translate3d(0, 0, 0) rotate(0deg); opacity: 0; }
    }

    @keyframes mainCardGlow {
      0% { transform: scale(1); box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
      50% { transform: scale(1.1); box-shadow: 0 0 50px rgba(212, 175, 55, 1), 0 0 30px #fff; }
      100% { transform: scale(1); box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    }
  </style>"""

content = css_pattern.sub(css_new, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
